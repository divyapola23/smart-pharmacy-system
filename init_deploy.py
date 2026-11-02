"""Deployment initializer: automatically creates tables, default demo users, and seed data.
Safe to run multiple times: never overwrites or duplicates existing data.
"""
import os
import sqlite3
from werkzeug.security import generate_password_hash

import database
from seed_demo import main as seed_main

def init_all(db_path=None):
    db_file = db_path or os.environ.get("PHARMACY_DB", database.DEFAULT_DB_PATH)
    print(f"Initializing database at: {db_file}")
    database.init_db(db_file)
    conn = database.get_connection(db_file)

    # 1. Ensure default Admin user exists
    admin_email = "admin@pharmacy.com"
    existing_admin = conn.execute("SELECT user_id FROM users WHERE email = ?", (admin_email,)).fetchone()
    if not existing_admin:
        pw_hash = generate_password_hash("Admin1234!")
        conn.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ("Admin User", admin_email, pw_hash, "admin")
        )
        conn.commit()
        print(f"Created default admin user: {admin_email}")

    # 2. Ensure default Pharmacist user exists
    pharm_email = "pharmacist@pharmacy.com"
    existing_pharm = conn.execute("SELECT user_id FROM users WHERE email = ?", (pharm_email,)).fetchone()
    if not existing_pharm:
        pw_hash = generate_password_hash("Pharmacist1234!")
        conn.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ("Pharmacist User", pharm_email, pw_hash, "pharmacist")
        )
        conn.commit()
        print(f"Created default pharmacist user: {pharm_email}")

    # 3. Seed demo medicines and inventory if not present
    try:
        seed_main()
    except SystemExit as e:
        print(f"Seed status: {e}")

    print("Database ready for deployment!")

if __name__ == "__main__":
    init_all()
