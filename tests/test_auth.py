from tests.helpers import BaseTestCase, PASSWORD


class AuthTests(BaseTestCase):
    def test_valid_login_succeeds(self):
        r = self.login("admin@test.com")
        self.assertIn(b"Dashboard", r.data)

    def test_invalid_password_fails(self):
        r = self.login("admin@test.com", "wrong-password")
        self.assertIn(b"Invalid email or password", r.data)

    def test_unknown_email_gets_same_message(self):
        r = self.login("nobody@test.com")
        self.assertIn(b"Invalid email or password", r.data)

    def test_passwords_are_hashed(self):
        stored = self.conn.execute("SELECT password_hash FROM users WHERE email='admin@test.com'").fetchone()[0]
        self.assertNotEqual(stored, PASSWORD)
        self.assertNotIn(PASSWORD, stored)

    def test_protected_pages_redirect_when_logged_out(self):
        for url in ["/dashboard", "/medicines", "/inventory", "/transactions", "/waste",
                    "/reports", "/transactions/sale", "/waste/add"]:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 302, url)
            self.assertIn("/login", r.headers["Location"], url)

    def test_pharmacist_cannot_manage_inventory(self):
        self.login("pharm@test.com")
        self.assertEqual(self.client.get("/inventory/add").status_code, 403)
        mid = self.add_medicine()
        r = self.post("/inventory/add", {"medicine_id": mid, "batch_no": "X", "quantity": 5,
                      "purchase_price": 1, "selling_price": 2, "expiry_date": "2099-01-01",
                      "reorder_level": 1})
        self.assertEqual(r.status_code, 403)
        self.assertEqual(self.count("inventory"), 0)

    def test_admin_cannot_record_sales_purchases_or_waste(self):
        self.login("admin@test.com")
        for url in ["/transactions/sale", "/transactions/purchase", "/waste/add"]:
            self.assertEqual(self.client.get(url).status_code, 403, url)
            self.assertEqual(self.post(url, {"quantity": 1}).status_code, 403, url)

    def test_both_roles_can_view_reports(self):
        for email in ["admin@test.com", "pharm@test.com"]:
            self.client = self.app.test_client()
            self.login(email)
            self.assertEqual(self.client.get("/reports").status_code, 200)

    def test_logout_ends_session(self):
        self.login("admin@test.com")
        self.assertEqual(self.client.get("/dashboard").status_code, 200)
        self.post("/logout")
        self.assertEqual(self.client.get("/dashboard").status_code, 302)

    def test_post_without_csrf_token_is_rejected(self):
        self.login("admin@test.com")
        r = self.client.post("/medicines/add", data={"medicine_name": "Hack"})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self.count("medicines"), 0)

    def test_post_with_wrong_csrf_token_is_rejected(self):
        r = self.client.post("/login", data={"email": "admin@test.com", "password": PASSWORD,
                                             "csrf_token": "forged"})
        self.assertEqual(r.status_code, 400)

    def test_logout_via_get_is_not_allowed(self):
        self.login("admin@test.com")
        self.assertEqual(self.client.get("/logout").status_code, 405)
        self.assertEqual(self.client.get("/dashboard").status_code, 200)

    def test_role_portal_enforcement(self):
        # Pharmacist attempting to log in on Admin portal tab is blocked
        r = self.client.post("/login", data={"email": "pharm@test.com", "password": PASSWORD,
                                             "portal_role": "admin", "csrf_token": self.csrf()},
                             follow_redirects=True)
        self.assertIn(b"This account is registered as a Pharmacist", r.data)

        # Admin attempting to log in on Pharmacist portal tab is blocked
        r = self.client.post("/login", data={"email": "admin@test.com", "password": PASSWORD,
                                             "portal_role": "pharmacist", "csrf_token": self.csrf()},
                             follow_redirects=True)
        self.assertIn(b"This account is registered as a Admin", r.data)

        # Correct role portals succeed
        r = self.client.post("/login", data={"email": "admin@test.com", "password": PASSWORD,
                                             "portal_role": "admin", "csrf_token": self.csrf()},
                             follow_redirects=True)
        self.assertIn(b"Dashboard", r.data)
