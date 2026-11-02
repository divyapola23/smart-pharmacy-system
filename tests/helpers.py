"""Shared test setup: a temporary database for every test (the real pharmacy.db is never touched)."""
import os
import tempfile
import unittest
from datetime import timedelta

from werkzeug.security import generate_password_hash

import database
from app import create_app
from services.common import today

PASSWORD = "TestPass123"
PASSWORD_HASH = generate_password_hash(PASSWORD)  # hashed once: hashing is deliberately slow


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.app = create_app({"TESTING": True, "DATABASE": self.db_path,
                               "SECRET_KEY": "test-secret-key"})
        self.client = self.app.test_client()
        self.conn = database.get_connection(self.db_path)
        self.admin_id = self.add_user("Admin One", "admin@test.com", "admin")
        self.pharm_id = self.add_user("Pat Pharmacist", "pharm@test.com", "pharmacist")

    def tearDown(self):
        self.conn.close()
        os.remove(self.db_path)

    # ------------------------------------------------------------ data helpers
    def add_user(self, name, email, role):
        return self.conn.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name, email, PASSWORD_HASH, role)).lastrowid

    def add_medicine(self, name="Paracetamol", maker="Acme"):
        return self.conn.execute(
            "INSERT INTO medicines (medicine_name, category, manufacturer) VALUES (?, 'Analgesic', ?)",
            (name, maker)).lastrowid

    def add_batch(self, medicine_id, batch="B1", qty=50, days_to_expiry=365, reorder=10,
                  purchase=1.0, selling=2.0):
        expiry = (today() + timedelta(days=days_to_expiry)).isoformat()
        return self.conn.execute(
            "INSERT INTO inventory (medicine_id, batch_no, quantity, purchase_price, selling_price, "
            "manufacture_date, expiry_date, reorder_level) VALUES (?, ?, ?, ?, ?, NULL, ?, ?)",
            (medicine_id, batch, qty, purchase, selling, expiry, reorder)).lastrowid

    def stock(self, inventory_id):
        return self.conn.execute("SELECT quantity FROM inventory WHERE inventory_id=?",
                                 (inventory_id,)).fetchone()[0]

    def count(self, table):
        return self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    # ------------------------------------------------------------ HTTP helpers
    def csrf(self, client=None):
        client = client or self.client
        with client.session_transaction() as s:
            token = s.get("csrf_token")
        if not token:
            client.get("/login")
            with client.session_transaction() as s:
                token = s["csrf_token"]
        return token

    def login(self, email="pharm@test.com", password=PASSWORD, client=None):
        client = client or self.client
        return client.post("/login", data={"email": email, "password": password,
                                           "csrf_token": self.csrf(client)}, follow_redirects=True)

    def post(self, url, data=None, follow=True):
        payload = dict(data or {}, csrf_token=self.csrf())
        return self.client.post(url, data=payload, follow_redirects=follow)
