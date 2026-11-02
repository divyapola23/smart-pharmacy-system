import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMG_DIR = r"c:\Users\Deekshita\Downloads\smart-pharmacy-system\smart-pharmacy-system\docs\images"
os.makedirs(IMG_DIR, exist_ok=True)

def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)

    ax.text(5, 7.1, "Entity-Relationship (ER) Diagram - Smart Pharmacy System", ha='center', va='center', fontsize=13, fontweight='bold', color='#113355')

    def draw_entity(x, y, w, h, title, cols, col_bg="#1f497d", body_bg="#ffffff"):
        hdr = patches.Rectangle((x, y + h - 0.4), w, 0.4, ec="#1f497d", fc=col_bg, lw=1.2)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 0.2, title, ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)

        body = patches.Rectangle((x, y), w, h - 0.4, ec="#1f497d", fc=body_bg, lw=1.2)
        ax.add_patch(body)
        c_text = "\n".join(cols)
        ax.text(x + 0.1, y + h - 0.5, c_text, va='top', fontsize=7.2, color="#222222")

    # MEDICINES
    draw_entity(0.5, 4.5, 2.6, 2.2, "MEDICINES",
                ["PK  medicine_id : INT", "    medicine_name : VARCHAR(100)", "    category : VARCHAR(50)", "    manufacturer : VARCHAR(100)"],
                col_bg="#1565c0")

    # INVENTORY
    draw_entity(3.7, 4.2, 2.7, 2.5, "INVENTORY",
                ["PK  inventory_id : INT", "FK  medicine_id : INT", "    batch_no : VARCHAR(50)", "    quantity : INT (CHECK >= 0)",
                 "    purchase_price : DECIMAL", "    selling_price : DECIMAL", "    expiry_date : DATE", "    reorder_level : INT"],
                col_bg="#00695c")

    # USERS
    draw_entity(7.0, 4.5, 2.5, 2.2, "USERS",
                ["PK  user_id : INT", "    name : VARCHAR(100)", "UK  email : VARCHAR(100)", "    password_hash : VARCHAR(255)",
                 "    role : ENUM('admin','pharm')"],
                col_bg="#4527a0")

    # TRANSACTIONS
    draw_entity(1.8, 1.0, 2.9, 2.4, "TRANSACTIONS",
                ["PK  transaction_id : INT", "    transaction_type : ENUM", "FK  inventory_id : INT",
                 "    quantity : INT (CHECK > 0)", "    unit_price : DECIMAL", "    total_amount : DECIMAL",
                 "    transaction_date : DATE", "FK  user_id : INT"],
                col_bg="#c2185b")

    # WASTE_RECORDS
    draw_entity(5.5, 1.0, 2.9, 2.4, "WASTE_RECORDS",
                ["PK  waste_id : INT", "FK  inventory_id : INT", "    quantity : INT (CHECK > 0)",
                 "    reason : ENUM('Expired',...)", "    disposal_date : DATE", "FK  user_id : INT"],
                col_bg="#d84315")

    # Relationships Lines
    # Medicines -> Inventory (1:N)
    ax.annotate('', xy=(3.7, 5.5), xytext=(3.1, 5.5), arrowprops=dict(arrowstyle='->', lw=1.5, color='#1565c0'))
    ax.text(3.4, 5.65, "1:N", ha='center', fontsize=8, fontweight='bold', color='#1565c0')

    # Inventory -> Transactions (1:N)
    ax.annotate('', xy=(3.0, 3.4), xytext=(4.3, 4.2), arrowprops=dict(arrowstyle='->', lw=1.5, color='#00695c'))
    ax.text(3.4, 3.8, "1:N", ha='center', fontsize=8, fontweight='bold', color='#00695c')

    # Inventory -> Waste_records (1:N)
    ax.annotate('', xy=(6.5, 3.4), xytext=(5.6, 4.2), arrowprops=dict(arrowstyle='->', lw=1.5, color='#00695c'))
    ax.text(6.3, 3.8, "1:N", ha='center', fontsize=8, fontweight='bold', color='#00695c')

    # Users -> Transactions (1:N)
    ax.annotate('', xy=(4.7, 2.2), xytext=(7.0, 4.7), arrowprops=dict(arrowstyle='->', lw=1.2, color='#4527a0', ls='--'))
    ax.text(6.0, 3.2, "records (1:N)", ha='center', fontsize=7.5, color='#4527a0')

    # Users -> Waste_records (1:N)
    ax.annotate('', xy=(7.5, 3.4), xytext=(7.8, 4.5), arrowprops=dict(arrowstyle='->', lw=1.2, color='#4527a0', ls='--'))
    ax.text(8.0, 3.9, "authorizes (1:N)", ha='center', fontsize=7.5, color='#4527a0')

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_4_6_er_diagram.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_add_product():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    # Frame
    frame = patches.FancyBboxPatch((0, 0), 10, 5.5, boxstyle="round,pad=0.05", ec="#b0bec5", fc="#f4f7fa", lw=1.5)
    ax.add_patch(frame)
    hdr = patches.Rectangle((0, 5.05), 10, 0.45, ec="#b0bec5", fc="#e0e0e0")
    ax.add_patch(hdr)
    ax.text(1.3, 5.27, "http://127.0.0.1:5000/medicines/add", fontsize=7.5, color="#555555", va='center')

    card = patches.FancyBboxPatch((1.5, 0.5), 7.0, 4.4, boxstyle="round,pad=0.1", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(card)

    ax.text(2.0, 4.5, "Add Medicine to Master Catalogue", fontsize=11, fontweight='bold', color="#113355")

    fields = [
        ("Medicine Name *", "Paracetamol 650mg", 3.8),
        ("Therapeutic Category", "Analgesic / Antipyretic", 3.0),
        ("Manufacturer Name", "Sample Health Pharma", 2.2)
    ]
    for lbl, val, y in fields:
        ax.text(2.0, y + 0.35, lbl, fontsize=8, fontweight='bold', color="#333333")
        f_box = patches.FancyBboxPatch((2.0, y), 6.0, 0.32, boxstyle="round,pad=0.02", ec="#cfd8dc", fc="#ffffff")
        ax.add_patch(f_box)
        ax.text(2.2, y + 0.16, val, fontsize=8, color="#222222", va='center')

    # Save button
    s_btn = patches.FancyBboxPatch((2.0, 1.2), 2.8, 0.4, boxstyle="round,pad=0.03", ec="#1f497d", fc="#1f497d")
    ax.add_patch(s_btn)
    ax.text(3.4, 1.4, "Save Medicine", ha='center', va='center', fontsize=8.5, fontweight='bold', color="white")

    c_btn = patches.FancyBboxPatch((5.1, 1.2), 2.0, 0.4, boxstyle="round,pad=0.03", ec="#9e9e9e", fc="#ffffff")
    ax.add_patch(c_btn)
    ax.text(6.1, 1.4, "Cancel", ha='center', va='center', fontsize=8.5, color="#555555")

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_7_6_add_product.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_transaction_audit():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    # Frame
    frame = patches.FancyBboxPatch((0, 0), 10, 5.5, boxstyle="round,pad=0.05", ec="#b0bec5", fc="#f4f7fa", lw=1.5)
    ax.add_patch(frame)
    hdr = patches.Rectangle((0, 5.05), 10, 0.45, ec="#b0bec5", fc="#e0e0e0")
    ax.add_patch(hdr)
    ax.text(1.3, 5.27, "http://127.0.0.1:5000/transactions", fontsize=7.5, color="#555555", va='center')

    ax.text(0.5, 4.6, "Transaction Audit Logs & Traceability", fontsize=11, fontweight='bold', color="#113355", va='center')

    t_box = patches.FancyBboxPatch((0.5, 0.6), 9.0, 3.8, boxstyle="round,pad=0.05", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(t_box)

    th = patches.Rectangle((0.5, 3.9), 9.0, 0.45, ec="#cfd8dc", fc="#e9eef4")
    ax.add_patch(th)
    ax.text(0.7, 4.12, "Txn ID", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(1.6, 4.12, "Type", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(2.6, 4.12, "Medicine & Batch", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(5.5, 4.12, "Qty", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(6.4, 4.12, "Total ($)", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(7.6, 4.12, "Recorded By", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(8.8, 4.12, "Date", fontsize=7.2, fontweight='bold', color="#37474f", va='center')

    txns = [
        ("4", "Sale", "Paracetamol 500mg (DEMO-PCM-01)", "30", "$75.00", "Pharmacist", "2026-10-21"),
        ("3", "Sale", "Ibuprofen 400mg (DEMO-IBU-01)", "12", "$60.00", "Pharmacist", "2026-10-21"),
        ("2", "Sale", "Amoxicillin 250mg (DEMO-AMX-01)", "10", "$90.00", "Pharmacist", "2026-10-21"),
        ("1", "Purchase", "Paracetamol 500mg (DEMO-PCM-01)", "200", "$300.00", "Pharmacist", "2026-10-21")
    ]
    for idx, (tid, typ, mb, qty, tot, usr, dt) in enumerate(txns):
        y = 3.4 - idx * 0.65
        rb = patches.Rectangle((0.5, y - 0.2), 9.0, 0.65, ec="#eeeeee", fc="#ffffff" if idx%2==0 else "#f8f9fa")
        ax.add_patch(rb)
        ax.text(0.7, y + 0.12, tid, fontsize=7.2, color="#555555", va='center')

        b_col = "#2e7d32" if typ == "Sale" else "#1565c0"
        b_bg = "#e8f5e9" if typ == "Sale" else "#e3f2fd"
        badge = patches.FancyBboxPatch((1.5, y - 0.05), 0.8, 0.3, boxstyle="round,pad=0.02", ec=b_col, fc=b_bg)
        ax.add_patch(badge)
        ax.text(1.9, y + 0.1, typ, fontsize=7, fontweight='bold', color=b_col, ha='center', va='center')

        ax.text(2.6, y + 0.12, mb, fontsize=7.5, color="#112233", va='center')
        ax.text(5.5, y + 0.12, qty, fontsize=7.5, fontweight='bold', color="#112233", va='center')
        ax.text(6.4, y + 0.12, tot, fontsize=7.5, fontweight='bold', color="#112233", va='center')
        ax.text(7.6, y + 0.12, usr, fontsize=7.2, color="#555555", va='center')
        ax.text(8.8, y + 0.12, dt, fontsize=7.2, color="#555555", va='center')

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_7_8_transaction_audit.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

if __name__ == "__main__":
    generate_er_diagram()
    generate_add_product()
    generate_transaction_audit()
