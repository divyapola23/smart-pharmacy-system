from datetime import timedelta

from services import inventory_service as inv
from services.common import ValidationError, today
from tests.helpers import BaseTestCase


class MedicineTests(BaseTestCase):
    def test_add_and_update_medicine(self):
        mid = inv.add_medicine(self.conn, {"medicine_name": "Aspirin", "category": "Analgesic",
                                           "manufacturer": "Acme"})
        self.assertEqual(inv.get_medicine(self.conn, mid)["medicine_name"], "Aspirin")
        inv.update_medicine(self.conn, mid, {"medicine_name": "Aspirin 75mg", "category": "Antiplatelet",
                                             "manufacturer": "Acme"})
        row = inv.get_medicine(self.conn, mid)
        self.assertEqual((row["medicine_name"], row["category"]), ("Aspirin 75mg", "Antiplatelet"))

    def test_name_required_and_duplicates_blocked(self):
        with self.assertRaises(ValidationError):
            inv.add_medicine(self.conn, {"medicine_name": "  "})
        inv.add_medicine(self.conn, {"medicine_name": "Aspirin", "manufacturer": "Acme"})
        with self.assertRaises(ValidationError):
            inv.add_medicine(self.conn, {"medicine_name": "ASPIRIN", "manufacturer": "acme"})
        self.assertEqual(self.count("medicines"), 1)

    def test_search_by_name_and_id(self):
        a = self.add_medicine("Aspirin", "X")
        self.add_medicine("Ibuprofen", "X")
        self.assertEqual([m["medicine_id"] for m in inv.list_medicines(self.conn, "aspi")], [a])
        self.assertEqual([m["medicine_id"] for m in inv.list_medicines(self.conn, str(a))], [a])

    def test_medicine_pages_work_over_http(self):
        self.login("pharm@test.com")
        self.post("/medicines/add", {"medicine_name": "Zinc", "category": "Supplement", "manufacturer": "Z"})
        self.assertEqual(self.count("medicines"), 1)
        mid = self.conn.execute("SELECT medicine_id FROM medicines").fetchone()[0]
        self.post(f"/medicines/{mid}/edit", {"medicine_name": "Zinc 50mg", "category": "", "manufacturer": "Z"})
        self.assertEqual(self.conn.execute("SELECT medicine_name FROM medicines").fetchone()[0], "Zinc 50mg")
        self.assertEqual(self.client.get(f"/medicines/{mid}").status_code, 200)
        self.assertEqual(self.client.get("/medicines/999").status_code, 404)


class BatchTests(BaseTestCase):
    def form(self, mid, **over):
        data = {"medicine_id": mid, "batch_no": "B100", "quantity": "40", "purchase_price": "1.5",
                "selling_price": "2.5", "manufacture_date": "", "reorder_level": "10",
                "expiry_date": (today() + timedelta(days=400)).isoformat()}
        data.update(over)
        return data

    def test_batch_requires_existing_medicine(self):
        with self.assertRaises(ValidationError):
            inv.add_batch(self.conn, self.form(999))
        iid = inv.add_batch(self.conn, self.form(self.add_medicine()))
        self.assertEqual(self.stock(iid), 40)

    def test_multiple_batches_of_same_medicine(self):
        mid = self.add_medicine()
        inv.add_batch(self.conn, self.form(mid, batch_no="A"))
        inv.add_batch(self.conn, self.form(mid, batch_no="B"))
        with self.assertRaises(ValidationError):  # same batch number again
            inv.add_batch(self.conn, self.form(mid, batch_no="A"))
        self.assertEqual(self.count("inventory"), 2)

    def test_invalid_batch_input_rejected(self):
        mid = self.add_medicine()
        for bad in [{"quantity": "-1"}, {"quantity": "abc"}, {"purchase_price": "-5"},
                    {"selling_price": "x"}, {"expiry_date": "31/12/2030"}, {"expiry_date": ""},
                    {"reorder_level": "-2"}, {"manufacture_date": "2999-01-01"}]:
            with self.assertRaises(ValidationError, msg=str(bad)):
                inv.add_batch(self.conn, self.form(mid, **bad))
        self.assertEqual(self.count("inventory"), 0)

    def test_update_batch_does_not_change_quantity(self):
        mid = self.add_medicine()
        iid = self.add_batch(mid, qty=33)
        inv.update_batch(self.conn, iid, self.form(mid, batch_no="NEW", quantity="999", reorder_level="5"))
        row = inv.get_batch(self.conn, iid)
        self.assertEqual((row["batch_no"], row["reorder_level"], row["quantity"]), ("NEW", 5, 33))

    def test_status_low_stock_near_expiry_expired(self):
        mid = self.add_medicine()
        ok = self.add_batch(mid, "OK", qty=100, days_to_expiry=365, reorder=10)
        low = self.add_batch(mid, "LOW", qty=10, days_to_expiry=365, reorder=10)
        near = self.add_batch(mid, "NEAR", qty=100, days_to_expiry=15, reorder=10)
        old = self.add_batch(mid, "OLD", qty=100, days_to_expiry=-1, reorder=10)
        empty = self.add_batch(mid, "EMPTY", qty=0, days_to_expiry=365, reorder=10)
        status = {r["inventory_id"]: r["status"] for r in inv.list_inventory(self.conn)}
        self.assertEqual(status[ok], "Available")
        self.assertEqual(status[low], "Low Stock")
        self.assertEqual(status[near], "Near Expiry")
        self.assertEqual(status[old], "Expired")
        self.assertEqual(status[empty], "Out of Stock")

    def test_expiry_on_today_is_not_expired(self):
        mid = self.add_medicine()
        iid = self.add_batch(mid, days_to_expiry=0)
        self.assertFalse(inv.check_expiry(self.conn, iid))

    def test_inventory_search_by_batch_name_and_medicine_id(self):
        mid = self.add_medicine("Aspirin")
        self.add_batch(mid, "ZX-9")
        self.assertEqual(len(inv.list_inventory(self.conn, "zx")), 1)
        self.assertEqual(len(inv.list_inventory(self.conn, "aspirin")), 1)
        self.assertEqual(len(inv.list_inventory(self.conn, str(mid))), 1)
        self.assertEqual(len(inv.list_inventory(self.conn, "nothing")), 0)

    def test_admin_adds_batch_over_http(self):
        self.login("admin@test.com")
        mid = self.add_medicine()
        self.post("/inventory/add", self.form(mid))
        self.assertEqual(self.count("inventory"), 1)
