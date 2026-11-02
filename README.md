# Smart Pharmacy Inventory and Medicine Waste Management System

A Flask + SQLite web application for a college Software Engineering mini project.
It manages medicines, batch-level inventory, purchases, sales, waste records and reports,
with two roles (Admin, Pharmacist).

> **Status / honesty note.** The automated tests (56) pass and every page was requested
> successfully as both roles on Linux (Python 3.13). It has **not** been run on Windows or in
> VS Code by the author of this code, and the pages were not checked visually in a browser.
> The Flask development server is for local use only; this is a learning project, **not**
> production pharmacy software (see "Limitations").

---

## 1. Install or verify Python (Windows)

1. Open **Command Prompt** or the VS Code terminal and run `python --version`.
2. If you see `Python 3.10` or newer, continue. Otherwise install it from https://www.python.org/downloads/
   and **tick "Add python.exe to PATH"** on the first installer screen.

## 2. Get the project folder

Unzip `smart-pharmacy-system.zip`, then in VS Code: **File > Open Folder** and choose `smart-pharmacy-system`.
Open a terminal in VS Code: **Terminal > New Terminal**.

## 3. Create and activate a virtual environment

```bat
python -m venv .venv
.venv\Scripts\activate
```
Your prompt should now start with `(.venv)`.
If PowerShell blocks activation: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then retry.
In VS Code press **Ctrl+Shift+P > Python: Select Interpreter** and pick the `.venv` one.

## 4. Install dependencies

```bat
pip install -r requirements.txt
```
(`requirements.txt` contains only `Flask`. Python's `sqlite3` and Werkzeug hashing are already included.)

## 5. Set a secret key (recommended)

The secret key signs login sessions. Do not write it in the source code.
```bat
set SECRET_KEY=type-a-long-random-string-here
```
(PowerShell: `$env:SECRET_KEY="type-a-long-random-string-here"`.)
If you skip this, a random temporary key is used and you are logged out every time the server restarts.

## 6. Create the database

The database (`pharmacy.db`) and all five tables are created automatically, **without deleting
anything**, the first time you run any of the commands below. The schema is in `schema.sql`.

## 7. Create the first Admin (and a Pharmacist)

```bat
python create_user.py
python create_user.py --role pharmacist
```
You type the email, name and a hidden password (minimum 8 characters). There is no default password.
To reset a forgotten password: `python create_user.py --reset`.

## 8. (Optional) Load demo data

```bat
python seed_demo.py
```
Adds 4 medicines, several `DEMO-` batches (including one near expiry, one low stock, one expired),
sales, purchases and waste records. Running it a second time does nothing.

## 9. Run the application

```bat
python app.py
```
Open http://127.0.0.1:5000 and log in. Stop the server with **Ctrl+C**.
(Alternative: `flask --app app run`.) Another port: `flask --app app run --port 5001`.

## 10. Run the tests

```bat
python -m unittest discover -s tests -t . -v
```
Tests use a temporary database each time, so your real `pharmacy.db` is never touched.

## 11. What to test by hand, module by module

| Module | Try this |
|---|---|
| Login | Wrong password shows an error; open `/dashboard` while logged out and you are sent to login |
| Roles | Pharmacist opening `/inventory/add` gets "403"; Admin opening `/transactions/sale` gets "403" |
| Medicines | Add, search by name and by ID, edit, view a medicine |
| Inventory | Admin adds a batch; check Low Stock / Near Expiry / Expired badges; search by batch number |
| Purchase | Pharmacist: pick an existing batch, buy 20, stock goes up by 20 |
| Sale | Sell 5, stock goes down by 5; try selling more than stock or from an expired batch (rejected) |
| Waste | Record waste of an expired batch (reason "Expired"); stock drops, history row appears |
| Reports | Choose each report, apply dates, click **Export CSV** and open it in Excel |

## 12. Routes

| Route | Methods | Who |
|---|---|---|
| `/login` | GET, POST | everyone |
| `/logout` | **POST** (button in sidebar) | logged in |
| `/dashboard` | GET | logged in |
| `/medicines`, `/medicines/<id>` | GET | logged in |
| `/medicines/add`, `/medicines/<id>/edit` | GET, POST | Admin, Pharmacist |
| `/inventory` | GET | logged in |
| `/inventory/add`, `/inventory/<id>/edit` | GET, POST | Admin |
| `/transactions` | GET | Admin, Pharmacist |
| `/transactions/purchase`, `/transactions/sale` | GET, POST | Pharmacist |
| `/waste` | GET | Admin, Pharmacist |
| `/waste/add` | GET, POST | Pharmacist |
| `/reports`, `/reports/export` | GET | Admin, Pharmacist |

Deviation from the brief: logout is POST (with CSRF token), not GET, so a malicious link cannot log you out.

## 13. Business rules worth remembering

* Quantity is **never edited directly**. It changes only via purchase, sale or waste, so history is complete.
  (The one exception: opening stock typed when an Admin first adds a batch.)
* Purchase of an existing medicine+batch adds to that batch and updates its purchase price to the latest price paid.
* A sale defaults to the batch selling price; a different unit price may be typed.
* Expired batches cannot be sold or purchased. They are listed on the Waste page; a Pharmacist records the write-off.
* Waste reason "Expired" is only accepted for a batch that is actually expired.
* Status labels: Expired (expiry before today) > Out of Stock > Low Stock (qty <= reorder level) > Near Expiry (within 30 days) > Available.
* Total sales value is revenue, **not** profit.
* There are no delete buttons: transaction and waste history is never removed.
  A mistaken entry would need a corrective entry (for example a waste record). A formal reversal feature is not implemented.
* Admin cannot record purchases/sales/waste (matches the use-case diagram). User accounts are managed with `create_user.py`.

## 14. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Activate the venv (`.venv\Scripts\activate`) and run `pip install -r requirements.txt` |
| VS Code shows import warnings / uses the wrong Python | Ctrl+Shift+P > *Python: Select Interpreter* > choose `.venv` |
| `'python' is not recognized` | Reinstall Python with "Add to PATH", or try `py` instead of `python` |
| "Database file not found" | Run `python create_user.py` or `python app.py` once from the project folder; the file is created there |
| `TemplateNotFound` | Run from inside `smart-pharmacy-system`; make sure the `templates` folder has all `.html` files |
| Page has no styling | CSS/JS use Bootstrap from a CDN, so internet is needed; also check `static/css/style.css` exists |
| `FOREIGN KEY constraint failed` | You referenced a medicine/batch/user that does not exist; add the medicine first |
| `Address already in use` | Another program uses port 5000: `flask --app app run --port 5001` |
| Keeps logging you out / "form expired" (400) | Set `SECRET_KEY` before starting; make sure browser cookies are on; reload the page and resubmit |
| Login fails for a new account | Passwords are case-sensitive; reset with `python create_user.py --reset` |

## 15. Back up the database

Stop the server, then:
```bat
mkdir backups
copy pharmacy.db backups\pharmacy_backup.db
```
Restore by copying the backup over `pharmacy.db`. Make backups before demos.

## 16. Limitations (important for real-world use)

* Single-location, no patient records, no prescriptions, no tax/GST, no barcode scanning.
* No formal sale reversal/return feature, no user-management screen, no password-change screen.
* No login rate-limiting or account lockout; no audit log beyond the transaction and waste tables.
* No PDF export (CSV only). Bootstrap is loaded from a CDN.
* Flask's built-in server and SQLite file are fine for a demo, not for a busy multi-user pharmacy.
  A real deployment needs HTTPS (`SESSION_COOKIE_SECURE=1`), a production server, backups and a security review.

## 17. Project structure

```
smart-pharmacy-system/
  app.py            routes, login/session, CSRF, role checks
  database.py       SQLite connection + transaction helper
  schema.sql        the five tables
  create_user.py    safe admin/pharmacist creation and password reset
  seed_demo.py      optional demo data
  requirements.txt
  services/         business logic (inventory, transaction, waste, report, common)
  templates/        HTML pages (base.html + one per module)
  static/           css/style.css, js/script.js, images/
  tests/            automated tests (unittest)
  docs/             SRS, diagrams, test cases, viva notes
```

## 18. Suggested build order (if you type it yourself)

1. `requirements.txt`, `schema.sql`, `database.py` -> run `python -c "import database; database.init_db()"`.
2. `services/common.py` (validation helpers).
3. `app.py` with login, logout, CSRF, `login_required`, `roles_required`; `base.html`, `login.html`, `dashboard.html`; `create_user.py`.
4. `services/inventory_service.py` + medicine/inventory routes and templates.
5. `services/transaction_service.py` + purchase/sale routes and templates.
6. `services/waste_service.py` + waste routes and templates.
7. `services/report_service.py` + reports route/template + CSV export.
8. Tests after each step, then `seed_demo.py`, then the docs.
