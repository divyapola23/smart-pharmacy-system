import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMG_DIR = r"c:\Users\Deekshita\Downloads\smart-pharmacy-system\smart-pharmacy-system\docs\images"
os.makedirs(IMG_DIR, exist_ok=True)

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)

    # Title
    ax.text(5, 6.6, "Three-Tier System Architecture", ha='center', va='center', fontsize=14, fontweight='bold', color='#113355')

    # Tier 1: Presentation Layer
    p1 = patches.FancyBboxPatch((0.8, 4.4), 8.4, 1.7, boxstyle="round,pad=0.2", ec="#1f5560", fc="#eef7f8", lw=1.5)
    ax.add_patch(p1)
    ax.text(1.2, 5.8, "PRESENTATION LAYER (Client Browser)", fontsize=11, fontweight='bold', color="#12343b")
    
    # Tier 1 components
    for i, (title, desc) in enumerate([
        ("Admin Portal", "Role-separated login,\nCatalogue governance"),
        ("Pharmacist Portal", "Counter dispensing,\nPurchase & Waste logs"),
        ("Responsive UI", "Bootstrap 5.3.3,\nHTML5, CSS3, JS"),
        ("Auto-fill & Alerts", "Dynamic notifications\n& quick demonstration")
    ]):
        x = 1.0 + i * 2.05
        box = patches.FancyBboxPatch((x, 4.6), 1.9, 0.95, boxstyle="round,pad=0.1", ec="#546e7a", fc="#ffffff", lw=1)
        ax.add_patch(box)
        ax.text(x + 0.95, 5.25, title, ha='center', va='center', fontsize=9, fontweight='bold', color="#113355")
        ax.text(x + 0.95, 4.85, desc, ha='center', va='center', fontsize=7.5, color="#555555")

    # Arrow Tier 1 <-> Tier 2
    ax.annotate('', xy=(5, 4.4), xytext=(5, 3.8), arrowprops=dict(arrowstyle='<->', lw=2, color='#1f5560'))
    ax.text(5.2, 4.1, "HTTP / HTTPS RESTful Requests & CSRF Protected Forms", fontsize=8, color="#1f5560", fontweight='semibold')

    # Tier 2: Application Layer
    p2 = patches.FancyBboxPatch((0.8, 1.9), 8.4, 1.8, boxstyle="round,pad=0.2", ec="#1f497d", fc="#f0f4f9", lw=1.5)
    ax.add_patch(p2)
    ax.text(1.2, 3.4, "APPLICATION LAYER (Flask Web Framework)", fontsize=11, fontweight='bold', color="#1f497d")

    # Tier 2 components
    for i, (title, desc) in enumerate([
        ("app.py Controller", "Route dispatching,\nSession & CSRF guard"),
        ("Inventory Service", "Medicine master,\nbatch status evaluation"),
        ("Transaction Service", "Atomic purchase/sale,\nstock deduction locks"),
        ("Report & Waste Service", "Sales Count intelligence,\nwaste write-offs, CSV")
    ]):
        x = 1.0 + i * 2.05
        box = patches.FancyBboxPatch((x, 2.1), 1.9, 1.05, boxstyle="round,pad=0.1", ec="#546e7a", fc="#ffffff", lw=1)
        ax.add_patch(box)
        ax.text(x + 0.95, 2.85, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#1f497d")
        ax.text(x + 0.95, 2.4, desc, ha='center', va='center', fontsize=7.5, color="#555555")

    # Arrow Tier 2 <-> Tier 3
    ax.annotate('', xy=(5, 1.9), xytext=(5, 1.3), arrowprops=dict(arrowstyle='<->', lw=2, color='#1f497d'))
    ax.text(5.2, 1.6, "ACID Transactions (BEGIN IMMEDIATE ... COMMIT/ROLLBACK)", fontsize=8, color="#1f497d", fontweight='semibold')

    # Tier 3: Data Layer
    p3 = patches.FancyBboxPatch((0.8, 0.2), 8.4, 1.05, boxstyle="round,pad=0.2", ec="#2e7d32", fc="#f1f8e9", lw=1.5)
    ax.add_patch(p3)
    ax.text(1.2, 1.0, "DATA LAYER (Embedded SQLite Database)", fontsize=11, fontweight='bold', color="#2e7d32")

    for i, (title, desc) in enumerate([
        ("users table", "Credentials & Roles"),
        ("medicines table", "Master drug info"),
        ("inventory table", "Batches & Expiry"),
        ("transactions table", "Purchases & Sales"),
        ("waste_records table", "Disposal & Reasons")
    ]):
        x = 1.0 + i * 1.62
        box = patches.FancyBboxPatch((x, 0.35), 1.5, 0.55, boxstyle="round,pad=0.08", ec="#81c784", fc="#ffffff", lw=1)
        ax.add_patch(box)
        ax.text(x + 0.75, 0.68, title, ha='center', va='center', fontsize=8, fontweight='bold', color="#1b5e20")
        ax.text(x + 0.75, 0.48, desc, ha='center', va='center', fontsize=7, color="#555555")

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_4_2_system_architecture.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)

    ax.text(5, 8.2, "Smart Pharmacy System Use Case Diagram", ha='center', va='center', fontsize=14, fontweight='bold', color='#113355')

    # Boundary box
    boundary = patches.FancyBboxPatch((2.6, 0.4), 4.8, 7.4, boxstyle="square,pad=0.1", ec="#1f497d", fc="#fdfdfd", lw=2)
    ax.add_patch(boundary)
    ax.text(5, 7.55, "Smart Pharmacy System Boundary", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#1f497d")

    # Actors
    # Admin (Left)
    ax.plot([1.2, 1.2], [5.6, 6.0], color="#113355", lw=2) # body
    ax.plot([0.9, 1.5], [5.8, 5.8], color="#113355", lw=2) # arms
    ax.plot([1.2, 0.9], [5.6, 5.1], color="#113355", lw=2) # left leg
    ax.plot([1.2, 1.5], [5.6, 5.1], color="#113355", lw=2) # right leg
    c_admin = patches.Circle((1.2, 6.25), 0.25, ec="#113355", fc="#cfe3e6", lw=2)
    ax.add_patch(c_admin)
    ax.text(1.2, 4.8, "Administrator", ha='center', va='center', fontsize=10, fontweight='bold', color="#113355")

    # Pharmacist (Right)
    ax.plot([8.8, 8.8], [5.6, 6.0], color="#2e7d32", lw=2)
    ax.plot([8.5, 9.1], [5.8, 5.8], color="#2e7d32", lw=2)
    ax.plot([8.8, 8.5], [5.6, 5.1], color="#2e7d32", lw=2)
    ax.plot([8.8, 9.1], [5.6, 5.1], color="#2e7d32", lw=2)
    c_pharm = patches.Circle((8.8, 6.25), 0.25, ec="#2e7d32", fc="#dcedc8", lw=2)
    ax.add_patch(c_pharm)
    ax.text(8.8, 4.8, "Pharmacist", ha='center', va='center', fontsize=10, fontweight='bold', color="#2e7d32")

    use_cases = [
        ("Login via Role Portal", 7.0, ["admin", "pharm"]),
        ("Manage Medicines Catalogue", 6.3, ["admin", "pharm"]),
        ("Add / Edit Inventory Batches", 5.6, ["admin"]),
        ("View Inventory & Alerts", 4.9, ["admin", "pharm"]),
        ("Record Purchase", 4.2, ["pharm"]),
        ("Record Sale (Dispensing)", 3.5, ["pharm"]),
        ("Record Waste Write-off", 2.8, ["pharm"]),
        ("Track Expiry & Low Stock", 2.1, ["admin", "pharm"]),
        ("Generate Reports & Export CSV", 1.4, ["admin", "pharm"]),
        ("Sales Count per Medicine", 0.7, ["admin"])
    ]

    for uc_text, y, roles in use_cases:
        ellipse = patches.Ellipse((5, y), 3.8, 0.55, ec="#1f497d", fc="#eef4fa", lw=1.2)
        ax.add_patch(ellipse)
        ax.text(5, y, uc_text, ha='center', va='center', fontsize=8.5, fontweight='semibold', color="#112233")

        if "admin" in roles:
            ax.plot([1.5, 3.1], [5.8, y], color="#455a64", lw=1.2, ls="--")
        if "pharm" in roles:
            ax.plot([8.5, 6.9], [5.8, y], color="#2e7d32", lw=1.2, ls="--")

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_4_4_use_case_diagram.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)

    ax.text(5, 8.2, "Smart Pharmacy System Class Diagram", ha='center', va='center', fontsize=14, fontweight='bold', color='#113355')

    def draw_class(x, y, w, h, name, attrs, methods):
        # header
        hdr = patches.Rectangle((x, y + h - 0.4), w, 0.4, ec="#1f497d", fc="#1f497d", lw=1.2)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 0.2, name, ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        # body
        body = patches.Rectangle((x, y), w, h - 0.4, ec="#1f497d", fc="#ffffff", lw=1.2)
        ax.add_patch(body)
        
        # attributes
        attr_text = "\n".join(attrs)
        ax.text(x + 0.1, y + h - 0.5, attr_text, va='top', fontsize=7.2, color="#222222")

        # divider
        div_y = y + len(methods) * 0.18 + 0.1
        ax.plot([x, x + w], [div_y, div_y], color="#b0bec5", lw=0.8)

        # methods
        meth_text = "\n".join(methods)
        ax.text(x + 0.1, div_y - 0.08, meth_text, va='top', fontsize=7.2, color="#004d40")

    # Medicine
    draw_class(0.4, 5.0, 2.6, 2.6, "Medicine",
               ["- medicine_id: int", "- medicine_name: str", "- category: str", "- manufacturer: str"],
               ["+ add_medicine()", "+ update_medicine()", "+ get_medicine()", "+ list_medicines()"])

    # Inventory
    draw_class(3.7, 5.0, 2.7, 2.6, "Inventory",
               ["- inventory_id: int", "- medicine_id: int [FK]", "- batch_no: str", "- quantity: int",
                "- purchase_price: float", "- selling_price: float", "- expiry_date: date", "- reorder_level: int"],
               ["+ get_status()", "+ add_batch()", "+ check_stock()", "+ check_expiry()"])

    # User
    draw_class(7.0, 5.0, 2.6, 2.6, "User",
               ["- user_id: int", "- name: str", "- email: str", "- password_hash: str", "- role: str"],
               ["+ login(email, pwd)", "+ logout()", "+ check_permission()"])

    # Transaction
    draw_class(0.8, 1.4, 2.6, 2.6, "Transaction",
               ["- transaction_id: int", "- transaction_type: str", "- inventory_id: int [FK]",
                "- quantity: int", "- unit_price: float", "- total_amount: float", "- user_id: int [FK]"],
               ["+ record_purchase()", "+ record_sale()", "+ list_transactions()"])

    # WasteRecord
    draw_class(3.9, 1.4, 2.6, 2.6, "WasteRecord",
               ["- waste_id: int", "- inventory_id: int [FK]", "- quantity: int", "- reason: str",
                "- disposal_date: date", "- user_id: int [FK]"],
               ["+ record_waste()", "+ list_waste()"])

    # ReportService
    draw_class(7.0, 1.4, 2.6, 2.6, "ReportService",
               ["- report_types: dict", "- date_filters: tuple"],
               ["+ dashboard_stats()", "+ sales_per_medicine()", "+ generate_report()", "+ report_to_csv()"])

    # Relationships
    ax.annotate("1..*  contains", xy=(3.7, 6.3), xytext=(3.0, 6.3), arrowprops=dict(arrowstyle='<-', lw=1.2, color='#1f497d'))
    ax.annotate("1..*  affects", xy=(2.1, 4.0), xytext=(4.3, 5.0), arrowprops=dict(arrowstyle='->', lw=1.2, color='#1f497d'))
    ax.annotate("1..*  generates", xy=(5.0, 4.0), xytext=(5.0, 5.0), arrowprops=dict(arrowstyle='->', lw=1.2, color='#1f497d'))
    ax.annotate("records", xy=(7.0, 5.8), xytext=(3.4, 2.7), arrowprops=dict(arrowstyle='<-', lw=1.2, color='#1f497d', ls=':'))
    ax.annotate("authorizes", xy=(7.0, 5.4), xytext=(6.5, 2.7), arrowprops=dict(arrowstyle='<-', lw=1.2, color='#1f497d', ls=':'))
    ax.annotate("reads", xy=(7.5, 4.0), xytext=(7.5, 5.0), arrowprops=dict(arrowstyle='->', lw=1.2, color='#004d40', ls='--'))

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_4_5_class_diagram.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(9, 8.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    ax.text(5, 9.6, "Smart Pharmacy System Activity Diagram", ha='center', va='center', fontsize=14, fontweight='bold', color='#113355')

    # Initial node
    c_start = patches.Circle((5, 9.0), 0.16, fc="#113355", ec="#113355")
    ax.add_patch(c_start)

    def draw_step(y, text, h=0.45, w=3.4, fc="#eef4fa", ec="#1f497d", font_size=8.5):
        box = patches.FancyBboxPatch((5 - w/2, y - h/2), w, h, boxstyle="round,pad=0.1", ec=ec, fc=fc, lw=1.2)
        ax.add_patch(box)
        ax.text(5, y, text, ha='center', va='center', fontsize=font_size, fontweight='semibold', color="#112233")

    def draw_decision(y, text):
        diamond = patches.Polygon([[5, y + 0.35], [5 + 1.2, y], [5, y - 0.35], [5 - 1.2, y]], ec="#e65100", fc="#fff3e0", lw=1.2)
        ax.add_patch(diamond)
        ax.text(5, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color="#bf360c")

    draw_step(8.3, "Select Role Portal (Admin / Pharmacist)")
    ax.annotate('', xy=(5, 8.05), xytext=(5, 8.84), arrowprops=dict(arrowstyle='->', lw=1.2))

    draw_step(7.4, "Submit Credentials & CSRF Token")
    ax.annotate('', xy=(5, 7.15), xytext=(5, 8.05), arrowprops=dict(arrowstyle='->', lw=1.2))

    draw_decision(6.4, "Valid Login?")
    ax.annotate('', xy=(5, 6.75), xytext=(5, 7.15), arrowprops=dict(arrowstyle='->', lw=1.2))

    # Invalid path
    ax.annotate('No: Flash Error', xy=(8.2, 8.3), xytext=(6.2, 6.4), arrowprops=dict(arrowstyle='->', lw=1.2, color='#c62828'))
    
    # Valid path -> Role check
    ax.annotate('Yes: Match Role', xy=(5, 5.5), xytext=(5, 6.05), arrowprops=dict(arrowstyle='->', lw=1.2, color='#2e7d32'))
    draw_step(5.2, "Establish Session & Load Dashboard")

    draw_decision(4.2, "Select Operation")
    ax.annotate('', xy=(5, 4.55), xytext=(5, 4.95), arrowprops=dict(arrowstyle='->', lw=1.2))

    # Operations
    draw_step(3.0, "Dispense Medicine (Sale)", w=2.4, fc="#e8f5e9", ec="#2e7d32")
    draw_step(3.0, "Batch & Stock Mgmt", w=2.4, fc="#e1f5fe", ec="#0288d1")
    # shift left/right
    box1 = patches.FancyBboxPatch((1.0, 2.75), 2.5, 0.5, boxstyle="round,pad=0.1", ec="#2e7d32", fc="#e8f5e9", lw=1.2)
    ax.add_patch(box1)
    ax.text(2.25, 3.0, "Dispense Sale (Pharmacist)", ha='center', va='center', fontsize=8, fontweight='semibold')

    box2 = patches.FancyBboxPatch((3.75, 2.75), 2.5, 0.5, boxstyle="round,pad=0.1", ec="#0288d1", fc="#e1f5fe", lw=1.2)
    ax.add_patch(box2)
    ax.text(5.0, 3.0, "Manage Batches (Admin)", ha='center', va='center', fontsize=8, fontweight='semibold')

    box3 = patches.FancyBboxPatch((6.5, 2.75), 2.7, 0.5, boxstyle="round,pad=0.1", ec="#7b1fa2", fc="#f3e5f5", lw=1.2)
    ax.add_patch(box3)
    ax.text(7.85, 3.0, "Sales Count Intelligence", ha='center', va='center', fontsize=8, fontweight='semibold')

    ax.annotate('', xy=(2.25, 3.3), xytext=(4.2, 4.0), arrowprops=dict(arrowstyle='->', lw=1))
    ax.annotate('', xy=(5.0, 3.3), xytext=(5.0, 3.85), arrowprops=dict(arrowstyle='->', lw=1))
    ax.annotate('', xy=(7.85, 3.3), xytext=(5.8, 4.0), arrowprops=dict(arrowstyle='->', lw=1))

    # Validation & atomic execution
    draw_step(1.8, "Validate Expiry & Shelf Stock (Server-Side Rules)")
    ax.annotate('', xy=(5, 2.05), xytext=(2.25, 2.75), arrowprops=dict(arrowstyle='->', lw=1))
    ax.annotate('', xy=(5, 2.05), xytext=(5.0, 2.75), arrowprops=dict(arrowstyle='->', lw=1))
    ax.annotate('', xy=(5, 2.05), xytext=(7.85, 2.75), arrowprops=dict(arrowstyle='->', lw=1))

    draw_step(0.9, "Execute Atomic Transaction (UPDATE Stock + INSERT Audit Row)")
    ax.annotate('', xy=(5, 1.15), xytext=(5, 1.55), arrowprops=dict(arrowstyle='->', lw=1.2))

    # Final node
    c_end_outer = patches.Circle((5, 0.25), 0.20, fc="none", ec="#113355", lw=1.5)
    c_end_inner = patches.Circle((5, 0.25), 0.12, fc="#113355", ec="#113355")
    ax.add_patch(c_end_outer)
    ax.add_patch(c_end_inner)
    ax.annotate('', xy=(5, 0.45), xytext=(5, 0.65), arrowprops=dict(arrowstyle='->', lw=1.2))

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_4_6_activity_diagram.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_sequence_diagrams():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)

    ax.text(5, 8.1, "Sequence Diagram: Pharmacist Dispensing & Admin Sales Count", ha='center', va='center', fontsize=13, fontweight='bold', color='#113355')

    lifelines = [
        ("Pharmacist / Admin", 1.2),
        ("Web Browser (UI)", 3.4),
        ("Flask (app.py)", 5.6),
        ("Service Layer", 7.6),
        ("SQLite DB", 9.2)
    ]

    for name, x in lifelines:
        box = patches.FancyBboxPatch((x - 0.9, 7.3), 1.8, 0.5, boxstyle="round,pad=0.1", ec="#1f497d", fc="#eef4fa", lw=1.2)
        ax.add_patch(box)
        ax.text(x, 7.55, name, ha='center', va='center', fontsize=8, fontweight='bold', color="#1f497d")
        ax.plot([x, x], [0.8, 7.3], color="#90a4ae", lw=1, ls="--")

    # Sequence steps
    steps = [
        (6.8, 1.2, 3.4, "1. Select batch & enter quantity", True),
        (6.3, 3.4, 5.6, "2. POST /transactions/sale (form, csrf)", True),
        (5.8, 5.6, 7.6, "3. record_sale(conn, user_id, form)", True),
        (5.3, 7.6, 9.2, "4. Check expiry & available stock", True),
        (4.8, 9.2, 7.6, "5. Return stock valid (not expired)", False),
        (4.3, 7.6, 9.2, "6. BEGIN; UPDATE stock; INSERT txn; COMMIT", True),
        (3.8, 9.2, 7.6, "7. Transaction confirmed", False),
        (3.3, 7.6, 5.6, "8. Return success payload", False),
        (2.8, 5.6, 3.4, "9. 302 Redirect /dashboard with Flash", False),
        (2.3, 3.4, 5.6, "10. Admin: GET /dashboard", True),
        (1.8, 5.6, 7.6, "11. sales_per_medicine(conn)", True),
        (1.3, 7.6, 3.4, "12. Render Sales Count Table & Metrics", False)
    ]

    for y, x1, x2, msg, is_call in steps:
        ls = '-' if is_call else '--'
        c = '#1f497d' if is_call else '#2e7d32'
        ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle='->', lw=1.2, color=c, ls=ls))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 0.12, msg, ha='center', va='bottom', fontsize=7.2, fontweight='semibold', color=c)

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_4_7_sequence_diagram.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

if __name__ == "__main__":
    generate_architecture_diagram()
    generate_use_case_diagram()
    generate_class_diagram()
    generate_activity_diagram()
    generate_sequence_diagrams()
