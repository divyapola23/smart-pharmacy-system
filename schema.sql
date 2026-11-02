-- Smart Pharmacy Inventory and Medicine Waste Management System
-- Database schema (SQLite). Safe to run repeatedly: uses IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('admin', 'pharmacist'))
);

CREATE TABLE IF NOT EXISTS medicines (
    medicine_id   INTEGER PRIMARY KEY,
    medicine_name TEXT NOT NULL,
    category      TEXT,
    manufacturer  TEXT,
    UNIQUE (medicine_name, manufacturer)
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id     INTEGER PRIMARY KEY,
    medicine_id      INTEGER NOT NULL REFERENCES medicines (medicine_id),
    batch_no         TEXT NOT NULL,
    quantity         INTEGER NOT NULL CHECK (quantity >= 0),
    purchase_price   REAL NOT NULL CHECK (purchase_price >= 0),
    selling_price    REAL NOT NULL CHECK (selling_price >= 0),
    manufacture_date TEXT,
    expiry_date      TEXT NOT NULL,
    reorder_level    INTEGER NOT NULL CHECK (reorder_level >= 0),
    UNIQUE (medicine_id, batch_no)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id   INTEGER PRIMARY KEY,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('Purchase', 'Sale')),
    inventory_id     INTEGER NOT NULL REFERENCES inventory (inventory_id),
    quantity         INTEGER NOT NULL CHECK (quantity > 0),
    unit_price       REAL NOT NULL CHECK (unit_price >= 0),
    total_amount     REAL NOT NULL CHECK (total_amount >= 0),
    transaction_date TEXT NOT NULL,
    user_id          INTEGER NOT NULL REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS waste_records (
    waste_id      INTEGER PRIMARY KEY,
    inventory_id  INTEGER NOT NULL REFERENCES inventory (inventory_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    reason        TEXT NOT NULL CHECK (reason IN ('Expired', 'Damaged', 'Recalled', 'Other')),
    disposal_date TEXT NOT NULL,
    user_id       INTEGER NOT NULL REFERENCES users (user_id)
);

CREATE INDEX IF NOT EXISTS idx_medicines_name   ON medicines (medicine_name);
CREATE INDEX IF NOT EXISTS idx_inventory_batch  ON inventory (batch_no);
CREATE INDEX IF NOT EXISTS idx_inventory_expiry ON inventory (expiry_date);
CREATE INDEX IF NOT EXISTS idx_txn_inventory    ON transactions (inventory_id);
CREATE INDEX IF NOT EXISTS idx_txn_date         ON transactions (transaction_date);
CREATE INDEX IF NOT EXISTS idx_waste_inventory  ON waste_records (inventory_id);
CREATE INDEX IF NOT EXISTS idx_waste_date       ON waste_records (disposal_date);
