"""Create (or reset the password of) a user account from the command line.

Usage (from the project folder, with the virtual environment active):
    python create_user.py                      # asks for details, role defaults to admin
    python create_user.py --role pharmacist    # create a pharmacist
    python create_user.py --reset              # reset the password of an existing user

The password is typed at a hidden prompt. It is never stored in the source code
and is saved only as a hash. There is no default or hardcoded admin password.
"""
import argparse
import getpass
import sqlite3
import sys

from werkzeug.security import generate_password_hash

import database
from services.common import EMAIL_RE

MIN_PASSWORD_LENGTH = 8


def ask_password():
    while True:
        pw = getpass.getpass("Password (min 8 characters): ")
        if len(pw) < MIN_PASSWORD_LENGTH:
            print(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")
            continue
        if pw != getpass.getpass("Confirm password: "):
            print("Passwords do not match.")
            continue
        return pw


def main():
    parser = argparse.ArgumentParser(description="Create or reset a pharmacy user.")
    parser.add_argument("--role", choices=["admin", "pharmacist"], default="admin")
    parser.add_argument("--reset", action="store_true", help="reset an existing user's password")
    parser.add_argument("--db", default=None, help="database path (default: pharmacy.db)")
    args = parser.parse_args()

    database.init_db(args.db)
    conn = database.get_connection(args.db)
    email = input("Email: ").strip().lower()
    if not EMAIL_RE.match(email):
        sys.exit("That does not look like a valid email address.")

    existing = conn.execute("SELECT user_id FROM users WHERE email = ?", (email,)).fetchone()
    if args.reset:
        if not existing:
            sys.exit("No user with that email.")
        conn.execute("UPDATE users SET password_hash = ? WHERE email = ?",
                     (generate_password_hash(ask_password()), email))
        print("Password updated.")
        return
    if existing:
        sys.exit("A user with that email already exists. Use --reset to change the password.")
    name = input("Full name: ").strip()
    if not name:
        sys.exit("Name is required.")
    try:
        conn.execute("INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                     (name, email, generate_password_hash(ask_password()), args.role))
    except sqlite3.Error:
        sys.exit("Could not create the user.")
    print(f"{args.role.capitalize()} account created for {email}.")


if __name__ == "__main__":
    main()
