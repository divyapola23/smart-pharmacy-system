"""Reports. Every figure is computed from database rows (nothing hardcoded).

Definitions used in this project
  Total purchased quantity = SUM(quantity) of Purchase transactions in range
  Total sold quantity      = SUM(quantity) of Sale transactions in range
  Total wasted quantity    = SUM(quantity) of waste records in range
  Total purchase value     = SUM(total_amount) of Purchase transactions
  Total sales value        = SUM(total_amount) of Sale transactions
                             (this is revenue, NOT profit)
  Low-stock batch          = not expired AND quantity <= reorder_level
  Expired batch            = expiry_date earlier than today
"""
import csv
import io
from datetime import timedelta

from services.common import NEAR_EXPIRY_DAYS, ServiceError, parse_date, today
from services.inventory_service import list_inventory

REPORT_TYPES = {
    "inventory": "Current Inventory Report",
    "low_stock": "Low-Stock Report",
    "expiry": "Expiry Report",
    "purchases": "Purchase Transaction Report",
    "sales": "Sales Transaction Report",
    "waste": "Waste Report",
    "summary": "Summary Report",
    "sales_per_medicine": "Sales Count Per Medicine Report",
}

_DATE_FILTERED = {"purchases", "sales", "waste", "summary", "sales_per_medicine"}


def _scalar(conn, sql, params=()):
    return conn.execute(sql, params).fetchone()[0] or 0


def count_low_stock(conn, on=None):
    return _scalar(conn, "SELECT COUNT(*) FROM inventory WHERE expiry_date >= ? "
                         "AND quantity <= reorder_level", ((on or today()).isoformat(),))


def count_expired(conn, on=None):
    return _scalar(conn, "SELECT COUNT(*) FROM inventory WHERE expiry_date < ?",
                   ((on or today()).isoformat(),))


def count_near_expiry(conn, on=None):
    on = on or today()
    return _scalar(conn, "SELECT COUNT(*) FROM inventory WHERE expiry_date >= ? "
                         "AND expiry_date <= ? AND quantity > 0",
                   (on.isoformat(), (on + timedelta(days=NEAR_EXPIRY_DAYS)).isoformat()))


def dashboard_stats(conn, on=None):
    return {
        "medicines": _scalar(conn, "SELECT COUNT(*) FROM medicines"),
        "batches": _scalar(conn, "SELECT COUNT(*) FROM inventory"),
        "units_in_stock": _scalar(conn, "SELECT SUM(quantity) FROM inventory"),
        "low_stock": count_low_stock(conn, on),
        "near_expiry": count_near_expiry(conn, on),
        "expired": count_expired(conn, on),
    }


def sales_per_medicine(conn, start=None, end=None):
    """Return sales statistics (sales count, units sold, total revenue) for every medicine."""
    extra, params = _range_sql("t.transaction_date", start, end)
    rows = conn.execute(f"""
        SELECT 
            m.medicine_id,
            m.medicine_name,
            m.category,
            m.manufacturer,
            COUNT(t.transaction_id) AS sales_count,
            COALESCE(SUM(t.quantity), 0) AS total_units_sold,
            COALESCE(SUM(t.total_amount), 0.0) AS total_revenue
        FROM medicines m
        LEFT JOIN inventory i ON i.medicine_id = m.medicine_id
        LEFT JOIN transactions t ON t.inventory_id = i.inventory_id AND t.transaction_type = 'Sale'{extra}
        GROUP BY m.medicine_id, m.medicine_name, m.category, m.manufacturer
        ORDER BY total_units_sold DESC, sales_count DESC, m.medicine_name ASC
    """, params).fetchall()
    return [dict(r) for r in rows]


def medicine_sales_summary(conn, medicine_id):
    """Return sales summary for a single medicine."""
    row = conn.execute("""
        SELECT 
            COUNT(t.transaction_id) AS sales_count,
            COALESCE(SUM(t.quantity), 0) AS total_units_sold,
            COALESCE(SUM(t.total_amount), 0.0) AS total_revenue
        FROM inventory i
        JOIN transactions t ON t.inventory_id = i.inventory_id AND t.transaction_type = 'Sale'
        WHERE i.medicine_id = ?
    """, (medicine_id,)).fetchone()
    if row:
        return {
            "sales_count": row["sales_count"] or 0,
            "total_units_sold": row["total_units_sold"] or 0,
            "total_revenue": row["total_revenue"] or 0.0,
        }
    return {"sales_count": 0, "total_units_sold": 0, "total_revenue": 0.0}


def _validate_range(start, end):
    start = parse_date(start, "Start date", required=False)
    end = parse_date(end, "End date", required=False)
    if start and end and start > end:
        raise ServiceError("Start date cannot be after end date.")
    return start, end


def _range_sql(column, start, end):
    sql, params = "", []
    if start:
        sql += f" AND date({column}) >= ?"
        params.append(start)
    if end:
        sql += f" AND date({column}) <= ?"
        params.append(end)
    return sql, params


def _txn_report(conn, kind, start, end):
    extra, params = _range_sql("t.transaction_date", start, end)
    rows = conn.execute(
        "SELECT t.transaction_id, t.transaction_date, m.medicine_name, i.batch_no, "
        "t.quantity, t.unit_price, t.total_amount, u.name AS recorded_by "
        "FROM transactions t JOIN inventory i ON i.inventory_id = t.inventory_id "
        "JOIN medicines m ON m.medicine_id = i.medicine_id "
        "JOIN users u ON u.user_id = t.user_id "
        "WHERE t.transaction_type = ?" + extra + " ORDER BY t.transaction_id",
        [kind] + params).fetchall()
    rows = [list(r) for r in rows]
    label = "purchased" if kind == "Purchase" else "sold"
    value_label = "Total purchase value" if kind == "Purchase" else "Total sales value"
    return {
        "columns": ["Txn ID", "Date", "Medicine", "Batch", "Qty", "Unit Price",
                    "Total", "Recorded By"],
        "rows": rows,
        "totals": [(f"Total quantity {label}", sum(r[4] for r in rows)),
                   (value_label, round(sum(r[6] for r in rows), 2))],
    }


def generate_report(conn, report_type, start=None, end=None, on=None):
    """Return {title, columns, rows, totals, start, end}. rows is a list of lists."""
    if report_type not in REPORT_TYPES:
        raise ServiceError("Please choose a valid report type.")
    start, end = _validate_range(start, end)
    on = on or today()
    report = {"type": report_type, "title": REPORT_TYPES[report_type],
              "start": start, "end": end, "generated": on.isoformat()}

    if report_type == "inventory":
        items = list_inventory(conn, on=on)
        report["columns"] = ["Inv ID", "Medicine", "Batch", "Qty", "Reorder Lvl",
                             "Purchase Price", "Selling Price", "Expiry", "Status"]
        report["rows"] = [[r["inventory_id"], r["medicine_name"], r["batch_no"], r["quantity"],
                           r["reorder_level"], r["purchase_price"], r["selling_price"],
                           r["expiry_date"], r["status"]] for r in items]
        report["totals"] = [("Number of batches", len(items)),
                            ("Total units in stock", sum(r["quantity"] for r in items)),
                            ("Low-stock batches", count_low_stock(conn, on)),
                            ("Expired batches", count_expired(conn, on))]

    elif report_type == "low_stock":
        items = [r for r in list_inventory(conn, on=on) if r["status"] in ("Low Stock", "Out of Stock")]
        report["columns"] = ["Inv ID", "Medicine", "Batch", "Qty", "Reorder Lvl", "Expiry"]
        report["rows"] = [[r["inventory_id"], r["medicine_name"], r["batch_no"], r["quantity"],
                           r["reorder_level"], r["expiry_date"]] for r in items]
        report["totals"] = [("Low-stock batches", len(items))]

    elif report_type == "expiry":
        limit = (on + timedelta(days=NEAR_EXPIRY_DAYS)).isoformat()
        rows = conn.execute(
            "SELECT i.inventory_id, m.medicine_name, i.batch_no, i.quantity, i.expiry_date "
            "FROM inventory i JOIN medicines m ON m.medicine_id = i.medicine_id "
            "WHERE i.expiry_date <= ? AND i.quantity > 0 ORDER BY i.expiry_date", (limit,)).fetchall()
        report["columns"] = ["Inv ID", "Medicine", "Batch", "Qty", "Expiry", "Status"]
        report["rows"] = [[r[0], r[1], r[2], r[3], r[4],
                          "Expired" if r[4] < on.isoformat() else "Near Expiry"] for r in rows]
        report["totals"] = [("Expired batches with stock", sum(1 for r in report["rows"] if r[5] == "Expired")),
                            ("Near-expiry batches", sum(1 for r in report["rows"] if r[5] == "Near Expiry"))]

    elif report_type in ("purchases", "sales"):
        report.update(_txn_report(conn, "Purchase" if report_type == "purchases" else "Sale", start, end))

    elif report_type == "waste":
        extra, params = _range_sql("w.disposal_date", start, end)
        rows = conn.execute(
            "SELECT w.waste_id, w.disposal_date, m.medicine_name, i.batch_no, w.quantity, "
            "w.reason, u.name FROM waste_records w "
            "JOIN inventory i ON i.inventory_id = w.inventory_id "
            "JOIN medicines m ON m.medicine_id = i.medicine_id "
            "JOIN users u ON u.user_id = w.user_id WHERE 1=1" + extra + " ORDER BY w.waste_id",
            params).fetchall()
        report["columns"] = ["Waste ID", "Disposal Date", "Medicine", "Batch", "Qty", "Reason", "Recorded By"]
        report["rows"] = [list(r) for r in rows]
        report["totals"] = [("Total wasted quantity", sum(r[4] for r in rows)),
                            ("Waste records", len(rows))]

    elif report_type == "sales_per_medicine":
        med_sales = sales_per_medicine(conn, start, end)
        report["columns"] = ["Medicine ID", "Medicine Name", "Category", "Manufacturer",
                             "Sales Count (Txns)", "Units Sold", "Total Revenue"]
        report["rows"] = [[r["medicine_id"], r["medicine_name"], r["category"] or "-",
                           r["manufacturer"] or "-", r["sales_count"], r["total_units_sold"],
                           round(r["total_revenue"], 2)] for r in med_sales]
        report["totals"] = [
            ("Total sales transactions", sum(r["sales_count"] for r in med_sales)),
            ("Total units sold", sum(r["total_units_sold"] for r in med_sales)),
            ("Total sales revenue", round(sum(r["total_revenue"] for r in med_sales), 2)),
        ]

    else:  # summary
        def txn_sum(kind, col):
            extra, params = _range_sql("transaction_date", start, end)
            return _scalar(conn, f"SELECT SUM({col}) FROM transactions "
                                 f"WHERE transaction_type = ?{extra}", [kind] + params)
        extra, params = _range_sql("disposal_date", start, end)
        wasted = _scalar(conn, f"SELECT SUM(quantity) FROM waste_records WHERE 1=1{extra}", params)
        report["columns"] = ["Metric", "Value", "Definition"]
        report["rows"] = [
            ["Total purchased quantity", txn_sum("Purchase", "quantity"), "Units bought in range"],
            ["Total sold quantity", txn_sum("Sale", "quantity"), "Units sold in range"],
            ["Total wasted quantity", wasted, "Units written off in range"],
            ["Total purchase value", round(txn_sum("Purchase", "total_amount"), 2), "Money spent on purchases"],
            ["Total sales value", round(txn_sum("Sale", "total_amount"), 2), "Money received from sales (not profit)"],
            ["Low-stock batches (now)", count_low_stock(conn, on), "Not expired, qty <= reorder level"],
            ["Expired batches (now)", count_expired(conn, on), "Expiry date before today"],
        ]
        report["totals"] = []

    # Whether the table is empty (summary always shows its metric rows).
    report["empty"] = not report["rows"]
    report["date_filtered"] = report_type in _DATE_FILTERED
    return report


def report_to_csv(report):
    """Render a report dict as CSV text (header, rows, then totals)."""
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow([report["title"]])
    if report.get("start") or report.get("end"):
        w.writerow(["Date range", report.get("start") or "", report.get("end") or ""])
    w.writerow(report["columns"])
    for row in report["rows"]:
        w.writerow([_safe_cell(c) for c in row])
    for label, value in report["totals"]:
        w.writerow([label, value])
    return out.getvalue()


def _safe_cell(value):
    """Stop spreadsheet formula injection: text starting with = + - @ is prefixed."""
    if isinstance(value, str) and value[:1] in ("=", "+", "-", "@"):
        return "'" + value
    return value
