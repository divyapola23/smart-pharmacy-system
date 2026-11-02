"""Medicine and inventory (batch) operations.

Medicine details live in `medicines`; batch details (quantity, expiry, prices)
live in `inventory`. Quantity is NOT edited directly: it changes only through
purchases, sales and waste records, so every change leaves a history entry.
(Opening stock entered when a batch is first added is the one exception.)
"""
import sqlite3
from datetime import timedelta

from database import Transaction
from services.common import (
    NEAR_EXPIRY_DAYS, ServiceError, ValidationError, clean_text, is_expired,
    parse_date, parse_int, parse_price, today,
)

# ----------------------------------------------------------------- status

def inventory_status(row, on=None):
    """Return one status label for an inventory row (dict-like)."""
    on = on or today()
    if is_expired(row["expiry_date"], on):
        return "Expired"
    if row["quantity"] == 0:
        return "Out of Stock"
    if row["quantity"] <= row["reorder_level"]:
        return "Low Stock"
    if row["expiry_date"] <= (on + timedelta(days=NEAR_EXPIRY_DAYS)).isoformat():
        return "Near Expiry"
    return "Available"


# --------------------------------------------------------------- medicines

def _medicine_fields(form):
    return (
        clean_text(form.get("medicine_name"), "Medicine name"),
        clean_text(form.get("category"), "Category", required=False),
        clean_text(form.get("manufacturer"), "Manufacturer", required=False),
    )


def add_medicine(conn, form):
    name, category, manufacturer = _medicine_fields(form)
    dup = conn.execute(
        "SELECT 1 FROM medicines WHERE lower(medicine_name) = lower(?) "
        "AND lower(COALESCE(manufacturer, '')) = lower(?)",
        (name, manufacturer or ""),
    ).fetchone()
    if dup:
        raise ValidationError("This medicine already exists for that manufacturer.")
    try:
        with Transaction(conn):
            cur = conn.execute(
                "INSERT INTO medicines (medicine_name, category, manufacturer) VALUES (?, ?, ?)",
                (name, category, manufacturer),
            )
        return cur.lastrowid
    except sqlite3.Error:
        raise ServiceError("Could not save the medicine. Please try again.")


def update_medicine(conn, medicine_id, form):
    if get_medicine(conn, medicine_id) is None:
        raise ValidationError("Medicine not found.")
    name, category, manufacturer = _medicine_fields(form)
    dup = conn.execute(
        "SELECT 1 FROM medicines WHERE lower(medicine_name) = lower(?) "
        "AND lower(COALESCE(manufacturer, '')) = lower(?) AND medicine_id != ?",
        (name, manufacturer or "", medicine_id),
    ).fetchone()
    if dup:
        raise ValidationError("Another medicine with this name and manufacturer exists.")
    try:
        with Transaction(conn):
            conn.execute(
                "UPDATE medicines SET medicine_name=?, category=?, manufacturer=? WHERE medicine_id=?",
                (name, category, manufacturer, medicine_id),
            )
    except sqlite3.Error:
        raise ServiceError("Could not update the medicine. Please try again.")


def get_medicine(conn, medicine_id):
    return conn.execute(
        "SELECT * FROM medicines WHERE medicine_id = ?", (medicine_id,)
    ).fetchone()


def list_medicines(conn, search=""):
    search = (search or "").strip()
    if not search:
        return conn.execute("SELECT * FROM medicines ORDER BY medicine_name").fetchall()
    like = f"%{search}%"
    if search.isdigit():
        return conn.execute(
            "SELECT * FROM medicines WHERE medicine_id = ? OR medicine_name LIKE ? "
            "ORDER BY medicine_name", (int(search), like)).fetchall()
    return conn.execute(
        "SELECT * FROM medicines WHERE medicine_name LIKE ? ORDER BY medicine_name",
        (like,)).fetchall()


# --------------------------------------------------------------- inventory

def _batch_fields(form, medicine_required=True):
    """Validate the fields shared by add / edit batch forms."""
    batch_no = clean_text(form.get("batch_no"), "Batch number", max_len=50)
    purchase_price = parse_price(form.get("purchase_price"), "Purchase price")
    selling_price = parse_price(form.get("selling_price"), "Selling price")
    manufacture = parse_date(form.get("manufacture_date"), "Manufacture date", required=False)
    expiry = parse_date(form.get("expiry_date"), "Expiry date")
    reorder = parse_int(form.get("reorder_level"), "Reorder level", minimum=0)
    if manufacture and manufacture >= expiry:
        raise ValidationError("Expiry date must be after the manufacture date.")
    return batch_no, purchase_price, selling_price, manufacture, expiry, reorder


def add_batch(conn, form):
    """Add a new batch with opening stock for an existing medicine."""
    medicine_id = parse_int(form.get("medicine_id"), "Medicine")
    if get_medicine(conn, medicine_id) is None:
        raise ValidationError("Selected medicine does not exist.")
    batch_no, pp, sp, mfg, exp, reorder = _batch_fields(form)
    quantity = parse_int(form.get("quantity"), "Quantity", minimum=0)
    if conn.execute("SELECT 1 FROM inventory WHERE medicine_id=? AND batch_no=?",
                    (medicine_id, batch_no)).fetchone():
        raise ValidationError(
            "This batch already exists for the medicine. Record a purchase to add stock to it.")
    try:
        with Transaction(conn):
            cur = conn.execute(
                "INSERT INTO inventory (medicine_id, batch_no, quantity, purchase_price, "
                "selling_price, manufacture_date, expiry_date, reorder_level) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (medicine_id, batch_no, quantity, pp, sp, mfg, exp, reorder),
            )
        return cur.lastrowid
    except sqlite3.Error:
        raise ServiceError("Could not save the batch. Please try again.")


def update_batch(conn, inventory_id, form):
    """Edit batch details. Quantity is intentionally not editable here."""
    if get_batch(conn, inventory_id) is None:
        raise ValidationError("Batch not found.")
    batch_no, pp, sp, mfg, exp, reorder = _batch_fields(form)
    medicine_id = get_batch(conn, inventory_id)["medicine_id"]
    if conn.execute(
        "SELECT 1 FROM inventory WHERE medicine_id=? AND batch_no=? AND inventory_id != ?",
        (medicine_id, batch_no, inventory_id),
    ).fetchone():
        raise ValidationError("Another batch of this medicine already uses that batch number.")
    try:
        with Transaction(conn):
            conn.execute(
                "UPDATE inventory SET batch_no=?, purchase_price=?, selling_price=?, "
                "manufacture_date=?, expiry_date=?, reorder_level=? WHERE inventory_id=?",
                (batch_no, pp, sp, mfg, exp, reorder, inventory_id),
            )
    except sqlite3.Error:
        raise ServiceError("Could not update the batch. Please try again.")


_BATCH_SELECT = (
    "SELECT i.*, m.medicine_name, m.category, m.manufacturer "
    "FROM inventory i JOIN medicines m ON m.medicine_id = i.medicine_id "
)


def get_batch(conn, inventory_id):
    return conn.execute(_BATCH_SELECT + "WHERE i.inventory_id = ?", (inventory_id,)).fetchone()


def list_inventory(conn, search="", on=None):
    """All batches (with a computed `status`), optionally filtered by search text."""
    search = (search or "").strip()
    sql, params = _BATCH_SELECT, []
    if search:
        like = f"%{search}%"
        sql += "WHERE m.medicine_name LIKE ? OR i.batch_no LIKE ?"
        params = [like, like]
        if search.isdigit():
            sql += " OR m.medicine_id = ?"
            params.append(int(search))
    sql += " ORDER BY m.medicine_name, i.expiry_date"
    rows = []
    for r in conn.execute(sql, params).fetchall():
        d = dict(r)
        d["status"] = inventory_status(d, on)
        rows.append(d)
    return rows


def check_stock(conn, inventory_id):
    batch = get_batch(conn, inventory_id)
    return None if batch is None else batch["quantity"]


def check_expiry(conn, inventory_id, on=None):
    batch = get_batch(conn, inventory_id)
    return None if batch is None else is_expired(batch["expiry_date"], on)
