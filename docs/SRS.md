# Software Requirements Specification
**Project:** Smart Pharmacy Inventory and Medicine Waste Management System

## 1. Abstract
This project is a web-based application that helps a pharmacy keep accurate digital records of
medicines, batch-wise stock, purchases, sales and wasted (expired, damaged, recalled) medicines.
Built with HTML/Bootstrap/JavaScript, Python Flask and SQLite, it updates stock automatically after
every purchase, sale and waste entry, flags low-stock and expired batches, blocks sales of expired
medicine, and produces database-driven reports that can be exported as CSV. Two roles, Admin and
Pharmacist, access the same application with different permissions.

## 2. Problem statement
Manual registers and spreadsheets lead to inaccurate stock counts, missed expiry dates, difficulty
tracing purchases and sales, and incomplete records of wasted medicine. The system replaces them
with centralised records, automatic stock updates, expiry/low-stock identification and reports.

## 3. Aim and objectives
Aim: improve stock accuracy, simplify transactions, track expired/damaged medicine and reduce wastage.
Objectives: maintain medicine details; manage stock per batch; track quantity and expiry; identify low-stock
and expired batches; record purchases and sales in one Transaction module; update inventory automatically;
record waste; generate inventory, purchase, sales and waste reports; role-based secure access; validate all data.

## 4. Scope
In scope: login, roles, medicines, batches, purchase, sale, waste, reports (CSV), dashboard alerts.
Out of scope: patient records, prescriptions, billing/tax, barcode scanning, multi-store, online payments, PDF export, user-management screen, sale returns.

## 5. Users
| Role | Description |
|---|---|
| Admin | Oversees the pharmacy: manages medicines and batches, monitors history, alerts and reports |
| Pharmacist | Daily operations: records purchases, sales and waste, manages medicines, views stock and reports |

## 6. Functional requirements
| ID | Requirement |
|---|---|
| FR1 | Users log in with email and password; passwords are stored hashed; invalid logins show an error |
| FR2 | Users can log out; the session ends |
| FR3 | Unauthenticated users cannot open protected pages; role permissions are enforced on the server |
| FR4 | Add, edit, view and search medicines (ID, name, category, manufacturer); duplicates are blocked |
| FR5 | Add and edit inventory batches linked to an existing medicine; several batches per medicine are allowed |
| FR6 | View inventory with quantity, dates, prices, reorder level; search by medicine name/ID or batch number |
| FR7 | Show status: Available, Low Stock, Near Expiry (30 days), Expired, Out of Stock |
| FR8 | Record a purchase: increases stock of an existing batch or creates a new batch; total = quantity x unit price |
| FR9 | Record a sale: reduces stock; total = quantity x unit price |
| FR10 | Reject sales that exceed stock, use an expired batch, use quantity <= 0, use an unknown batch or an invalid price |
| FR11 | Purchases/sales/waste and the stock change are saved together or not at all |
| FR12 | List expired batches still in stock; record waste with batch, quantity, reason (Expired/Damaged/Recalled/Other), disposal date and user |
| FR13 | Waste reduces stock; waste cannot exceed stock; waste history is kept |
| FR14 | Reports: current inventory, low stock, expiry, purchases, sales, waste, summary; date filters; totals; empty-result message |
| FR15 | Export the displayed report to CSV |
| FR16 | Dashboard shows counts and alerts computed from the database |

## 7. Non-functional requirements
| ID | Requirement |
|---|---|
| NFR1 Security | Hashed passwords, session cookies (HttpOnly, SameSite=Lax), CSRF tokens on all POSTs, parameterised SQL, secret key from environment |
| NFR2 Integrity | Foreign keys on; CHECK constraints (no negative stock, allowed types/reasons/roles); explicit transactions |
| NFR3 Usability | Responsive Bootstrap UI, clear messages and status badges |
| NFR4 Reliability | Errors never expose SQL, stack traces or secrets; history is never deleted |
| NFR5 Portability | Runs locally on Windows with Python and VS Code; no external database server |
| NFR6 Maintainability | Business logic in `services/`, routes in `app.py`, automated tests |

## 8. Permission matrix
| Operation | Admin | Pharmacist |
|---|---|---|
| Login / logout / dashboard | Yes | Yes |
| View medicines, inventory | Yes | Yes |
| Add / edit medicine | Yes | Yes |
| Add / edit inventory batch | Yes | No (adds stock by recording a purchase) |
| View transactions, waste history | Yes | Yes |
| Record purchase / sale / waste | No | Yes |
| Reports and CSV export | Yes | Yes |

## 9. Database (five tables)
`users`, `medicines`, `inventory` (unique medicine_id + batch_no), `transactions` (type Purchase/Sale),
`waste_records`. Exact columns are in `schema.sql` and the ER diagram in `diagrams.md`.

## 10. Report definitions
Total purchased/sold/wasted quantity = sum of quantities in range. Total purchase value / sales value =
sum of total_amount of Purchase / Sale transactions (sales value is revenue, not profit).
Low-stock batch = not expired and quantity <= reorder level. Expired batch = expiry date before today.

## 11. Assumptions and constraints
One pharmacy location; single database file; internet access for the Bootstrap CDN; dates in YYYY-MM-DD;
prices in one currency; development server only.
