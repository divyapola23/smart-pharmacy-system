# UML / ER diagrams (PlantUML source)

How to view: install the VS Code extension **PlantUML** (needs Java) and press `Alt+D`, **or** paste a
block (without the code fence) into https://www.plantuml.com/plantuml . Export PNG for your report.
*These were written to match the code and schema but were not rendered by the author; if a diagram does
not render, check the PlantUML syntax version.*

## 1. Block diagram
```plantuml
@startuml
left to right direction
rectangle "Admin / Pharmacist" as users
rectangle "User Interface\n(Browser: HTML, Bootstrap, JS)" as ui
rectangle "Pharmacy Management System (Flask)" as sys {
  rectangle "Medicine\nManagement" as med
  rectangle "Inventory\nManagement" as inv
  rectangle "Transaction\nManagement" as txn
  rectangle "Waste\nManagement" as wst
  rectangle "Report\nGeneration" as rpt
}
database "PharmacyDB\n(SQLite)" as db
rectangle "Output / Reports\n- Updated inventory\n- Purchase and sales records\n- Waste records\n- Generated reports (CSV)" as out
users --> ui
ui --> sys
sys --> db
db --> sys
sys --> out
@enduml
```

## 2. Class diagram (seven conceptual classes)
```plantuml
@startuml
class Admin {
  adminId
  name
  email
  login()
  manageInventory()
  generateReport()
  logout()
}
class Pharmacist {
  pharmacistId
  name
  email
  login()
  recordTransaction()
  recordWaste()
  logout()
}
class Medicine {
  medicineId
  medicineName
  category
  manufacturer
  addMedicine()
  updateMedicine()
  searchMedicine()
}
class Inventory {
  inventoryId
  medicineId
  batchNo
  quantity
  purchasePrice
  sellingPrice
  manufactureDate
  expiryDate
  reorderLevel
  addStock()
  updateStock()
  checkStock()
  checkExpiry()
}
class Transaction {
  transactionId
  transactionType
  transactionDate
  inventoryId
  quantity
  unitPrice
  totalAmount
  addTransaction()
  viewTransactions()
}
class WasteRecord {
  wasteId
  inventoryId
  quantity
  reason
  disposalDate
  recordWaste()
  viewWaste()
}
class Report {
  reportId
  reportType
  generatedDate
  generateReport()
  exportReport()
}
Admin "1" --> "*" Inventory : manages
Pharmacist "1" --> "*" Inventory : updates
Pharmacist "1" --> "*" Transaction : records
Pharmacist "1" --> "*" WasteRecord : records
Inventory "*" --> "1" Medicine : refers to
Inventory "1" --> "*" WasteRecord : has
Transaction "*" --> "1" Inventory : affects
Report ..> Inventory : reads
Report ..> Transaction : reads
Report ..> WasteRecord : reads
@enduml
```
Note: in the code, Admin and Pharmacist are one `users` table with a `role` column. Purchase and Sale are
one `Transaction` class distinguished by `transactionType`.

## 3. Use case diagram
```plantuml
@startuml
left to right direction
actor Admin
actor Pharmacist
rectangle "Smart Pharmacy System" {
  usecase "Login" as UC1
  usecase "Manage Medicines" as UC2
  usecase "Manage Inventory" as UC3
  usecase "View Inventory" as UC4
  usecase "Record Purchase" as UC5
  usecase "Record Sale" as UC6
  usecase "Record Waste" as UC7
  usecase "Track Expiry" as UC8
  usecase "Generate Reports" as UC9
  usecase "Logout" as UC10
  usecase "Update Inventory" as UC11
}
Admin --> UC1
Admin --> UC2
Admin --> UC3
Admin --> UC4
Admin --> UC8
Admin --> UC9
Admin --> UC10
Pharmacist --> UC1
Pharmacist --> UC2
Pharmacist --> UC4
Pharmacist --> UC5
Pharmacist --> UC6
Pharmacist --> UC7
Pharmacist --> UC8
Pharmacist --> UC9
Pharmacist --> UC10
UC5 ..> UC11 : <<include>>
UC6 ..> UC11 : <<include>>
UC7 ..> UC11 : <<include>>
@enduml
```

## 4. Activity diagram
```plantuml
@startuml
start
:Login;
:Verify credentials;
if (Valid login?) then (no)
  :Show error;
  :Return to login;
  detach
else (yes)
endif
if (Role?) then (Admin)
  :Admin operations available;
else (Pharmacist)
  :Pharmacist operations available;
endif
repeat
  :Select operation;
  switch (Operation)
  case (Medicines)
    :Manage medicines;
  case (Inventory)
    :View / manage inventory;
  case (Transactions)
    :Record purchase or sale;
    :Update inventory;
  case (Waste)
    :Record waste;
    :Update inventory;
  case (Reports)
    :Generate / view / export report;
  endswitch
repeat while (Another operation?) is (yes)
->no;
:Logout;
stop
@enduml
```

## 5. Sequence diagram
```plantuml
@startuml
actor Admin
actor Pharmacist
participant System
database Database
Admin -> System : login(email, password)
System -> Database : find user, verify hash
Database --> System : user
System --> Admin : dashboard / error
Admin -> System : add/edit medicine or batch
System -> Database : INSERT / UPDATE
System --> Admin : confirmation
Pharmacist -> System : login(email, password)
System -> Database : find user, verify hash
System --> Pharmacist : dashboard
Pharmacist -> System : record purchase / sale
System -> System : validate (stock, expiry, quantity, price)
System -> Database : BEGIN; UPDATE inventory; INSERT transaction; COMMIT
Database --> System : ok
System --> Pharmacist : confirmation + updated stock
Pharmacist -> System : record waste
System -> System : validate
System -> Database : BEGIN; INSERT waste_record; UPDATE inventory; COMMIT
System --> Pharmacist : confirmation
Admin -> System : request report (type, dates)
System -> Database : SELECT ...
Database --> System : rows
System --> Admin : table / CSV
Admin -> System : logout
Pharmacist -> System : logout
@enduml
```

## 6. Component diagram
```plantuml
@startuml
actor Admin
actor Pharmacist
component "User Interface" as UI
component "Authentication and Role Access" as Auth
component "Medicine Management" as Med
component "Inventory Management" as Inv
component "Transaction Management" as Txn
component "Waste Management" as Wst
component "Report Generation" as Rpt
component "Database Layer (database.py)" as DBL
database "Database (SQLite)" as DB
Admin --> UI
Pharmacist --> UI
UI --> Auth
UI --> Med
UI --> Inv
UI --> Txn
UI --> Wst
UI --> Rpt
Med --> Auth
Inv --> Auth
Txn --> Auth
Wst --> Auth
Rpt --> Auth
Auth --> DBL
Med --> DBL
Inv --> DBL
Txn --> DBL
Wst --> DBL
Rpt --> DBL
Txn ..> Inv : updates stock
Wst ..> Inv : updates stock
DBL --> DB
@enduml
```

## 7. Deployment diagram
```plantuml
@startuml
node "User Computer" {
  artifact "Web Browser" as browser
  artifact "Rendered pages (HTML/CSS/JS)" as pages
}
node "Application Server" {
  artifact "Flask application (app.py)" as flask
  artifact "Templates and static files" as tpl
  component "Authentication" as a1
  component "Medicine Management" as a2
  component "Inventory Management" as a3
  component "Transaction Management" as a4
  component "Waste Management" as a5
  component "Report Generation" as a6
}
node "Database Environment" {
  artifact "PharmacyDB (pharmacy.db, SQLite file)" as db
}
browser --> flask : HTTP (localhost:5000)
flask --> db : sqlite3 file access
@enduml
```
SQLite is an embedded database: no separate database server is needed. When run locally, all three nodes
are the same computer (the Flask process and `pharmacy.db` file sit on the user's machine).

## 8. ER diagram (matches `schema.sql`)
```plantuml
@startuml
hide circle
entity users {
  * user_id : INTEGER <<PK>>
  --
  name : TEXT NOT NULL
  email : TEXT NOT NULL UNIQUE
  password_hash : TEXT NOT NULL
  role : TEXT CHECK (admin, pharmacist)
}
entity medicines {
  * medicine_id : INTEGER <<PK>>
  --
  medicine_name : TEXT NOT NULL
  category : TEXT
  manufacturer : TEXT
  UNIQUE (medicine_name, manufacturer)
}
entity inventory {
  * inventory_id : INTEGER <<PK>>
  --
  medicine_id : INTEGER <<FK>> NOT NULL
  batch_no : TEXT NOT NULL
  quantity : INTEGER CHECK >= 0
  purchase_price : REAL
  selling_price : REAL
  manufacture_date : TEXT
  expiry_date : TEXT NOT NULL
  reorder_level : INTEGER
  UNIQUE (medicine_id, batch_no)
}
entity transactions {
  * transaction_id : INTEGER <<PK>>
  --
  transaction_type : TEXT CHECK (Purchase, Sale)
  inventory_id : INTEGER <<FK>> NOT NULL
  quantity : INTEGER CHECK > 0
  unit_price : REAL
  total_amount : REAL
  transaction_date : TEXT NOT NULL
  user_id : INTEGER <<FK>> NOT NULL
}
entity waste_records {
  * waste_id : INTEGER <<PK>>
  --
  inventory_id : INTEGER <<FK>> NOT NULL
  quantity : INTEGER CHECK > 0
  reason : TEXT CHECK (Expired, Damaged, Recalled, Other)
  disposal_date : TEXT NOT NULL
  user_id : INTEGER <<FK>> NOT NULL
}
medicines ||--o{ inventory : "has batches"
inventory ||--o{ transactions : "has"
inventory ||--o{ waste_records : "has"
users ||--o{ transactions : "records"
users ||--o{ waste_records : "records"
@enduml
```
