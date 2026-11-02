from datetime import timedelta
from unittest import mock

from services import transaction_service as txn
from services.common import ServiceError, ValidationError, today
from tests.helpers import BaseTestCase


class PurchaseTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mid = self.add_medicine()

    def test_purchase_increases_stock_50_plus_20(self):
        iid = self.add_batch(self.mid, qty=50)
        r = txn.record_purchase(self.conn, self.pharm_id,
                                {"inventory_id": iid, "quantity": "20", "unit_price": "1.25"})
        self.assertEqual(self.stock(iid), 70)
        self.assertEqual(r["new_quantity"], 70)
        self.assertEqual(r["total_amount"], 25.0)
        row = self.conn.execute("SELECT * FROM transactions").fetchone()
        self.assertEqual((row["transaction_type"], row["quantity"], row["total_amount"], row["user_id"]),
                         ("Purchase", 20, 25.0, self.pharm_id))

    def test_purchase_new_batch_creates_inventory_record(self):
        r = txn.record_purchase(self.conn, self.pharm_id, {
            "medicine_id": self.mid, "batch_no": "NEW1", "quantity": "30", "unit_price": "2",
            "selling_price": "3", "expiry_date": (today() + timedelta(days=200)).isoformat(),
            "reorder_level": "5"})
        self.assertEqual(self.stock(r["inventory_id"]), 30)
        self.assertEqual(self.count("inventory"), 1)

    def test_purchase_same_medicine_and_batch_adds_to_existing(self):
        iid = self.add_batch(self.mid, "SAME", qty=10)
        r = txn.record_purchase(self.conn, self.pharm_id, {
            "medicine_id": self.mid, "batch_no": "SAME", "quantity": "5", "unit_price": "1",
            "selling_price": "2", "expiry_date": (today() + timedelta(days=200)).isoformat()})
        self.assertEqual(r["inventory_id"], iid)
        self.assertEqual(self.stock(iid), 15)
        self.assertEqual(self.count("inventory"), 1)

    def test_invalid_purchases_rejected_and_change_nothing(self):
        iid = self.add_batch(self.mid, qty=50)
        old = self.add_batch(self.mid, "OLD", qty=5, days_to_expiry=-3)
        bad_forms = [
            {"inventory_id": iid, "quantity": "0", "unit_price": "1"},
            {"inventory_id": iid, "quantity": "-4", "unit_price": "1"},
            {"inventory_id": iid, "quantity": "2.5", "unit_price": "1"},
            {"inventory_id": iid, "quantity": "5", "unit_price": "-1"},
            {"inventory_id": iid, "quantity": "5", "unit_price": "abc"},
            {"inventory_id": 9999, "quantity": "5", "unit_price": "1"},
            {"inventory_id": old, "quantity": "5", "unit_price": "1"},
            {"medicine_id": 9999, "batch_no": "Z", "quantity": "5", "unit_price": "1"},
            {"medicine_id": self.mid, "batch_no": "Z", "quantity": "5", "unit_price": "1",
             "selling_price": "2", "expiry_date": "2001-01-01"},
        ]
        for form in bad_forms:
            with self.assertRaises(ValidationError, msg=str(form)):
                txn.record_purchase(self.conn, self.pharm_id, form)
        self.assertEqual(self.stock(iid), 50)
        self.assertEqual(self.stock(old), 5)
        self.assertEqual(self.count("transactions"), 0)
        self.assertEqual(self.count("inventory"), 2)


class SaleTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mid = self.add_medicine()

    def test_sale_decreases_stock_70_minus_5(self):
        iid = self.add_batch(self.mid, qty=70, selling=4.0)
        r = txn.record_sale(self.conn, self.pharm_id, {"inventory_id": iid, "quantity": "5"})
        self.assertEqual(self.stock(iid), 65)
        self.assertEqual(r["total_amount"], 20.0)  # 5 x 4.00 default selling price
        row = self.conn.execute("SELECT * FROM transactions").fetchone()
        self.assertEqual((row["transaction_type"], row["unit_price"]), ("Sale", 4.0))

    def test_sale_with_custom_unit_price(self):
        iid = self.add_batch(self.mid, qty=10, selling=4.0)
        r = txn.record_sale(self.conn, self.pharm_id, {"inventory_id": iid, "quantity": "2", "unit_price": "3.5"})
        self.assertEqual(r["total_amount"], 7.0)

    def test_sale_can_sell_exactly_all_stock(self):
        iid = self.add_batch(self.mid, qty=5)
        txn.record_sale(self.conn, self.pharm_id, {"inventory_id": iid, "quantity": "5"})
        self.assertEqual(self.stock(iid), 0)

    def test_sale_exceeding_stock_rejected(self):
        iid = self.add_batch(self.mid, qty=5)
        with self.assertRaises(ValidationError) as ctx:
            txn.record_sale(self.conn, self.pharm_id, {"inventory_id": iid, "quantity": "6"})
        self.assertIn("Insufficient stock", str(ctx.exception))
        self.assertEqual(self.stock(iid), 5)
        self.assertEqual(self.count("transactions"), 0)

    def test_sale_from_expired_batch_rejected(self):
        iid = self.add_batch(self.mid, qty=50, days_to_expiry=-1)
        with self.assertRaises(ValidationError) as ctx:
            txn.record_sale(self.conn, self.pharm_id, {"inventory_id": iid, "quantity": "1"})
        self.assertIn("expired", str(ctx.exception))
        self.assertEqual(self.stock(iid), 50)
        self.assertEqual(self.count("transactions"), 0)

    def test_other_invalid_sales_rejected(self):
        iid = self.add_batch(self.mid, qty=50)
        for form in [{"inventory_id": iid, "quantity": "0"}, {"inventory_id": iid, "quantity": "-3"},
                     {"inventory_id": iid, "quantity": ""}, {"inventory_id": 9999, "quantity": "1"},
                     {"inventory_id": "", "quantity": "1"},
                     {"inventory_id": iid, "quantity": "1", "unit_price": "-2"},
                     {"inventory_id": iid, "quantity": "1", "unit_price": "nan"}]:
            with self.assertRaises(ValidationError, msg=str(form)):
                txn.record_sale(self.conn, self.pharm_id, form)
        self.assertEqual(self.stock(iid), 50)
        self.assertEqual(self.count("transactions"), 0)

    def test_failure_midway_rolls_back_stock_change(self):
        """The stock UPDATE succeeds, then the INSERT fails (unknown user -> foreign key error).
        The stock change must be rolled back too."""
        iid = self.add_batch(self.mid, qty=50)
        with self.assertRaises(ServiceError) as ctx:
            txn.record_sale(self.conn, 9999, {"inventory_id": iid, "quantity": "5"})
        self.assertNotIn("FOREIGN", str(ctx.exception).upper())  # no raw SQL error shown
        self.assertEqual(self.stock(iid), 50)
        self.assertEqual(self.count("transactions"), 0)

    def test_purchase_failure_midway_rolls_back(self):
        iid = self.add_batch(self.mid, qty=50)
        with self.assertRaises(ServiceError):
            txn.record_purchase(self.conn, 9999, {"inventory_id": iid, "quantity": "5", "unit_price": "1"})
        self.assertEqual(self.stock(iid), 50)

    def test_database_blocks_negative_stock_even_if_service_bypassed(self):
        import sqlite3
        iid = self.add_batch(self.mid, qty=5)
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("UPDATE inventory SET quantity = quantity - 10 WHERE inventory_id=?", (iid,))
        self.assertEqual(self.stock(iid), 5)

    def test_transaction_type_restricted_by_database(self):
        import sqlite3
        iid = self.add_batch(self.mid)
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                "INSERT INTO transactions (transaction_type, inventory_id, quantity, unit_price, "
                "total_amount, transaction_date, user_id) VALUES ('Refund', ?, 1, 1, 1, 'x', ?)",
                (iid, self.pharm_id))


class TransactionRouteTests(BaseTestCase):
    def test_pharmacist_sale_and_purchase_over_http(self):
        iid = self.add_batch(self.add_medicine(), qty=70)
        self.login("pharm@test.com")
        r = self.post("/transactions/sale", {"inventory_id": iid, "quantity": "5"})
        self.assertIn(b"Sale recorded", r.data)
        self.assertEqual(self.stock(iid), 65)
        r = self.post("/transactions/purchase", {"inventory_id": iid, "quantity": "10", "unit_price": "1"})
        self.assertIn(b"Purchase recorded", r.data)
        self.assertEqual(self.stock(iid), 75)
        r = self.post("/transactions/sale", {"inventory_id": iid, "quantity": "500"}, follow=True)
        self.assertIn(b"Insufficient stock", r.data)
        self.assertEqual(self.stock(iid), 75)
        self.assertEqual(self.count("transactions"), 2)

    def test_admin_sees_transaction_history(self):
        iid = self.add_batch(self.add_medicine(), qty=70)
        txn.record_sale(self.conn, self.pharm_id, {"inventory_id": iid, "quantity": "1"})
        self.login("admin@test.com")
        r = self.client.get("/transactions?type=Sale")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Sale", r.data)
