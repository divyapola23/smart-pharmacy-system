from datetime import timedelta

from services import waste_service as waste
from services.common import ValidationError, today
from tests.helpers import BaseTestCase


class WasteTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mid = self.add_medicine()

    def test_waste_reduces_stock_65_minus_3(self):
        iid = self.add_batch(self.mid, qty=65)
        r = waste.record_waste(self.conn, self.pharm_id,
                               {"inventory_id": iid, "quantity": "3", "reason": "Damaged"})
        self.assertEqual(self.stock(iid), 62)
        self.assertEqual(r["new_quantity"], 62)
        row = self.conn.execute("SELECT * FROM waste_records").fetchone()
        self.assertEqual((row["quantity"], row["reason"], row["user_id"],
                          row["disposal_date"]), (3, "Damaged", self.pharm_id, today().isoformat()))

    def test_expired_batch_listed_and_can_be_written_off(self):
        old = self.add_batch(self.mid, "OLD", qty=20, days_to_expiry=-5)
        self.add_batch(self.mid, "FRESH", qty=20)
        self.assertEqual([b["inventory_id"] for b in waste.list_expired_batches(self.conn)], [old])
        waste.record_waste(self.conn, self.pharm_id, {"inventory_id": old, "quantity": "20", "reason": "Expired"})
        self.assertEqual(self.stock(old), 0)
        self.assertEqual(waste.list_expired_batches(self.conn), [])  # nothing left to dispose
        self.assertEqual(len(waste.list_waste(self.conn)), 1)       # history preserved

    def test_invalid_waste_rejected_and_nothing_changes(self):
        iid = self.add_batch(self.mid, qty=10)
        base = {"inventory_id": iid, "quantity": "2", "reason": "Damaged"}
        bad = [dict(base, quantity="11"), dict(base, quantity="0"), dict(base, quantity="-1"),
               dict(base, quantity="x"), dict(base, inventory_id="9999"), dict(base, reason="Because"),
               dict(base, reason=""), dict(base, reason="Expired"),  # batch is not expired
               dict(base, disposal_date=(today() + timedelta(days=3)).isoformat()),
               dict(base, disposal_date="not-a-date")]
        for form in bad:
            with self.assertRaises(ValidationError, msg=str(form)):
                waste.record_waste(self.conn, self.pharm_id, form)
        self.assertEqual(self.stock(iid), 10)
        self.assertEqual(self.count("waste_records"), 0)

    def test_waste_failure_midway_rolls_back(self):
        from services.common import ServiceError
        iid = self.add_batch(self.mid, qty=10)
        with self.assertRaises(ServiceError):
            waste.record_waste(self.conn, 9999, {"inventory_id": iid, "quantity": "2", "reason": "Damaged"})
        self.assertEqual(self.stock(iid), 10)
        self.assertEqual(self.count("waste_records"), 0)

    def test_waste_over_http_and_history_visible_to_admin(self):
        iid = self.add_batch(self.mid, qty=10)
        self.login("pharm@test.com")
        r = self.post("/waste/add", {"inventory_id": iid, "quantity": "4", "reason": "Recalled"})
        self.assertIn(b"Waste recorded", r.data)
        self.assertEqual(self.stock(iid), 6)
        self.client = self.app.test_client()
        self.login("admin@test.com")
        self.assertIn(b"Recalled", self.client.get("/waste").data)
