"""Waste records: expired / damaged / recalled / other stock written off."""
import sqlite3

from database import Transaction
from services.common import (
    ServiceError, ValidationError, is_expired, parse_date, parse_int, today,
)
from services.inventory_service import get_batch

WASTE_REASONS = ("Expired", "Damaged", "Recalled", "Other")


def list_expired_batches(conn, on=None):
    """Expired batches that still have stock waiting to be written off."""
    on = on or today()
    return conn.execute(
        "SELECT i.*, m.medicine_name FROM inventory i "
        "JOIN medicines m ON m.medicine_id = i.medicine_id "
        "WHERE i.expiry_date < ? AND i.quantity > 0 ORDER BY i.expiry_date",
        (on.isoformat(),)).fetchall()


def record_waste(conn, user_id, form):
    """Write off stock. Creates a waste record AND reduces inventory atomically.

    Rules: quantity must be a positive whole number not above current stock;
    reason must be one of WASTE_REASONS; disposal date cannot be in the future;
    reason "Expired" is only allowed for a batch that is actually expired.
    """
    inventory_id = parse_int(form.get("inventory_id"), "Batch")
    quantity = parse_int(form.get("quantity"), "Quantity")
    reason = str(form.get("reason") or "").strip()
    if reason not in WASTE_REASONS:
        raise ValidationError("Please choose a valid waste reason.")
    disposal = parse_date(form.get("disposal_date") or today().isoformat(), "Disposal date")
    if disposal > today().isoformat():
        raise ValidationError("Disposal date cannot be in the future.")
    if get_batch(conn, inventory_id) is None:
        raise ValidationError("Selected batch does not exist.")

    try:
        with Transaction(conn):
            batch = get_batch(conn, inventory_id)
            if reason == "Expired" and not is_expired(batch["expiry_date"]):
                raise ValidationError("This batch has not expired. Choose another reason.")
            if quantity > batch["quantity"]:
                raise ValidationError(
                    f"Insufficient stock. Only {batch['quantity']} unit(s) available.")
            conn.execute(
                "UPDATE inventory SET quantity = quantity - ? WHERE inventory_id = ?",
                (quantity, inventory_id))
            cur = conn.execute(
                "INSERT INTO waste_records (inventory_id, quantity, reason, disposal_date, user_id) "
                "VALUES (?, ?, ?, ?, ?)", (inventory_id, quantity, reason, disposal, user_id))
            waste_id = cur.lastrowid
    except sqlite3.Error:
        raise ServiceError("The waste record could not be saved. No stock was changed.")

    return {"waste_id": waste_id, "new_quantity": get_batch(conn, inventory_id)["quantity"]}


def list_waste(conn, start=None, end=None):
    sql = ("SELECT w.*, m.medicine_name, i.batch_no, u.name AS user_name "
           "FROM waste_records w "
           "JOIN inventory i ON i.inventory_id = w.inventory_id "
           "JOIN medicines m ON m.medicine_id = i.medicine_id "
           "JOIN users u ON u.user_id = w.user_id WHERE 1=1")
    params = []
    if start:
        sql += " AND w.disposal_date >= ?"
        params.append(start)
    if end:
        sql += " AND w.disposal_date <= ?"
        params.append(end)
    sql += " ORDER BY w.waste_id DESC"
    return conn.execute(sql, params).fetchall()
