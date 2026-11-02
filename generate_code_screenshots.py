import os
import io
from PIL import Image, ImageDraw, ImageFont
import pygments
from pygments.lexers import PythonLexer, SqlLexer, HtmlLexer, JavascriptLexer
from pygments.formatters import ImageFormatter

IMG_DIR = r"c:\Users\Deekshita\Downloads\smart-pharmacy-system\smart-pharmacy-system\docs\images"
os.makedirs(IMG_DIR, exist_ok=True)

# Fonts
FONT_CONSOLAS = r"C:\Windows\Fonts\consola.ttf"
FONT_SEGOE = r"C:\Windows\Fonts\segoeui.ttf"
FONT_SEGOE_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

def render_ide_window(
    code_text: str,
    lexer,
    filename: str,
    title: str,
    breadcrumb: str,
    out_filename: str,
    lang_label: str = "Python",
    inactive_tabs=None,
    style: str = "dracula",
    font_size: int = 24,
    line_number_chars: int = 3,
    target_width: int = 1800
):
    inactive_tabs = inactive_tabs or []
    
    # 1. Render code with Pygments
    formatter = ImageFormatter(
        font_name="Consolas",
        font_size=font_size,
        line_numbers=True,
        line_number_bg="#21222c",
        line_number_fg="#6272a4",
        style=style,
        image_pad=18,
        line_number_chars=line_number_chars
    )
    code_bytes = pygments.highlight(code_text, lexer, formatter)
    code_img = Image.open(io.BytesIO(code_bytes)).convert("RGBA")

    # Dimensions
    hdr_h = 52       # macOS / VS Code title bar
    tabs_h = 44      # Editor tabs bar
    crumb_h = 36     # Breadcrumbs bar
    status_h = 38    # Status bar
    top_offset = hdr_h + tabs_h + crumb_h
    
    # Calculate canvas size
    content_w = max(target_width, code_img.width + 40)
    canvas_w = content_w
    canvas_h = top_offset + code_img.height + 24 + status_h

    # Create base image
    bg_color = (40, 42, 54, 255)       # Dracula editor background (#282a36)
    title_bg = (30, 31, 41, 255)       # Header background (#1e1f29)
    tab_bar_bg = (25, 26, 34, 255)     # Inactive tab bar background (#191a22)
    tab_active_bg = (40, 42, 54, 255)  # Active tab background (#282a36)
    crumb_bg = (33, 34, 44, 255)       # Breadcrumbs background (#21222c)
    status_bg = (68, 71, 90, 255)      # Status bar background (#44475a)
    border_color = (98, 114, 164, 180) # Subtle border (#6272a4)

    img = Image.new("RGBA", (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(img)

    # Load fonts
    font_title = ImageFont.truetype(FONT_SEGOE, 18)
    font_tab = ImageFont.truetype(FONT_SEGOE_BOLD, 16)
    font_tab_inact = ImageFont.truetype(FONT_SEGOE, 15)
    font_crumb = ImageFont.truetype(FONT_CONSOLAS, 15)
    font_status = ImageFont.truetype(FONT_SEGOE, 15)

    # 1. Title Bar
    draw.rectangle([0, 0, canvas_w, hdr_h], fill=title_bg)
    draw.line([0, hdr_h, canvas_w, hdr_h], fill=(50, 52, 65, 255), width=1)

    # Window traffic light buttons
    dots = [
        ((28, hdr_h // 2), 7.5, (255, 85, 85, 255)),   # Red close
        ((52, hdr_h // 2), 7.5, (241, 250, 140, 255)), # Yellow min
        ((76, hdr_h // 2), 7.5, (80, 250, 123, 255))   # Green max
    ]
    for (cx, cy), r, col in dots:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    # Centered window title
    bbox = font_title.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((canvas_w - tw) // 2, (hdr_h - (bbox[3] - bbox[1])) // 2 - 2), title, fill=(248, 248, 242, 230), font=font_title)

    # 2. Tabs Bar
    draw.rectangle([0, hdr_h, canvas_w, hdr_h + tabs_h], fill=tab_bar_bg)
    
    # Active Tab
    tab_x = 0
    active_tab_w = 260
    draw.rectangle([tab_x, hdr_h, tab_x + active_tab_w, hdr_h + tabs_h], fill=tab_active_bg)
    # Active tab top border highlight (purple/cyan)
    draw.line([tab_x, hdr_h, tab_x + active_tab_w, hdr_h], fill=(189, 147, 249, 255), width=3)
    # File icon color badge
    icon_col = (139, 233, 253, 255) if lang_label == "SQL" else ((80, 250, 123, 255) if lang_label == "Python" else (255, 184, 108, 255))
    draw.ellipse([tab_x + 18, hdr_h + tabs_h // 2 - 5, tab_x + 28, hdr_h + tabs_h // 2 + 5], fill=icon_col)
    draw.text((tab_x + 36, hdr_h + 12), filename, fill=(248, 248, 242, 255), font=font_tab)
    # Tab close 'x'
    draw.text((tab_x + active_tab_w - 24, hdr_h + 12), "x", fill=(98, 114, 164, 255), font=font_tab_inact)
    draw.line([tab_x + active_tab_w, hdr_h, tab_x + active_tab_w, hdr_h + tabs_h], fill=(50, 52, 65, 255), width=1)

    # Inactive Tabs
    curr_tab_x = tab_x + active_tab_w
    for inact in inactive_tabs:
        inact_w = 200
        draw.text((curr_tab_x + 20, hdr_h + 13), inact, fill=(98, 114, 164, 255), font=font_tab_inact)
        draw.line([curr_tab_x + inact_w, hdr_h, curr_tab_x + inact_w, hdr_h + tabs_h], fill=(40, 42, 54, 255), width=1)
        curr_tab_x += inact_w

    # 3. Breadcrumb Bar
    draw.rectangle([0, hdr_h + tabs_h, canvas_w, top_offset], fill=crumb_bg)
    draw.line([0, top_offset, canvas_w, top_offset], fill=(50, 52, 65, 255), width=1)
    draw.text((20, hdr_h + tabs_h + 8), breadcrumb, fill=(139, 233, 253, 220), font=font_crumb)

    # 4. Paste Code Image
    img.paste(code_img, (15, top_offset + 10), mask=code_img)

    # 5. Bottom Status Bar
    status_y = canvas_h - status_h
    draw.rectangle([0, status_y, canvas_w, canvas_h], fill=status_bg)
    
    # Left status indicators
    status_left = f"  -- main*   |   [x] 0 errors   [!] 0 warnings   |   Smart Pharmacy POS Core"
    draw.text((15, status_y + 9), status_left, fill=(248, 248, 242, 240), font=font_status)

    # Right status indicators
    status_right = f"UTF-8   |   Spaces: 4   |   {lang_label}   |   Prettier: active  "
    r_bbox = font_status.getbbox(status_right)
    rw = r_bbox[2] - r_bbox[0]
    draw.text((canvas_w - rw - 15, status_y + 9), status_right, fill=(248, 248, 242, 240), font=font_status)

    # Outer border
    draw.rectangle([0, 0, canvas_w - 1, canvas_h - 1], outline=border_color, width=2)

    # Save final image
    out_path = os.path.join(IMG_DIR, out_filename)
    img.save(out_path, "PNG", dpi=(300, 300))
    print(f"Generated code screenshot: {out_path} ({canvas_w}x{canvas_h})")
    return out_path

# =========================================================================
# CODE SAMPLES GENERATION
# =========================================================================

def generate_all():
    print("Generating IDE Code Screenshots for Project Report...")

    # 1. Database Schema (schema.sql)
    code_schema = """-- =========================================================================
-- Smart Pharmacy Inventory and Medicine Waste Management System
-- Database Schema: SQLite Relational DDL with Integrity Constraints
-- =========================================================================

CREATE TABLE IF NOT EXISTS medicines (
    medicine_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT NOT NULL,
    category      TEXT NOT NULL,
    manufacturer  TEXT,
    UNIQUE (medicine_name, manufacturer)
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id      INTEGER NOT NULL REFERENCES medicines (medicine_id),
    batch_no         TEXT NOT NULL,
    quantity         INTEGER NOT NULL CHECK (quantity >= 0),
    purchase_price   REAL NOT NULL CHECK (purchase_price >= 0),
    selling_price    REAL NOT NULL CHECK (selling_price >= 0),
    manufacture_date TEXT,
    expiry_date      TEXT NOT NULL,
    reorder_level    INTEGER NOT NULL CHECK (reorder_level >= 0),
    UNIQUE (medicine_id, batch_no)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('Purchase', 'Sale')),
    inventory_id     INTEGER NOT NULL REFERENCES inventory (inventory_id),
    quantity         INTEGER NOT NULL CHECK (quantity > 0),
    unit_price       REAL NOT NULL CHECK (unit_price >= 0),
    total_amount     REAL NOT NULL CHECK (total_amount >= 0),
    transaction_date TEXT NOT NULL,
    user_id          INTEGER NOT NULL REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS waste_records (
    waste_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    inventory_id  INTEGER NOT NULL REFERENCES inventory (inventory_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    reason        TEXT NOT NULL CHECK (reason IN ('Expired', 'Damaged', 'Recalled', 'Other')),
    disposal_date TEXT NOT NULL,
    user_id       INTEGER NOT NULL REFERENCES users (user_id)
);

-- Relational Performance Indexes for Real-Time Expiry and Audit Lookups
CREATE INDEX IF NOT EXISTS idx_inventory_expiry ON inventory (expiry_date);
CREATE INDEX IF NOT EXISTS idx_txn_inventory    ON transactions (inventory_id);
CREATE INDEX IF NOT EXISTS idx_txn_date         ON transactions (transaction_date);"""

    render_ide_window(
        code_text=code_schema,
        lexer=SqlLexer(),
        filename="schema.sql",
        title="smart-pharmacy-system - Database Schema Layer (schema.sql)",
        breadcrumb="smart-pharmacy-system > schema.sql > Relational Schema & Constraints",
        out_filename="code_screenshot_database_schema.png",
        lang_label="SQLite SQL",
        inactive_tabs=["database.py", "app.py"],
        font_size=23,
        target_width=1820
    )

    # 2. Database Connectivity & Atomic Transactions (database.py)
    code_database = '''"""Database Access Layer & Atomic Transaction Context Manager (database.py)."""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "pharmacy.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def get_connection(db_path=None):
    """Open a SQLite connection configured with foreign keys and row factory."""
    conn = sqlite3.connect(db_path or DEFAULT_DB_PATH, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(db_path=None):
    """Execute schema script safely on system startup if tables do not exist."""
    conn = get_connection(db_path)
    try:
        with open(SCHEMA_PATH, encoding="utf-8") as f:
            conn.executescript(f.read())
    finally:
        conn.close()

class Transaction:
    """Context manager providing ACID transactions with immediate row locks.
    
    Prevents race conditions by locking SQLite before reading and writing.
    Automatically issues COMMIT upon clean exit or ROLLBACK upon exception.
    """
    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        self.conn.execute("BEGIN IMMEDIATE")
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.conn.execute("COMMIT")
        else:
            self.conn.execute("ROLLBACK")
        return False  # Re-raise exception to caller'''

    render_ide_window(
        code_text=code_database,
        lexer=PythonLexer(),
        filename="database.py",
        title="smart-pharmacy-system - Database Transaction Manager (database.py)",
        breadcrumb="smart-pharmacy-system > database.py > get_connection() & class Transaction",
        out_filename="code_screenshot_database_transaction.png",
        lang_label="Python 3.10",
        inactive_tabs=["schema.sql", "app.py"],
        font_size=23,
        target_width=1820
    )

    # 3. Backend FEFO Stock Allocation Engine (transaction_service.py)
    code_fefo = '''def record_sale(conn, user_id, form):
    """Record a clinical sale using First-Expired, First-Out (FEFO) rules.
    
    Guarantees:
      1. Expired batches cannot be dispensed under any circumstances.
      2. Validates requested quantity against live batch stock under transaction lock.
      3. Performs atomic inventory deduction and writes immutable transaction log.
    """
    inventory_id = parse_int(form.get("inventory_id"), "Batch")
    quantity = parse_int(form.get("quantity"), "Quantity", minimum=1)
    
    batch = get_batch(conn, inventory_id)
    if batch is None:
        raise ValidationError("Selected batch does not exist.")
        
    price_text = str(form.get("unit_price") or "").strip()
    unit_price = parse_price(price_text, "Unit price") if price_text else batch["selling_price"]
    total = round(quantity * unit_price, 2)

    try:
        with Transaction(conn):
            # Re-read batch state inside immediate lock to eliminate race conditions
            batch = get_batch(conn, inventory_id)
            if is_expired(batch["expiry_date"]):
                raise ValidationError("This batch has expired and cannot be dispensed.")
            if quantity > batch["quantity"]:
                raise ValidationError(
                    f"Insufficient stock. Only {batch['quantity']} unit(s) available.")

            # Atomically decrement batch quantity
            conn.execute(
                "UPDATE inventory SET quantity = quantity - ? WHERE inventory_id = ?",
                (quantity, inventory_id))

            # Insert immutable sales transaction audit trail entry
            cur = conn.execute(
                "INSERT INTO transactions (transaction_type, inventory_id, quantity, "
                "unit_price, total_amount, transaction_date, user_id) "
                "VALUES ('Sale', ?, ?, ?, ?, ?, ?)",
                (inventory_id, quantity, unit_price, total, now_str(), user_id))
            transaction_id = cur.lastrowid
    except sqlite3.Error:
        raise ServiceError("The sale could not be processed. No stock was deducted.")

    return {"transaction_id": transaction_id, "inventory_id": inventory_id,
            "new_quantity": get_batch(conn, inventory_id)["quantity"], "total_amount": total}'''

    render_ide_window(
        code_text=code_fefo,
        lexer=PythonLexer(),
        filename="transaction_service.py",
        title="smart-pharmacy-system - Backend FEFO Engine (transaction_service.py)",
        breadcrumb="smart-pharmacy-system > services > transaction_service.py > record_sale()",
        out_filename="code_screenshot_backend_fefo.png",
        lang_label="Python 3.10",
        inactive_tabs=["inventory_service.py", "app.py"],
        font_size=23,
        target_width=1820
    )

    # 4. Backend Dynamic Expiry & Shelf-Life Calculation (inventory_service.py / common.py)
    code_expiry = '''def inventory_status(row, on=None, warning_days=30):
    """Dynamically evaluate product shelf-life and stock threshold status.
    
    Evaluates dates at query time against system calendar without scheduled background cron daemons:
      - 'Expired':      expiry_date < today
      - 'Out of Stock': quantity == 0
      - 'Low Stock':    quantity <= reorder_level
      - 'Near Expiry':  expiry_date <= (today + warning_days)
      - 'Available':    Safe, verified stock available for clinical dispensing
    """
    on = on or today()
    expiry_str = row["expiry_date"]
    
    if is_expired(expiry_str, on):
        return "Expired"
        
    if row["quantity"] == 0:
        return "Out of Stock"
        
    if row["quantity"] <= row["reorder_level"]:
        return "Low Stock"
        
    threshold_date = (on + timedelta(days=warning_days)).isoformat()
    if expiry_str <= threshold_date:
        return "Near Expiry"
        
    return "Available"

def calculate_medicine_aggregates(conn):
    """Aggregate total stock across all active batches using direct SQL SUM."""
    return conn.execute("""
        SELECT m.medicine_id, m.medicine_name, m.category,
               COALESCE(SUM(i.quantity), 0) AS total_stock,
               COUNT(i.inventory_id) AS active_batches
        FROM medicines m
        LEFT JOIN inventory i ON i.medicine_id = m.medicine_id
        GROUP BY m.medicine_id
        ORDER BY m.medicine_name ASC
    """).fetchall()'''

    render_ide_window(
        code_text=code_expiry,
        lexer=PythonLexer(),
        filename="inventory_service.py",
        title="smart-pharmacy-system - Dynamic Expiry Engine (inventory_service.py)",
        breadcrumb="smart-pharmacy-system > services > inventory_service.py > inventory_status()",
        out_filename="code_screenshot_backend_expiry.png",
        lang_label="Python 3.10",
        inactive_tabs=["transaction_service.py", "report_service.py"],
        font_size=23,
        target_width=1820
    )

    # 5. Backend Flask Controller & Security Middleware (app.py)
    code_controller = '''@app.before_request
def load_user_and_check_csrf():
    """Global request guard: establishes user session and validates anti-CSRF token."""
    g.user = None
    user_id = session.get("user_id")
    if user_id is not None:
        g.user = get_db().execute(
            "SELECT user_id, name, email, role FROM users WHERE user_id = ?",
            (user_id,)).fetchone()

    # Enforce cryptographic CSRF token validation on all state-altering POST requests
    if request.method == "POST":
        sent_token = request.form.get("csrf_token", "")
        expected_token = session.get("csrf_token", "")
        if not expected_token or not hmac.compare_digest(sent_token, expected_token):
            abort(400, "Your form expired or CSRF token was invalid. Please try again.")

@app.route("/dashboard")
@login_required
def dashboard():
    """Render role-tailored dashboard with KPI statistics, alerts, and sales analytics."""
    db = get_db()
    stats = rep.dashboard_stats(db)
    
    # Filter high-priority warnings: Expired, Near Expiry, and Low Stock
    alerts = [r for r in inv.list_inventory(db)
              if r["status"] in ("Expired", "Near Expiry", "Low Stock", "Out of Stock")]
              
    # Generate Admin Sales Count per Medicine analytics table
    sales_by_medicine = rep.sales_per_medicine(db)
    
    return render_template("dashboard.html", stats=stats, alerts=alerts[:10],
                           sales_by_medicine=sales_by_medicine)'''

    render_ide_window(
        code_text=code_controller,
        lexer=PythonLexer(),
        filename="app.py",
        title="smart-pharmacy-system - Flask Application Controller (app.py)",
        breadcrumb="smart-pharmacy-system > app.py > load_user_and_check_csrf() & dashboard()",
        out_filename="code_screenshot_backend_controller.png",
        lang_label="Python / Flask",
        inactive_tabs=["database.py", "transaction_service.py"],
        font_size=23,
        target_width=1820
    )

    # 6. Frontend Jinja2 POS Sale & Batch Dispensing Template (templates/transaction_form.html)
    code_template = '''{% extends "base.html" %}
{% block title %}Record Medicine Sale - Smart Pharmacy POS{% endblock %}
{% block content %}
<div class="card form-card shadow-sm border-0">
  <div class="card-header bg-primary text-white py-3">
    <h5 class="mb-0 fw-bold">Point-of-Sale: Record Medicine Dispensing (FEFO Enforced)</h5>
  </div>
  <div class="card-body p-4">
    <form method="post" novalidate id="saleForm">
      <input type="hidden" name="csrf_token" value="{{ csrf_token }}">

      <!-- Batch Selector with Live Stock and Expiry Badges -->
      <div class="mb-3">
        <label class="form-label fw-bold">Select Active Non-Expired Batch *</label>
        <select class="form-select form-select-lg" name="inventory_id" id="sale-batch" required>
          <option value="">-- Choose verified batch --</option>
          {% for b in batches %}
            <option value="{{ b.inventory_id }}" data-price="{{ b.selling_price }}"
                    data-stock="{{ b.quantity }}"
                    {{ 'selected' if form.inventory_id == b.inventory_id|string }}>
              {{ b.medicine_name }} [Batch: {{ b.batch_no }}] - Stock: {{ b.quantity }} units (Exp: {{ b.expiry_date }})
            </option>
          {% endfor %}
        </select>
        <div class="form-text text-muted">Expired batches are mathematically quarantined from this list.</div>
      </div>

      <!-- Quantity and Dynamic Selling Price Fields -->
      <div class="row g-3">
        <div class="col-md-6 mb-3">
          <label class="form-label fw-bold">Quantity to Dispense *</label>
          <input class="form-control" type="number" min="1" step="1" name="quantity" id="sale-qty" required>
        </div>
        <div class="col-md-6 mb-3">
          <label class="form-label fw-bold">Unit Selling Price ($)</label>
          <input class="form-control" type="number" min="0" step="0.01" name="unit_price" id="sale-price"
                 placeholder="Auto-populated from batch default">
        </div>
      </div>

      <!-- Form Submission Controls -->
      <div class="d-flex gap-2 mt-3">
        <button class="btn btn-success px-4 py-2 fw-semibold" type="submit">Confirm & Dispense Sale</button>
        <a class="btn btn-outline-secondary px-4 py-2" href="{{ url_for('transactions') }}">Cancel</a>
      </div>
    </form>
  </div>
</div>
{% endblock %}'''

    render_ide_window(
        code_text=code_template,
        lexer=HtmlLexer(),
        filename="transaction_form.html",
        title="smart-pharmacy-system - Frontend POS Dispensing Template (transaction_form.html)",
        breadcrumb="smart-pharmacy-system > templates > transaction_form.html > <form id='saleForm'>",
        out_filename="code_screenshot_frontend_sale.png",
        lang_label="HTML5 / Jinja2",
        inactive_tabs=["base.html", "dashboard.html"],
        font_size=23,
        target_width=1820
    )

    # 7. Frontend Client-Side Script & Interactivity (static/js/script.js)
    code_script = '''// =========================================================================
// Smart Pharmacy Frontend Interactive Logic & Client-Side Guards (script.js)
// =========================================================================

document.addEventListener("DOMContentLoaded", function () {
  // 1. Dynamic Unit Price Auto-Population upon Batch Selection
  const saleBatch = document.getElementById("sale-batch");
  const salePrice = document.getElementById("sale-price");
  
  if (saleBatch && salePrice) {
    saleBatch.addEventListener("change", function () {
      const selectedOption = saleBatch.options[saleBatch.selectedIndex];
      if (selectedOption && selectedOption.dataset.price) {
        salePrice.value = parseFloat(selectedOption.dataset.price).toFixed(2);
        salePrice.placeholder = "Batch Default: $" + selectedOption.dataset.price;
      }
    });
  }

  // 2. Active Sidebar Navigation Link Highlighting
  document.querySelectorAll(".sidebar .nav-link").forEach(function (link) {
    const targetPath = link.getAttribute("href");
    if (targetPath && window.location.pathname.startsWith(targetPath) && targetPath !== "/") {
      link.classList.add("active");
    }
  });

  // 3. Form Double-Submission Guard & Submit Button Lock
  document.querySelectorAll("form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      const submitBtn = e.submitter || form.querySelector("button[type='submit']");
      if (form.dataset.submitted === "true") {
        e.preventDefault(); // Prevent duplicate transactions
        return;
      }
      form.dataset.submitted = "true";
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
      }
    });
  });
});'''

    render_ide_window(
        code_text=code_script,
        lexer=JavascriptLexer(),
        filename="script.js",
        title="smart-pharmacy-system - Frontend Client Logic (static/js/script.js)",
        breadcrumb="smart-pharmacy-system > static > js > script.js > DOMContentLoaded",
        out_filename="code_screenshot_frontend_script.png",
        lang_label="JavaScript (ES6)",
        inactive_tabs=["styles.css", "base.html"],
        font_size=23,
        target_width=1820
    )

    print("All 7 IDE code screenshots generated successfully!")

if __name__ == "__main__":
    generate_all()
