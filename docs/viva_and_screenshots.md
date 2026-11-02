# Viva explanation and screenshot checklist

## 1. One-minute summary
"The Smart Pharmacy system is a Flask web application with an SQLite database. Pharmacists and admins log in,
manage medicines and batch-wise stock, record purchases and sales, write off expired or damaged medicine, and
generate reports. Stock updates automatically and expired medicine cannot be sold."

## 2. Architecture (three layers)
* **Presentation:** HTML, Bootstrap, a little JavaScript (templates/, static/).
* **Application:** Flask (`app.py` routes, login, CSRF, role checks) and `services/` (all business rules).
* **Data:** SQLite file `pharmacy.db`, accessed only through `database.py`. The browser never touches the database.
Flow: Browser -> Flask route -> service function -> SQLite -> back to the page.

## 3. Modules
Authentication and roles; Medicine management; Inventory (batches, status); Transactions (purchase and sale in ONE
table with `transaction_type`); Waste management; Reports (7 types + CSV).

## 4. Database
Five tables: users, medicines, inventory, transactions, waste_records. A medicine has many batches; each batch has many
transactions and waste records; a user records many transactions and waste records. Medicine details are separate from
batch details because one medicine can have several batches with different expiry dates and prices.
Constraints: foreign keys, UNIQUE(medicine_id, batch_no), CHECK(quantity >= 0), allowed values for role/type/reason.

## 5. Key workflows
* **Sale:** check batch exists -> not expired -> quantity <= stock -> BEGIN -> reduce stock -> insert Sale row -> COMMIT.
  Any failure triggers ROLLBACK, so stock and records never disagree.
* **Purchase:** existing batch gets more stock; a new batch creates an inventory row; Purchase row saved in the same transaction.
* **Waste:** validate -> reduce stock -> insert waste record -> COMMIT. Expired batches are only *shown*; a person records the write-off.

## 6. Security (be ready to explain)
Password hashing (Werkzeug), session login, role checks on the server (not just hidden buttons), CSRF tokens, parameterised SQL
(prevents SQL injection), secret key from an environment variable, no default admin password, generic error messages.

## 7. Likely questions
* *Why one transactions table?* Purchase and Sale have identical fields; a type column avoids duplication.
* *Why can't I edit quantity directly?* So every stock change has a history record.
* *Why no delete?* Pharmacy records must be kept; mistakes are corrected with new entries.
* *What does the database transaction do?* All-or-nothing: stock change and record are saved together or not at all.
* *Why SQLite?* Simple, no server to install; fine for a mini project, not for a busy multi-user pharmacy.
* *Is sales value profit?* No. It is revenue; profit would also need cost of goods sold.
* *Limitations?* No returns/reversals, no user-management screen, no lockout, no PDF, development server only.

## 8. Screenshot checklist for the report
1. Login page  2. Login error message  3. Admin dashboard with alerts  4. Medicines list + search
5. Add/edit medicine form  6. Medicine detail  7. Inventory list showing all status badges  8. Add batch form
9. Purchase form  10. Purchase success message  11. Sale form  12. Sale rejected: insufficient stock
13. Sale rejected: expired batch (or batch missing from list)  14. Transactions history  15. Waste page with expired batches
16. Record waste form + success  17. Waste history  18. Report: inventory  19. Report: sales with date filter
20. Report: empty result message  21. Report: summary  22. CSV opened in Excel  23. 403 page for a forbidden action
24. Terminal showing tests passing  25. VS Code project structure  26. Each rendered diagram (block, class, use case, activity,
sequence, component, deployment, ER)
