# Test cases with expected and actual results

**Automated run:** `python -m unittest discover -s tests -t . -v` on 12 Oct 2026 (Linux, Python 3.13): **56 tests, all passed.**
"Actual" for manual UI cases is left blank for you to fill in while testing on your own machine and to screenshot.

## A. Automated tests (test file in brackets)
| ID | Scenario | Expected | Actual |
|---|---|---|---|
| TC01 | Valid login [test_auth] | Dashboard shown | Pass |
| TC02 | Wrong password / unknown email [test_auth] | Same "Invalid email or password" message | Pass |
| TC03 | Password stored as hash [test_auth] | Stored value differs from the password | Pass |
| TC04 | Open protected pages logged out [test_auth] | Redirect to /login | Pass |
| TC05 | Pharmacist opens/posts inventory add [test_auth] | 403, no record created | Pass |
| TC06 | Admin opens/posts sale, purchase, waste [test_auth] | 403 | Pass |
| TC07 | Logout [test_auth] | Dashboard no longer accessible | Pass |
| TC08 | POST with missing/wrong CSRF token [test_auth] | 400, nothing saved | Pass |
| TC09 | Add and edit medicine; duplicate; blank name [test_inventory] | Saved / updated; duplicate and blank rejected | Pass |
| TC10 | Search medicine by name and ID [test_inventory] | Correct medicine returned | Pass |
| TC11 | Batch for non-existent medicine; invalid quantity/price/date [test_inventory] | Rejected, no row added | Pass |
| TC12 | Several batches of one medicine; duplicate batch number [test_inventory] | Different batches allowed; duplicate rejected | Pass |
| TC13 | Status labels [test_inventory] | Available, Low Stock, Near Expiry, Expired, Out of Stock | Pass |
| TC14 | Edit batch cannot change quantity [test_inventory] | Quantity unchanged | Pass |
| TC15 | Purchase: stock 50, buy 20 [test_transactions] | Stock 70, total = 20 x price, transaction row saved | Pass |
| TC16 | Purchase new batch / same batch again [test_transactions] | New batch created / quantity added to existing | Pass |
| TC17 | Invalid purchases (qty 0, negative, text, bad price, unknown or expired batch) [test_transactions] | Rejected; stock and transactions unchanged | Pass |
| TC18 | Sale: stock 70, sell 5 [test_transactions] | Stock 65, Sale row saved, total correct | Pass |
| TC19 | Sale of exactly all stock [test_transactions] | Stock 0 | Pass |
| TC20 | Sale more than stock [test_transactions] | "Insufficient stock"; nothing changes | Pass |
| TC21 | Sale from expired batch [test_transactions] | Rejected with "expired" message | Pass |
| TC22 | Sale: qty 0/negative/blank, unknown batch, negative or NaN price [test_transactions] | Rejected | Pass |
| TC23 | Failure midway (stock updated, then insert fails) for sale and purchase [test_transactions] | Rollback: stock unchanged, no raw SQL error shown | Pass |
| TC24 | Database rejects negative stock and type "Refund" [test_transactions] | IntegrityError | Pass |
| TC25 | Waste: stock 65, waste 3 [test_waste] | Stock 62, waste record saved | Pass |
| TC26 | Expired batch listed then written off [test_waste] | Listed; after waste stock 0, history kept | Pass |
| TC27 | Invalid waste (too many, qty <= 0, bad reason, future date, "Expired" on a valid batch) [test_waste] | Rejected; nothing changes | Pass |
| TC28 | Waste failure midway [test_waste] | Rollback | Pass |
| TC29 | Inventory / low-stock / expiry reports [test_reports] | Match database rows and totals | Pass |
| TC30 | Purchase and sales totals (10x3 + 5x4 = 50) [test_reports] | Quantities and values correct | Pass |
| TC31 | Date filter inside and outside range [test_reports] | Rows included / none; totals 0 | Pass |
| TC32 | Invalid dates or report type [test_reports] | Rejected | Pass |
| TC33 | CSV export content and formula-injection protection [test_reports] | Filtered rows only; cells starting with = are neutralised | Pass |
| TC34 | Empty report page [test_reports] | "No records found" message | Pass |

## B. Manual UI cases (fill in "Actual")
| ID | Steps | Expected | Actual |
|---|---|---|---|
| M01 | Login as Admin with wrong password | Red error, stays on login | |
| M02 | Add medicine "Test 500mg" | Appears in list with success message | |
| M03 | Admin adds batch with expiry yesterday | Saved; status Expired; appears on Waste page | |
| M04 | Pharmacist records purchase on an existing batch | Success message shows new stock | |
| M05 | Pharmacist sells more than available | Red error message, stock unchanged | |
| M06 | Pharmacist records waste with reason Expired | Stock reduced; row in waste history | |
| M07 | Reports > Sales with date range > Export CSV | CSV opens in Excel with the same rows | |
| M08 | Resize browser to phone width | Layout stacks; menu still usable | |
| M09 | Double-click the Save button on a form | Only one record created | |

Smoke check done by the author: after loading the demo data and starting the server, every page returned HTTP 200
for the permitted role and 403 for the forbidden role (Linux, 12 Oct 2026). Pages were not visually inspected.
