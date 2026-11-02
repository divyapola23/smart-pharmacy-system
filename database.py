"""Database layer: connection helper and schema creation.

The frontend never touches SQLite directly. Only Flask code (routes and
services) calls get_connection().
"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "pharmacy.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


def get_connection(db_path=None):
    """Open a SQLite connection with foreign keys enforced.

    isolation_level=None puts the connection in autocommit mode so that our
    services can control transactions explicitly with BEGIN / COMMIT / ROLLBACK.
    """
    conn = sqlite3.connect(db_path or DEFAULT_DB_PATH, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=None):
    """Create tables if they do not exist. Never deletes existing data."""
    conn = get_connection(db_path)
    try:
        with open(SCHEMA_PATH, encoding="utf-8") as f:
            conn.executescript(f.read())
    finally:
        conn.close()


class Transaction:
    """Context manager for an explicit database transaction.

    with Transaction(conn):
        ... several statements ...
    Commits if the block finishes, rolls back if it raises.
    """

    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        self.conn.execute("BEGIN IMMEDIATE")
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.conn.execute("COMMIT")
        else:
            self.conn.execute("ROLLBACK")
        return False  # re-raise any exception
