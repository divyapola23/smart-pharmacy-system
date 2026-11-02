"""Purchases and sales. Both are rows in the single `transactions` table.

Every stock change and its transaction row are written inside ONE database
transaction: both succeed, or both are rolled back.
"""
import sqlite3

from database import Transaction
from services.common import (
    ServiceError, ValidationError, is_expired, now_str, parse_date, parse_int,
    parse_price, today, clean_text,
)
from services.inventory_service import get_batch, get_medicine


def record_purchase(conn, user_id, form):
    """Record a purchase.

    Rules:
      * If form has `inventory_id`, stock is added to that existing batch.
      * Otherwise the form describes a batch (medicine_id + batch_no + ...):
          - if that medicine/batch already exists, stock is added to it;
          - if not, a new batch is created.
      * The batch's purchase_price is updated to the latest unit price paid.
      * Expired stock cannot be purchased.
    Returns a dict with transaction_id, inventory_id, new_quantity, total_amount.
    """
    quantity = parse_int(form.get("quantity"), "Quantity")
    unit_price = parse_price(form.get("unit_price"), "Unit purchase price")
    total = round(quantity * unit_price, 2)

    inventory_id = str(form.get("inventory_id") or "").strip()
    new_batch = None
    if inventory_id:
        inventory_id = parse_int(inventory_id, "Batch")
    else:
        medicine_id = parse_int(form.get("medicine_id"), "Medicine")
        if get_medicine(conn, medicine_id) is None:
            raise ValidationError("Selected medicine does not exist.")
        batch_no = clean_text(form.get("batch_no"), "Batch number", max_len=50)
        existing = conn.execute(
            "SELECT inventory_id FROM inventory WHERE medicine_id=? AND batch_no=?",
            (medicine_id, batch_no)).fetchone()
        if existing:
            inventory_id = existing["inventory_id"]
        else:
            expiry = parse_date(form.get("expiry_date"), "Expiry date")
            if is_expired(expiry):
                raise ValidationError("Cannot purchase a batch that is already expired.")
            mfg = parse_date(form.get("manufacture_date"), "Manufacture date", required=False)
            if mfg and mfg >= expiry:
                raise ValidationError("Expiry date must be after the manufacture date.")
            new_batch = dict(
                medicine_id=medicine_id, batch_no=batch_no, expiry=expiry, mfg=mfg,
                selling_price=parse_price(form.get("selling_price"), "Selling price"),
                reorder=parse_int(form.get("reorder_level") or 10, "Reorder level", minimum=0),
            )

    if inventory_id:
        batch = get_batch(conn, inventory_id)
        if batch is None:
            raise ValidationError("Selected batch does not exist.")
        if is_expired(batch["expiry_date"]):
            raise ValidationError("Cannot purchase stock for an expired batch.")

    try:
        with Transaction(conn):
            if new_batch:
                cur = conn.execute(
                    "INSERT INTO inventory (medicine_id, batch_no, quantity, purchase_price, "
                    "selling_price, manufacture_date, expiry_date, reorder_level) "
                    "VALUES (?, ?, 0, ?, ?, ?, ?, ?)",
                    (new_batch["medicine_id"], new_batch["batch_no"], unit_price,
                     new_batch["selling_price"], new_batch["mfg"], new_batch["expiry"],
                     new_batch["reorder"]))
                inventory_id = cur.lastrowid
            conn.execute(
                "UPDATE inventory SET quantity = quantity + ?, purchase_price = ? "
                "WHERE inventory_id = ?", (quantity, unit_price, inventory_id))
            cur = conn.execute(
                "INSERT INTO transactions (transaction_type, inventory_id, quantity, "
                "unit_price, total_amount, transaction_date, user_id) "
                "VALUES ('Purchase', ?, ?, ?, ?, ?, ?)",
                (inventory_id, quantity, unit_price, total, now_str(), user_id))
            transaction_id = cur.lastrowid
    except sqlite3.Error:
        raise ServiceError("The purchase could not be saved. No stock was changed.")

    return {"transaction_id": transaction_id, "inventory_id": inventory_id,
            "new_quantity": get_batch(conn, inventory_id)["quantity"], "total_amount": total}


def record_sale(conn, user_id, form):
    """Record a sale from one batch.

    Rejects: unknown batch, expired batch, quantity <= 0, quantity greater than
    stock, invalid/negative price. Unit price defaults to the batch selling price.
    """
    inventory_id = parse_int(form.get("inventory_id"), "Batch")
    quantity = parse_int(form.get("quantity"), "Quantity")
    batch = get_batch(conn, inventory_id)
    if batch is None:
        raise ValidationError("Selected batch does not exist.")
    price_text = str(form.get("unit_price") or "").strip()
    unit_price = parse_price(price_text, "Unit price") if price_text else batch["selling_price"]
    total = round(quantity * unit_price, 2)

    try:
        with Transaction(conn):
            # Re-read inside the transaction so checks use the latest data.
            batch = get_batch(conn, inventory_id)
            if is_expired(batch["expiry_date"]):
                raise ValidationError("This batch has expired and cannot be sold.")
            if quantity > batch["quantity"]:
                raise ValidationError(
                    f"Insufficient stock. Only {batch['quantity']} unit(s) available.")
            conn.execute(
                "UPDATE inventory SET quantity = quantity - ? WHERE inventory_id = ?",
                (quantity, inventory_id))
            cur = conn.execute(
                "INSERT INTO transactions (transaction_type, inventory_id, quantity, "
                "unit_price, total_amount, transaction_date, user_id) "
                "VALUES ('Sale', ?, ?, ?, ?, ?, ?)",
                (inventory_id, quantity, unit_price, total, now_str(), user_id))
            transaction_id = cur.lastrowid
    except sqlite3.Error:
        raise ServiceError("The sale could not be saved. No stock was changed.")

    return {"transaction_id": transaction_id, "inventory_id": inventory_id,
            "new_quantity": get_batch(conn, inventory_id)["quantity"], "total_amount": total}


def list_transactions(conn, transaction_type=None, start=None, end=None):
    sql = ("SELECT t.*, m.medicine_name, i.batch_no, u.name AS user_name "
           "FROM transactions t "
           "JOIN inventory i ON i.inventory_id = t.inventory_id "
           "JOIN medicines m ON m.medicine_id = i.medicine_id "
           "JOIN users u ON u.user_id = t.user_id WHERE 1=1")
    params = []
    if transaction_type in ("Purchase", "Sale"):
        sql += " AND t.transaction_type = ?"
        params.append(transaction_type)
    if start:
        sql += " AND date(t.transaction_date) >= ?"
        params.append(start)
    if end:
        sql += " AND date(t.transaction_date) <= ?"
        params.append(end)
    sql += " ORDER BY t.transaction_id DESC"
    return conn.execute(sql, params).fetchall()
