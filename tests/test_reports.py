from datetime import timedelta

from services import report_service as rep
from services import transaction_service as txn
from services import waste_service as waste
from services.common import ServiceError, today
from tests.helpers import BaseTestCase


class ReportTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        mid = self.add_medicine("Aspirin")
        self.a = self.add_batch(mid, "A", qty=100, selling=3.0, reorder=10)
        self.low = self.add_batch(mid, "LOW", qty=4, reorder=10)
        self.old = self.add_batch(mid, "OLD", qty=7, days_to_expiry=-2)
        txn.record_purchase(self.conn, self.pharm_id, {"inventory_id": self.a, "quantity": "20", "unit_price": "1.5"})
        txn.record_sale(self.conn, self.pharm_id, {"inventory_id": self.a, "quantity": "10"})
        txn.record_sale(self.conn, self.pharm_id, {"inventory_id": self.a, "quantity": "5", "unit_price": "4"})
        waste.record_waste(self.conn, self.pharm_id, {"inventory_id": self.old, "quantity": "3", "reason": "Expired"})

    def test_inventory_report_matches_database(self):
        r = rep.generate_report(self.conn, "inventory")
        self.assertEqual(len(r["rows"]), 3)
        totals = dict(r["totals"])
        self.assertEqual(totals["Total units in stock"], self.conn.execute("SELECT SUM(quantity) FROM inventory").fetchone()[0])
        self.assertEqual(totals["Low-stock batches"], 1)
        self.assertEqual(totals["Expired batches"], 1)

    def test_low_stock_and_expiry_reports(self):
        low = rep.generate_report(self.conn, "low_stock")
        self.assertEqual([row[2] for row in low["rows"]], ["LOW"])
        exp = rep.generate_report(self.conn, "expiry")
        self.assertEqual([row[2] for row in exp["rows"]], ["OLD"])
        self.assertEqual(exp["rows"][0][5], "Expired")

    def test_purchase_and_sales_totals(self):
        p = rep.generate_report(self.conn, "purchases")
        self.assertEqual(dict(p["totals"]), {"Total quantity purchased": 20, "Total purchase value": 30.0})
        s = rep.generate_report(self.conn, "sales")
        self.assertEqual(dict(s["totals"]), {"Total quantity sold": 15, "Total sales value": 50.0})  # 10x3 + 5x4

    def test_waste_report_total(self):
        w = rep.generate_report(self.conn, "waste")
        self.assertEqual(dict(w["totals"])["Total wasted quantity"], 3)

    def test_summary_report(self):
        s = {row[0]: row[1] for row in rep.generate_report(self.conn, "summary")["rows"]}
        self.assertEqual(s["Total purchased quantity"], 20)
        self.assertEqual(s["Total sold quantity"], 15)
        self.assertEqual(s["Total wasted quantity"], 3)
        self.assertEqual(s["Total purchase value"], 30.0)
        self.assertEqual(s["Total sales value"], 50.0)

    def test_date_filter_includes_and_excludes(self):
        t = today().isoformat()
        inside = rep.generate_report(self.conn, "sales", t, t)
        self.assertEqual(len(inside["rows"]), 2)
        tomorrow = (today() + timedelta(days=1)).isoformat()
        outside = rep.generate_report(self.conn, "sales", tomorrow, tomorrow)
        self.assertEqual(outside["rows"], [])
        self.assertTrue(outside["empty"])
        self.assertEqual(dict(outside["totals"])["Total sales value"], 0)

    def test_invalid_filters_rejected(self):
        with self.assertRaises(ServiceError):
            rep.generate_report(self.conn, "sales", "2030-02-01", "2030-01-01")
        with self.assertRaises(ServiceError):
            rep.generate_report(self.conn, "sales", "garbage", None)
        with self.assertRaises(ServiceError):
            rep.generate_report(self.conn, "nonsense")

    def test_csv_contains_filtered_data(self):
        t = today().isoformat()
        csv_text = rep.report_to_csv(rep.generate_report(self.conn, "sales", t, t))
        self.assertIn("Sales Transaction Report", csv_text)
        self.assertIn("Aspirin", csv_text)
        self.assertIn("Total sales value,50.0", csv_text)
        tomorrow = (today() + timedelta(days=1)).isoformat()
        empty_csv = rep.report_to_csv(rep.generate_report(self.conn, "sales", tomorrow, tomorrow))
        self.assertNotIn("Aspirin", empty_csv)

    def test_csv_blocks_formula_injection(self):
        self.conn.execute("UPDATE medicines SET medicine_name = '=HYPERLINK(\"http://x\")'")
        csv_text = rep.report_to_csv(rep.generate_report(self.conn, "inventory"))
        self.assertNotIn(",=HYPERLINK", csv_text)
        self.assertIn("'=HYPERLINK", csv_text)

    def test_reports_page_and_export_over_http(self):
        self.login("admin@test.com")
        r = self.client.get("/reports?type=sales")
        self.assertIn(b"Sales Transaction Report", r.data)
        r = self.client.get("/reports?type=sales&start=2000-01-01&end=2000-01-02")
        self.assertIn(b"No records found", r.data)
        r = self.client.get("/reports/export?type=purchases")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.mimetype, "text/csv")
        self.assertIn(b"Purchase Transaction Report", r.data)

    def test_dashboard_counts_come_from_database(self):
        stats = rep.dashboard_stats(self.conn)
        self.assertEqual((stats["medicines"], stats["batches"], stats["low_stock"], stats["expired"]), (1, 3, 1, 1))

    def test_sales_per_medicine(self):
        sales = rep.sales_per_medicine(self.conn)
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0]["medicine_name"], "Aspirin")
        self.assertEqual(sales[0]["sales_count"], 2)
        self.assertEqual(sales[0]["total_units_sold"], 15)  # 10 + 5
        self.assertEqual(sales[0]["total_revenue"], 50.0)

    def test_medicine_sales_summary(self):
        mid = self.conn.execute("SELECT medicine_id FROM medicines WHERE medicine_name='Aspirin'").fetchone()[0]
        summary = rep.medicine_sales_summary(self.conn, mid)
        self.assertEqual(summary["sales_count"], 2)
        self.assertEqual(summary["total_units_sold"], 15)
        self.assertEqual(summary["total_revenue"], 50.0)

    def test_admin_dashboard_shows_sales_per_medicine(self):
        self.login("admin@test.com")
        r = self.client.get("/dashboard")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Sales Count per Medicine", r.data)
        self.assertIn(b"Aspirin", r.data)

    def test_sales_per_medicine_report_and_export(self):
        self.login("admin@test.com")
        r = self.client.get("/reports?type=sales_per_medicine")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Sales Count Per Medicine Report", r.data)
        self.assertIn(b"Aspirin", r.data)

        export = self.client.get("/reports/export?type=sales_per_medicine")
        self.assertEqual(export.status_code, 200)
        self.assertEqual(export.mimetype, "text/csv")
        self.assertIn(b"Sales Count Per Medicine Report", export.data)
        self.assertIn(b"Aspirin", export.data)
