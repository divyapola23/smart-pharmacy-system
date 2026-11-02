"""Load clearly-labelled DEMO data (medicines, batches, transactions, waste).

Usage:   python seed_demo.py
         python seed_demo.py --db some_other.db

* Needs at least one user to exist (run create_user.py first); records are
  attributed to the first pharmacist, or to the first user if none exists.
* Refuses to run twice: if demo data is already present it does nothing.
* Demo batch numbers start with "DEMO-" so they are easy to recognise.
* Contains no patient information.
"""
import argparse
import sys
from datetime import timedelta

import database
from services import transaction_service as txn, waste_service as waste
from services.common import today

DEMO_MEDICINES = [
    ("Paracetamol 500mg", "Analgesic", "Demo Pharma Ltd"),
    ("Amoxicillin 250mg", "Antibiotic", "Demo Pharma Ltd"),
    ("Cetirizine 10mg", "Antihistamine", "Sample Labs"),
    ("Ibuprofen 400mg", "Analgesic", "Sample Labs"),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=None)
    args = parser.parse_args()

    database.init_db(args.db)
    conn = database.get_connection(args.db)
    if conn.execute("SELECT 1 FROM inventory WHERE batch_no LIKE 'DEMO-%'").fetchone():
        sys.exit("Demo data already present. Nothing was changed.")
    user = (conn.execute("SELECT user_id FROM users WHERE role='pharmacist' ORDER BY user_id").fetchone()
            or conn.execute("SELECT user_id FROM users ORDER BY user_id").fetchone())
    if user is None:
        sys.exit("Create a user first:  python create_user.py")
    uid = user["user_id"]
    d = today()

    ids = {}
    for name, cat, maker in DEMO_MEDICINES:
        row = conn.execute("SELECT medicine_id FROM medicines WHERE medicine_name=? AND manufacturer=?",
                           (name, maker)).fetchone()
        if row:
            ids[name] = row["medicine_id"]
        else:
            ids[name] = conn.execute(
                "INSERT INTO medicines (medicine_name, category, manufacturer) VALUES (?, ?, ?)",
                (name, cat, maker)).lastrowid

    def purchase(med, batch, qty, cost, sell, expiry, reorder):
        return txn.record_purchase(conn, uid, {
            "medicine_id": ids[med], "batch_no": batch, "quantity": qty, "unit_price": cost,
            "selling_price": sell, "expiry_date": (d + timedelta(days=expiry)).isoformat(),
            "manufacture_date": (d - timedelta(days=200)).isoformat(), "reorder_level": reorder})

    p1 = purchase("Paracetamol 500mg", "DEMO-PCM-01", 200, 1.5, 2.5, 400, 40)
    p2 = purchase("Amoxicillin 250mg", "DEMO-AMX-01", 60, 6.0, 9.0, 20, 30)      # near expiry
    p3 = purchase("Cetirizine 10mg", "DEMO-CET-01", 25, 2.0, 3.5, 300, 30)       # will be low stock
    p4 = purchase("Ibuprofen 400mg", "DEMO-IBU-01", 80, 3.0, 5.0, 365, 20)

    # An already-expired batch, created as opening stock (a purchase of expired stock is refused).
    conn.execute(
        "INSERT INTO inventory (medicine_id, batch_no, quantity, purchase_price, selling_price, "
        "manufacture_date, expiry_date, reorder_level) VALUES (?, 'DEMO-IBU-OLD', 15, 3.0, 5.0, ?, ?, 20)",
        (ids["Ibuprofen 400mg"], (d - timedelta(days=700)).isoformat(),
         (d - timedelta(days=10)).isoformat()))
    expired_id = conn.execute("SELECT inventory_id FROM inventory WHERE batch_no='DEMO-IBU-OLD'"
                              ).fetchone()[0]

    txn.record_sale(conn, uid, {"inventory_id": p1["inventory_id"], "quantity": 30})
    txn.record_sale(conn, uid, {"inventory_id": p2["inventory_id"], "quantity": 10})
    txn.record_sale(conn, uid, {"inventory_id": p3["inventory_id"], "quantity": 5})
    txn.record_sale(conn, uid, {"inventory_id": p4["inventory_id"], "quantity": 12})
    waste.record_waste(conn, uid, {"inventory_id": expired_id, "quantity": 5, "reason": "Expired"})
    waste.record_waste(conn, uid, {"inventory_id": p1["inventory_id"], "quantity": 4,
                                   "reason": "Damaged"})
    print("Demo data loaded (batch numbers start with DEMO-).")


if __name__ == "__main__":
    main()
