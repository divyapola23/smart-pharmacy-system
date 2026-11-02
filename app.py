"""Flask application: routes, login/session handling, CSRF and permissions.

Business rules live in services/*.py; this file only
  1. authenticates the user and checks the role,
  2. passes form data to a service,
  3. shows a success or error message.
"""
import hmac
import logging
import os
import secrets
from datetime import timedelta
from functools import wraps

from flask import (
    Flask, Response, abort, flash, g, redirect, render_template, request,
    send_from_directory, session, url_for,
)
from werkzeug.security import check_password_hash

import database
from services import (
    inventory_service as inv, report_service as rep,
    transaction_service as txn, waste_service as waste,
)
from services.common import ServiceError, today

ADMIN, PHARMACIST = "admin", "pharmacist"
log = logging.getLogger("pharmacy")


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATABASE=os.environ.get("PHARMACY_DB", database.DEFAULT_DB_PATH),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        # Set SESSION_COOKIE_SECURE=1 when serving over HTTPS.
        SESSION_COOKIE_SECURE=os.environ.get("SESSION_COOKIE_SECURE") == "1",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=2),
    )
    if test_config:
        app.config.update(test_config)
    if not app.config["SECRET_KEY"]:
        # No hardcoded key. A random one works for local use, but everyone is
        # logged out whenever the server restarts. Set SECRET_KEY to avoid that.
        app.config["SECRET_KEY"] = secrets.token_hex(32)
        log.warning("SECRET_KEY not set; using a temporary random key.")

    database.init_db(app.config["DATABASE"])  # CREATE IF NOT EXISTS: never deletes data

    # ------------------------------------------------------------ helpers
    def get_db():
        if "db" not in g:
            g.db = database.get_connection(app.config["DATABASE"])
        return g.db

    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.before_request
    def load_user_and_check_csrf():
        g.user = None
        user_id = session.get("user_id")
        if user_id is not None:
            g.user = get_db().execute(
                "SELECT user_id, name, email, role FROM users WHERE user_id = ?",
                (user_id,)).fetchone()
            if g.user is None:
                session.clear()
        if request.method == "POST":  # every state-changing request needs a CSRF token
            sent = request.form.get("csrf_token", "")
            expected = session.get("csrf_token", "")
            if not expected or not hmac.compare_digest(sent, expected):
                abort(400, "Your form expired or was invalid. Please go back and try again.")

    @app.context_processor
    def inject_globals():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(16)
        return {"csrf_token": session["csrf_token"], "current_user": g.get("user"),
                "ADMIN": ADMIN, "PHARMACIST": PHARMACIST, "today": today().isoformat()}

    def login_required(view):
        @wraps(view)
        def wrapped(*a, **kw):
            if g.user is None:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("login"))
            return view(*a, **kw)
        return wrapped

    def roles_required(*roles):
        def decorator(view):
            @wraps(view)
            def wrapped(*a, **kw):
                if g.user is None:
                    flash("Please log in to continue.", "warning")
                    return redirect(url_for("login"))
                if g.user["role"] not in roles:
                    abort(403)
                return view(*a, **kw)
            return wrapped
        return decorator

    # --------------------------------------------------------------- auth
    @app.route("/")
    def index():
        return redirect(url_for("dashboard" if g.user else "login"))

    @app.route("/login", methods=["GET", "POST"])
    @app.route("/login/<role>", methods=["GET", "POST"])
    def login(role=None):
        requested_role = role or request.args.get("role") or request.form.get("portal_role")
        if requested_role not in (ADMIN, PHARMACIST):
            requested_role = "admin"

        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if user and check_password_hash(user["password_hash"], password):
                portal_role = request.form.get("portal_role")
                if portal_role in (ADMIN, PHARMACIST) and user["role"] != portal_role:
                    flash(f"This account is registered as a {user['role'].capitalize()}. Please use the {user['role'].capitalize()} login tab.", "warning")
                    return render_template("login.html", active_role=user["role"])
                session.clear()  # new session on login
                session["user_id"] = user["user_id"]
                session.permanent = True
                flash(f"Welcome, {user['name']}.", "success")
                return redirect(url_for("dashboard"))
            flash("Invalid email or password.", "danger")  # same message for both cases
            return render_template("login.html", active_role=requested_role)
        return render_template("login.html", active_role=requested_role)

    @app.route("/download/report-pdf")
    def download_report_pdf():
        downloads_dir = os.path.join(app.root_path, "static", "downloads")
        return send_from_directory(downloads_dir, "SMART_PHARMACY_PROJECT_REPORT.pdf",
                                   as_attachment=True, download_name="SMART_PHARMACY_PROJECT_REPORT.pdf")

    @app.route("/download/report-docx")
    def download_report_docx():
        downloads_dir = os.path.join(app.root_path, "static", "downloads")
        return send_from_directory(downloads_dir, "SMART_PHARMACY_PROJECT_REPORT.docx",
                                   as_attachment=True, download_name="SMART_PHARMACY_PROJECT_REPORT.docx")

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        db = get_db()
        stats = rep.dashboard_stats(db)
        alerts = [r for r in inv.list_inventory(db)
                  if r["status"] in ("Expired", "Near Expiry", "Low Stock", "Out of Stock")]
        sales_by_medicine = rep.sales_per_medicine(db)
        return render_template("dashboard.html", stats=stats, alerts=alerts[:10],
                               sales_by_medicine=sales_by_medicine)

    # ----------------------------------------------------------- medicines
    @app.route("/medicines")
    @login_required
    def medicines():
        q = request.args.get("q", "")
        return render_template("medicines.html", medicines=inv.list_medicines(get_db(), q), q=q)

    @app.route("/medicines/<int:medicine_id>")
    @login_required
    def medicine_detail(medicine_id):
        db = get_db()
        med = inv.get_medicine(db, medicine_id)
        if med is None:
            abort(404)
        batches = [b for b in inv.list_inventory(db) if b["medicine_id"] == medicine_id]
        sales_summary = rep.medicine_sales_summary(db, medicine_id)
        return render_template("medicine_detail.html", med=med, batches=batches,
                               sales_summary=sales_summary)

    @app.route("/medicines/add", methods=["GET", "POST"])
    @roles_required(ADMIN, PHARMACIST)
    def medicine_add():
        if request.method == "POST":
            try:
                inv.add_medicine(get_db(), request.form)
                flash("Medicine added.", "success")
                return redirect(url_for("medicines"))
            except ServiceError as e:
                flash(str(e), "danger")
        return render_template("medicine_form.html", med=request.form, editing=False)

    @app.route("/medicines/<int:medicine_id>/edit", methods=["GET", "POST"])
    @roles_required(ADMIN, PHARMACIST)
    def medicine_edit(medicine_id):
        db = get_db()
        med = inv.get_medicine(db, medicine_id)
        if med is None:
            abort(404)
        if request.method == "POST":
            try:
                inv.update_medicine(db, medicine_id, request.form)
                flash("Medicine updated.", "success")
                return redirect(url_for("medicines"))
            except ServiceError as e:
                flash(str(e), "danger")
            med = request.form
        return render_template("medicine_form.html", med=med, editing=True,
                               medicine_id=medicine_id)

    # ----------------------------------------------------------- inventory
    @app.route("/inventory")
    @login_required
    def inventory():
        q = request.args.get("q", "")
        return render_template("inventory.html", items=inv.list_inventory(get_db(), q), q=q)

    @app.route("/inventory/add", methods=["GET", "POST"])
    @roles_required(ADMIN)
    def inventory_add():
        db = get_db()
        if request.method == "POST":
            try:
                inv.add_batch(db, request.form)
                flash("Batch added.", "success")
                return redirect(url_for("inventory"))
            except ServiceError as e:
                flash(str(e), "danger")
        return render_template("inventory_form.html", batch=request.form, editing=False,
                               medicines=inv.list_medicines(db))

    @app.route("/inventory/<int:inventory_id>/edit", methods=["GET", "POST"])
    @roles_required(ADMIN)
    def inventory_edit(inventory_id):
        db = get_db()
        batch = inv.get_batch(db, inventory_id)
        if batch is None:
            abort(404)
        if request.method == "POST":
            try:
                inv.update_batch(db, inventory_id, request.form)
                flash("Batch updated.", "success")
                return redirect(url_for("inventory"))
            except ServiceError as e:
                flash(str(e), "danger")
            batch = dict(request.form, medicine_name=batch["medicine_name"],
                         quantity=batch["quantity"])
        return render_template("inventory_form.html", batch=batch, editing=True,
                               inventory_id=inventory_id, medicines=[])

    # -------------------------------------------------------- transactions
    @app.route("/transactions")
    @roles_required(ADMIN, PHARMACIST)
    def transactions():
        kind = request.args.get("type", "")
        return render_template("transactions.html", rows=txn.list_transactions(get_db(), kind),
                               kind=kind)

    @app.route("/transactions/purchase", methods=["GET", "POST"])
    @roles_required(PHARMACIST)
    def purchase():
        db = get_db()
        if request.method == "POST":
            try:
                r = txn.record_purchase(db, g.user["user_id"], request.form)
                flash(f"Purchase recorded (total {r['total_amount']:.2f}). "
                      f"Updated stock: {r['new_quantity']}.", "success")
                return redirect(url_for("transactions"))
            except ServiceError as e:
                flash(str(e), "danger")
        batches = [b for b in inv.list_inventory(db) if b["status"] != "Expired"]
        return render_template("transaction_form.html", mode="purchase", form=request.form,
                               medicines=inv.list_medicines(db), batches=batches)

    @app.route("/transactions/sale", methods=["GET", "POST"])
    @roles_required(PHARMACIST)
    def sale():
        db = get_db()
        if request.method == "POST":
            try:
                r = txn.record_sale(db, g.user["user_id"], request.form)
                flash(f"Sale recorded (total {r['total_amount']:.2f}). "
                      f"Remaining stock: {r['new_quantity']}.", "success")
                return redirect(url_for("transactions"))
            except ServiceError as e:
                flash(str(e), "danger")
        batches = [b for b in inv.list_inventory(db)
                   if b["status"] != "Expired" and b["quantity"] > 0]
        return render_template("transaction_form.html", mode="sale", form=request.form,
                               medicines=[], batches=batches)

    # --------------------------------------------------------------- waste
    @app.route("/waste")
    @roles_required(ADMIN, PHARMACIST)
    def waste_list():
        db = get_db()
        return render_template("waste.html", records=waste.list_waste(db),
                               expired=waste.list_expired_batches(db))

    @app.route("/waste/add", methods=["GET", "POST"])
    @roles_required(PHARMACIST)
    def waste_add():
        db = get_db()
        if request.method == "POST":
            try:
                r = waste.record_waste(db, g.user["user_id"], request.form)
                flash(f"Waste recorded. Remaining stock: {r['new_quantity']}.", "success")
                return redirect(url_for("waste_list"))
            except ServiceError as e:
                flash(str(e), "danger")
        batches = [b for b in inv.list_inventory(db) if b["quantity"] > 0]
        return render_template("waste_form.html", form=request.form, batches=batches,
                               reasons=waste.WASTE_REASONS)

    # ------------------------------------------------------------- reports
    def _report_from_args():
        report_type = request.args.get("type", "")
        if not report_type:
            return None
        return rep.generate_report(get_db(), report_type, request.args.get("start"),
                                   request.args.get("end"))

    @app.route("/reports")
    @roles_required(ADMIN, PHARMACIST)
    def reports():
        report = None
        try:
            report = _report_from_args()
        except ServiceError as e:
            flash(str(e), "danger")
        return render_template("reports.html", report=report, types=rep.REPORT_TYPES,
                               args=request.args)

    @app.route("/reports/export")
    @roles_required(ADMIN, PHARMACIST)
    def reports_export():
        try:
            report = _report_from_args()
        except ServiceError as e:
            flash(str(e), "danger")
            return redirect(url_for("reports"))
        if report is None:
            flash("Choose a report type first.", "warning")
            return redirect(url_for("reports"))
        return Response(
            rep.report_to_csv(report), mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={report['type']}_report.csv"})

    # ------------------------------------------------------ error handlers
    @app.errorhandler(400)
    def bad_request(e):
        return render_template("error.html", code=400, message=e.description), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", code=403,
                               message="You do not have permission to do that."), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(e):
        # Details go to the log, never to the user.
        return render_template("error.html", code=500,
                               message="Something went wrong. Please try again."), 500

    return app


if __name__ == "__main__":
    # Development server only. Not suitable for real production use.
    port = int(os.environ.get("PORT", 5000))
    create_app().run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
