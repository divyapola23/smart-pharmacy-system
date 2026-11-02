import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMG_DIR = r"c:\Users\Deekshita\Downloads\smart-pharmacy-system\smart-pharmacy-system\docs\images"
os.makedirs(IMG_DIR, exist_ok=True)

def draw_browser_frame(ax, title="Smart Pharmacy System - Web Browser", w=10, h=6.5):
    # Outer frame
    frame = patches.FancyBboxPatch((0, 0), w, h, boxstyle="round,pad=0.05", ec="#b0bec5", fc="#f4f7fa", lw=1.5)
    ax.add_patch(frame)
    # Header bar
    hdr = patches.Rectangle((0, h - 0.45), w, 0.45, ec="#b0bec5", fc="#e0e0e0")
    ax.add_patch(hdr)
    # Window controls
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        dot = patches.Circle((0.25 + i * 0.22, h - 0.22), 0.08, fc=c, ec=c)
        ax.add_patch(dot)
    # URL bar
    url_box = patches.FancyBboxPatch((1.2, h - 0.35), w - 2.5, 0.25, boxstyle="round,pad=0.03", ec="#cccccc", fc="#ffffff")
    ax.add_patch(url_box)
    ax.text(1.3, h - 0.23, "http://127.0.0.1:5000" + title.split("-")[-1].strip(), fontsize=7.5, color="#555555", va='center')

def generate_fig_7_1():
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)

    draw_browser_frame(ax, "Smart Pharmacy System - /login/admin")

    # Center card
    card = patches.FancyBboxPatch((2.2, 0.5), 5.6, 5.0, boxstyle="round,pad=0.15", ec="#cfd8dc", fc="#ffffff", lw=1.2)
    ax.add_patch(card)

    ax.text(5.0, 5.15, "⚚ Smart Pharmacy", ha='center', va='center', fontsize=14, fontweight='bold', color="#113355")
    ax.text(5.0, 4.85, "Inventory & Medicine Waste Management System", ha='center', va='center', fontsize=8, color="#546e7a")

    # Role Tabs
    tab_bg = patches.FancyBboxPatch((2.5, 4.2), 5.0, 0.42, boxstyle="round,pad=0.05", ec="#e0e0e0", fc="#eef2f6")
    ax.add_patch(tab_bg)
    
    t_admin = patches.FancyBboxPatch((2.55, 4.23), 2.4, 0.36, boxstyle="round,pad=0.05", ec="#1f497d", fc="#1f497d")
    ax.add_patch(t_admin)
    ax.text(3.75, 4.41, "🛡️ Admin Portal", ha='center', va='center', fontsize=8, fontweight='bold', color="white")

    ax.text(6.25, 4.41, "💊 Pharmacist Portal", ha='center', va='center', fontsize=8, fontweight='bold', color="#555555")

    # Form Fields
    ax.text(2.6, 3.85, "Admin Email", fontsize=8, fontweight='bold', color="#333333")
    f_email = patches.FancyBboxPatch((2.6, 3.4), 4.8, 0.35, boxstyle="round,pad=0.03", ec="#b0bec5", fc="#ffffff")
    ax.add_patch(f_email)
    ax.text(2.8, 3.58, "admin@pharmacy.com", fontsize=8, color="#222222", va='center')

    ax.text(2.6, 3.1, "Password", fontsize=8, fontweight='bold', color="#333333")
    f_pass = patches.FancyBboxPatch((2.6, 2.65), 4.8, 0.35, boxstyle="round,pad=0.03", ec="#b0bec5", fc="#ffffff")
    ax.add_patch(f_pass)
    ax.text(2.8, 2.83, "••••••••••••", fontsize=8, color="#222222", va='center')

    # Login Button
    btn = patches.FancyBboxPatch((2.6, 2.05), 4.8, 0.42, boxstyle="round,pad=0.05", ec="#1f497d", fc="#1f497d")
    ax.add_patch(btn)
    ax.text(5.0, 2.26, "Log In as Administrator", ha='center', va='center', fontsize=9, fontweight='bold', color="white")

    # Demo credentials pill
    demo_box = patches.FancyBboxPatch((2.6, 1.45), 4.8, 0.45, boxstyle="round,pad=0.04", ec="#e0e0e0", fc="#f8f9fa")
    ax.add_patch(demo_box)
    ax.text(2.75, 1.68, "Demo: admin@pharmacy.com / Admin1234!", fontsize=7, color="#555555", va='center')
    af_btn = patches.FancyBboxPatch((6.3, 1.53), 1.0, 0.28, boxstyle="round,pad=0.02", ec="#1f497d", fc="#ffffff")
    ax.add_patch(af_btn)
    ax.text(6.8, 1.67, "Auto Fill", ha='center', va='center', fontsize=7, fontweight='bold', color="#1f497d")

    # Download report buttons footer
    ax.text(5.0, 1.15, "📄 Download Official Project Report", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#78909c")
    b_pdf = patches.FancyBboxPatch((2.7, 0.65), 2.2, 0.35, boxstyle="round,pad=0.03", ec="#c62828", fc="#ffebee")
    ax.add_patch(b_pdf)
    ax.text(3.8, 0.825, "Download PDF Report", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#c62828")

    b_docx = patches.FancyBboxPatch((5.1, 0.65), 2.2, 0.35, boxstyle="round,pad=0.03", ec="#1565c0", fc="#e3f2fd")
    ax.add_patch(b_docx)
    ax.text(6.2, 0.825, "Download Word (DOCX)", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#1565c0")

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_7_1_user_login.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_fig_7_2():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)

    draw_browser_frame(ax, "Smart Pharmacy System - /dashboard")

    # Sidebar
    sidebar = patches.Rectangle((0, 0), 1.8, 6.05, ec="#12343b", fc="#12343b")
    ax.add_patch(sidebar)
    ax.text(0.9, 5.7, "⚚ Pharmacy", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#ffffff")
    
    menus = ["Dashboard", "Medicines", "Inventory", "Transactions", "Waste", "Reports"]
    for i, m in enumerate(menus):
        y = 5.2 - i * 0.4
        bg = "#1f5560" if i == 0 else "#12343b"
        if i == 0:
            box = patches.FancyBboxPatch((0.15, y - 0.15), 1.5, 0.3, boxstyle="round,pad=0.02", ec="none", fc=bg)
            ax.add_patch(box)
        ax.text(0.3, y, m, fontsize=7.5, color="white" if i == 0 else "#cfe3e6", va='center')

    # Main Header
    ax.text(2.1, 5.7, "Dashboard", fontsize=13, fontweight='bold', color="#112233", va='center')
    ax.text(8.8, 5.7, "Admin User (admin)", fontsize=7.5, color="#546e7a", va='center')

    # Stat Cards
    stats = [
        ("Medicines", "4", "#1565c0"),
        ("Batches", "5", "#1565c0"),
        ("Units in Stock", "280", "#1565c0"),
        ("Low Stock", "1", "#f57c00"),
        ("Near Expiry", "1", "#0288d1"),
        ("Expired Batches", "1", "#d32f2f")
    ]
    for i, (label, val, col) in enumerate(stats):
        x = 2.1 + i * 1.25
        card = patches.FancyBboxPatch((x, 4.8), 1.15, 0.65, boxstyle="round,pad=0.03", ec="#cfd8dc", fc="#ffffff")
        ax.add_patch(card)
        left_border = patches.Rectangle((x, 4.8), 0.05, 0.65, ec=col, fc=col)
        ax.add_patch(left_border)
        ax.text(x + 0.12, 5.28, label, fontsize=6.5, color="#546e7a")
        ax.text(x + 0.12, 4.98, val, fontsize=11, fontweight='bold', color=col)

    # Sales Count per Medicine Section
    sec_box = patches.FancyBboxPatch((2.1, 0.5), 7.6, 4.0, boxstyle="round,pad=0.05", ec="#b0bec5", fc="#ffffff", lw=1)
    ax.add_patch(sec_box)

    sec_hdr = patches.Rectangle((2.1, 4.05), 7.6, 0.45, ec="#cfd8dc", fc="#f8f9fa")
    ax.add_patch(sec_hdr)
    ax.text(2.3, 4.28, "🛡️ Admin Feature: Sales Count per Medicine", fontsize=9, fontweight='bold', color="#113355", va='center')
    ax.text(8.7, 4.28, "Export CSV →", fontsize=7.5, color="#1565c0", fontweight='bold', va='center')

    # Table Header
    th_bg = patches.Rectangle((2.1, 3.65), 7.6, 0.35, ec="#cfd8dc", fc="#e9eef4")
    ax.add_patch(th_bg)
    ax.text(2.3, 3.82, "Medicine Name", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(4.2, 3.82, "Category", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(5.5, 3.82, "Sales Txns", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(6.8, 3.82, "Units Sold", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(8.2, 3.82, "Total Revenue", fontsize=7.2, fontweight='bold', color="#37474f", va='center')

    # Table rows
    table_rows = [
        ("Paracetamol 500mg", "Analgesic", "1", "30 units", "$75.00"),
        ("Ibuprofen 400mg", "Analgesic", "1", "12 units", "$60.00"),
        ("Amoxicillin 250mg", "Antibiotic", "1", "10 units", "$90.00"),
        ("Cetirizine 10mg", "Antihistamine", "1", "5 units", "$17.50"),
    ]
    for r_idx, (m_name, cat, txns, sold, rev) in enumerate(table_rows):
        y = 3.25 - r_idx * 0.45
        row_bg = "#ffffff" if r_idx % 2 == 0 else "#f8f9fa"
        rb = patches.Rectangle((2.1, y - 0.1), 7.6, 0.45, ec="#eeeeee", fc=row_bg)
        ax.add_patch(rb)
        ax.text(2.3, y + 0.12, m_name, fontsize=7.5, fontweight='bold', color="#1565c0", va='center')
        ax.text(4.2, y + 0.12, cat, fontsize=7.2, color="#555555", va='center')
        # Pill badge for sales count
        badge = patches.FancyBboxPatch((5.6, y - 0.02), 0.35, 0.25, boxstyle="round,pad=0.03", ec="#1565c0", fc="#e3f2fd")
        ax.add_patch(badge)
        ax.text(5.77, y + 0.1, txns, fontsize=7.2, fontweight='bold', color="#1565c0", ha='center', va='center')
        ax.text(6.8, y + 0.12, sold, fontsize=7.2, fontweight='bold', color="#2e7d32", va='center')
        ax.text(8.2, y + 0.12, rev, fontsize=7.5, fontweight='bold', color="#112233", va='center')

    # Stock alert table below
    ax.text(2.3, 1.25, "Recent Stock & Expiry Alerts", fontsize=8.5, fontweight='bold', color="#c62828")
    ax.text(2.3, 0.85, "• DEMO-AMX-01: Near Expiry (expires in 20 days)\n• DEMO-CET-01: Low Stock (20 units left, reorder at 30)\n• DEMO-IBU-OLD: Expired (quarantined on Waste page)",
            fontsize=7, color="#444444")

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_7_2_admin_dashboard.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_fig_7_3():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    draw_browser_frame(ax, "Smart Pharmacy System - /medicines")

    # Title & Add button
    ax.text(0.5, 4.6, "Medicines Catalogue", fontsize=12, fontweight='bold', color="#112233", va='center')
    btn_add = patches.FancyBboxPatch((8.2, 4.4), 1.4, 0.4, boxstyle="round,pad=0.03", ec="#1f497d", fc="#1f497d")
    ax.add_patch(btn_add)
    ax.text(8.9, 4.6, "+ Add medicine", ha='center', va='center', fontsize=7.5, fontweight='bold', color="white")

    # Search bar
    sbox = patches.FancyBboxPatch((0.5, 3.8), 3.5, 0.35, boxstyle="round,pad=0.03", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(sbox)
    ax.text(0.7, 3.97, "Search by name or ID...", fontsize=7.5, color="#888888", va='center')
    sbtn = patches.FancyBboxPatch((4.1, 3.8), 0.8, 0.35, boxstyle="round,pad=0.02", ec="#1f497d", fc="#ffffff")
    ax.add_patch(sbtn)
    ax.text(4.5, 3.97, "Search", ha='center', va='center', fontsize=7.2, fontweight='bold', color="#1f497d")

    # Table
    t_box = patches.FancyBboxPatch((0.5, 0.5), 9.0, 3.0, boxstyle="round,pad=0.05", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(t_box)

    th = patches.Rectangle((0.5, 3.1), 9.0, 0.4, ec="#cfd8dc", fc="#e9eef4")
    ax.add_patch(th)
    ax.text(0.8, 3.3, "ID", fontsize=7.5, fontweight='bold', color="#37474f", va='center')
    ax.text(1.5, 3.3, "Medicine Name", fontsize=7.5, fontweight='bold', color="#37474f", va='center')
    ax.text(4.0, 3.3, "Category", fontsize=7.5, fontweight='bold', color="#37474f", va='center')
    ax.text(6.0, 3.3, "Manufacturer", fontsize=7.5, fontweight='bold', color="#37474f", va='center')
    ax.text(8.5, 3.3, "Actions", fontsize=7.5, fontweight='bold', color="#37474f", va='center')

    rows = [
        ("1", "Paracetamol 500mg", "Analgesic", "Demo Pharma Ltd"),
        ("2", "Amoxicillin 250mg", "Antibiotic", "Demo Pharma Ltd"),
        ("3", "Cetirizine 10mg", "Antihistamine", "Sample Labs"),
        ("4", "Ibuprofen 400mg", "Analgesic", "Sample Labs"),
    ]
    for idx, (mid, name, cat, mfg) in enumerate(rows):
        y = 2.6 - idx * 0.5
        rb = patches.Rectangle((0.5, y - 0.15), 9.0, 0.5, ec="#f0f0f0", fc="#ffffff" if idx%2==0 else "#f8f9fa")
        ax.add_patch(rb)
        ax.text(0.8, y + 0.1, mid, fontsize=7.2, color="#555555", va='center')
        ax.text(1.5, y + 0.1, name, fontsize=7.5, fontweight='bold', color="#1565c0", va='center')
        ax.text(4.0, y + 0.1, cat, fontsize=7.2, color="#333333", va='center')
        ax.text(6.0, y + 0.1, mfg, fontsize=7.2, color="#333333", va='center')

        # Action buttons
        b_view = patches.FancyBboxPatch((8.0, y - 0.05), 0.55, 0.3, boxstyle="round,pad=0.02", ec="#78909c", fc="#ffffff")
        ax.add_patch(b_view)
        ax.text(8.27, y + 0.1, "View", fontsize=6.8, color="#37474f", ha='center', va='center')

        b_edit = patches.FancyBboxPatch((8.65, y - 0.05), 0.55, 0.3, boxstyle="round,pad=0.02", ec="#1565c0", fc="#ffffff")
        ax.add_patch(b_edit)
        ax.text(8.92, y + 0.1, "Edit", fontsize=6.8, color="#1565c0", ha='center', va='center')

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_7_3_medicines_catalogue.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_fig_7_4():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    draw_browser_frame(ax, "Smart Pharmacy System - /inventory")

    ax.text(0.5, 4.6, "Batch Inventory Management", fontsize=12, fontweight='bold', color="#112233", va='center')
    btn_add = patches.FancyBboxPatch((8.0, 4.4), 1.6, 0.4, boxstyle="round,pad=0.03", ec="#1f497d", fc="#1f497d")
    ax.add_patch(btn_add)
    ax.text(8.8, 4.6, "+ Add new batch", ha='center', va='center', fontsize=7.5, fontweight='bold', color="white")

    t_box = patches.FancyBboxPatch((0.5, 0.5), 9.0, 3.6, boxstyle="round,pad=0.05", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(t_box)

    th = patches.Rectangle((0.5, 3.65), 9.0, 0.45, ec="#cfd8dc", fc="#e9eef4")
    ax.add_patch(th)
    ax.text(0.7, 3.87, "Medicine", fontsize=7.5, fontweight='bold', color="#37474f", va='center')
    ax.text(2.8, 3.87, "Batch No", fontsize=7.5, fontweight='bold', color="#37474f", va='center')
    ax.text(4.2, 3.87, "Qty", fontsize=7.5, fontweight='bold', color="#37474f", va='center')
    ax.text(5.2, 3.87, "Expiry Date", fontsize=7.5, fontweight='bold', color="#37474f", va='center')
    ax.text(6.8, 3.87, "Selling Price", fontsize=7.5, fontweight='bold', color="#37474f", va='center')
    ax.text(8.3, 3.87, "Status Badge", fontsize=7.5, fontweight='bold', color="#37474f", va='center')

    batches = [
        ("Paracetamol 500mg", "DEMO-PCM-01", "166", "2027-11-25", "$2.50", "Available", "#2e7d32", "#e8f5e9"),
        ("Amoxicillin 250mg", "DEMO-AMX-01", "50", "2026-11-10", "$9.00", "Near Expiry", "#0288d1", "#e1f5fe"),
        ("Cetirizine 10mg", "DEMO-CET-01", "20", "2027-08-17", "$3.50", "Low Stock", "#f57c00", "#fff3e0"),
        ("Ibuprofen 400mg", "DEMO-IBU-01", "68", "2027-10-21", "$5.00", "Available", "#2e7d32", "#e8f5e9"),
        ("Ibuprofen 400mg", "DEMO-IBU-OLD", "10", "2026-10-11", "$5.00", "Expired", "#d32f2f", "#ffebee")
    ]
    for idx, (med, bno, qty, exp, prc, st, col, bgcol) in enumerate(batches):
        y = 3.15 - idx * 0.55
        rb = patches.Rectangle((0.5, y - 0.18), 9.0, 0.55, ec="#eeeeee", fc="#ffffff" if idx%2==0 else "#f8f9fa")
        ax.add_patch(rb)
        ax.text(0.7, y + 0.1, med, fontsize=7.5, fontweight='bold', color="#112233", va='center')
        ax.text(2.8, y + 0.1, bno, fontsize=7.2, color="#333333", va='center')
        ax.text(4.2, y + 0.1, qty, fontsize=7.5, fontweight='bold', color="#112233", va='center')
        ax.text(5.2, y + 0.1, exp, fontsize=7.2, color="#555555", va='center')
        ax.text(6.8, y + 0.1, prc, fontsize=7.2, color="#333333", va='center')

        # Status badge
        badge = patches.FancyBboxPatch((8.0, y - 0.05), 1.2, 0.32, boxstyle="round,pad=0.03", ec=col, fc=bgcol)
        ax.add_patch(badge)
        ax.text(8.6, y + 0.11, st, fontsize=7, fontweight='bold', color=col, ha='center', va='center')

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_7_4_inventory_batches.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_fig_7_5():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    draw_browser_frame(ax, "Smart Pharmacy System - /transactions/sale")

    card = patches.FancyBboxPatch((1.5, 0.6), 7.0, 4.3, boxstyle="round,pad=0.1", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(card)

    ax.text(2.0, 4.4, "Record Medicine Sale (Clinical Dispensing)", fontsize=11, fontweight='bold', color="#113355")
    ax.text(2.0, 4.1, "Select batch, verify price and dispense medication to customer.", fontsize=7.5, color="#546e7a")

    # Form fields
    ax.text(2.0, 3.65, "Select Batch (Available & Not Expired)", fontsize=8, fontweight='bold', color="#333333")
    f_sel = patches.FancyBboxPatch((2.0, 3.2), 6.0, 0.35, boxstyle="round,pad=0.03", ec="#1f497d", fc="#ffffff")
    ax.add_patch(f_sel)
    ax.text(2.2, 3.37, "Paracetamol 500mg - Batch DEMO-PCM-01 (166 in stock, Exp: 2027-11-25)", fontsize=7.5, color="#112233", va='center')

    ax.text(2.0, 2.85, "Quantity to Sell", fontsize=8, fontweight='bold', color="#333333")
    f_qty = patches.FancyBboxPatch((2.0, 2.4), 2.8, 0.35, boxstyle="round,pad=0.03", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(f_qty)
    ax.text(2.2, 2.57, "5", fontsize=8, fontweight='bold', color="#112233", va='center')

    ax.text(5.2, 2.85, "Unit Selling Price ($)", fontsize=8, fontweight='bold', color="#333333")
    f_prc = patches.FancyBboxPatch((5.2, 2.4), 2.8, 0.35, boxstyle="round,pad=0.03", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(f_prc)
    ax.text(5.4, 2.57, "2.50", fontsize=8, color="#112233", va='center')

    # Total auto calculation
    tot_box = patches.FancyBboxPatch((2.0, 1.7), 6.0, 0.45, boxstyle="round,pad=0.04", ec="#81c784", fc="#e8f5e9")
    ax.add_patch(tot_box)
    ax.text(2.2, 1.92, "Total Sale Value: $12.50  (Stock will decrease: 166 → 161)", fontsize=8, fontweight='bold', color="#2e7d32", va='center')

    # Submit button
    s_btn = patches.FancyBboxPatch((2.0, 1.05), 6.0, 0.42, boxstyle="round,pad=0.04", ec="#2e7d32", fc="#2e7d32")
    ax.add_patch(s_btn)
    ax.text(5.0, 1.26, "Confirm & Dispense Sale", ha='center', va='center', fontsize=9, fontweight='bold', color="white")

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_7_5_pharmacist_sale.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_fig_7_6():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    draw_browser_frame(ax, "Smart Pharmacy System - /waste")

    ax.text(0.5, 4.6, "Medicine Waste & Hazardous Disposal Management", fontsize=11, fontweight='bold', color="#113355", va='center')

    # Alert warning box
    ab = patches.FancyBboxPatch((0.5, 3.8), 9.0, 0.5, boxstyle="round,pad=0.03", ec="#e57373", fc="#ffebee")
    ax.add_patch(ab)
    ax.text(0.7, 4.05, "⚠️ 1 Expired Batch in stock: DEMO-IBU-OLD (Ibuprofen 400mg) - Record write-off below to dispose securely.",
            fontsize=7.5, fontweight='bold', color="#c62828", va='center')

    # Table
    t_box = patches.FancyBboxPatch((0.5, 0.5), 9.0, 3.0, boxstyle="round,pad=0.05", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(t_box)

    th = patches.Rectangle((0.5, 3.05), 9.0, 0.4, ec="#cfd8dc", fc="#e9eef4")
    ax.add_patch(th)
    ax.text(0.8, 3.25, "Waste ID", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(2.0, 3.25, "Medicine & Batch", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(4.5, 3.25, "Quantity Disposed", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(6.2, 3.25, "Reason", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(7.6, 3.25, "Disposal Date", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(8.8, 3.25, "User", fontsize=7.2, fontweight='bold', color="#37474f", va='center')

    records = [
        ("1", "Ibuprofen 400mg (DEMO-IBU-OLD)", "5 units", "Expired", "2026-10-21", "Pharmacist"),
        ("2", "Paracetamol 500mg (DEMO-PCM-01)", "4 units", "Damaged", "2026-10-21", "Pharmacist")
    ]
    for idx, (wid, mb, qty, rsn, dt, usr) in enumerate(records):
        y = 2.55 - idx * 0.55
        rb = patches.Rectangle((0.5, y - 0.15), 9.0, 0.55, ec="#eeeeee", fc="#ffffff" if idx%2==0 else "#f8f9fa")
        ax.add_patch(rb)
        ax.text(0.8, y + 0.1, wid, fontsize=7.2, color="#555555", va='center')
        ax.text(2.0, y + 0.1, mb, fontsize=7.5, fontweight='bold', color="#1565c0", va='center')
        ax.text(4.5, y + 0.1, qty, fontsize=7.5, fontweight='bold', color="#c62828", va='center')

        badge = patches.FancyBboxPatch((6.1, y - 0.05), 1.0, 0.3, boxstyle="round,pad=0.02",
                                      ec="#d32f2f" if rsn=="Expired" else "#f57c00",
                                      fc="#ffebee" if rsn=="Expired" else "#fff3e0")
        ax.add_patch(badge)
        ax.text(6.6, y + 0.1, rsn, fontsize=7, fontweight='bold', color="#d32f2f" if rsn=="Expired" else "#f57c00", ha='center', va='center')

        ax.text(7.6, y + 0.1, dt, fontsize=7.2, color="#555555", va='center')
        ax.text(8.8, y + 0.1, usr, fontsize=7.2, color="#333333", va='center')

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_7_6_waste_management.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

def generate_fig_7_7():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    draw_browser_frame(ax, "Smart Pharmacy System - /reports")

    ax.text(0.5, 4.6, "Management Reports & Analytics", fontsize=11, fontweight='bold', color="#113355", va='center')

    # Filter form card
    f_card = patches.FancyBboxPatch((0.5, 3.4), 9.0, 0.95, boxstyle="round,pad=0.04", ec="#cfd8dc", fc="#f8f9fa")
    ax.add_patch(f_card)

    ax.text(0.7, 4.05, "Report Type", fontsize=7.2, fontweight='bold', color="#333333")
    r_sel = patches.FancyBboxPatch((0.7, 3.55), 2.8, 0.35, boxstyle="round,pad=0.02", ec="#1f497d", fc="#ffffff")
    ax.add_patch(r_sel)
    ax.text(0.85, 3.72, "Sales Count Per Medicine Report", fontsize=7.2, fontweight='bold', color="#113355", va='center')

    ax.text(3.8, 4.05, "From Date (Optional)", fontsize=7.2, fontweight='bold', color="#333333")
    d1 = patches.FancyBboxPatch((3.8, 3.55), 1.8, 0.35, boxstyle="round,pad=0.02", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(d1)
    ax.text(3.95, 3.72, "2026-10-01", fontsize=7.2, color="#555555", va='center')

    ax.text(5.9, 4.05, "To Date (Optional)", fontsize=7.2, fontweight='bold', color="#333333")
    d2 = patches.FancyBboxPatch((5.9, 3.55), 1.8, 0.35, boxstyle="round,pad=0.02", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(d2)
    ax.text(6.05, 3.72, "2026-10-31", fontsize=7.2, color="#555555", va='center')

    g_btn = patches.FancyBboxPatch((8.0, 3.55), 1.3, 0.35, boxstyle="round,pad=0.02", ec="#1f497d", fc="#1f497d")
    ax.add_patch(g_btn)
    ax.text(8.65, 3.72, "Generate", ha='center', va='center', fontsize=7.5, fontweight='bold', color="white")

    # Table Header & Export button
    ax.text(0.5, 3.0, "Sales Count Per Medicine Report", fontsize=9, fontweight='bold', color="#1f497d", va='center')
    csv_btn = patches.FancyBboxPatch((8.0, 2.8), 1.5, 0.38, boxstyle="round,pad=0.03", ec="#2e7d32", fc="#2e7d32")
    ax.add_patch(csv_btn)
    ax.text(8.75, 2.99, "📥 Export CSV", ha='center', va='center', fontsize=7.5, fontweight='bold', color="white")

    t_box = patches.FancyBboxPatch((0.5, 0.5), 9.0, 2.1, boxstyle="round,pad=0.05", ec="#cfd8dc", fc="#ffffff")
    ax.add_patch(t_box)

    th = patches.Rectangle((0.5, 2.15), 9.0, 0.4, ec="#cfd8dc", fc="#e9eef4")
    ax.add_patch(th)
    ax.text(0.8, 2.35, "ID", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(1.5, 2.35, "Medicine Name", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(4.0, 2.35, "Sales Count", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(6.0, 2.35, "Units Sold", fontsize=7.2, fontweight='bold', color="#37474f", va='center')
    ax.text(8.0, 2.35, "Total Revenue", fontsize=7.2, fontweight='bold', color="#37474f", va='center')

    rep_rows = [
        ("1", "Paracetamol 500mg", "1", "30", "$75.00"),
        ("4", "Ibuprofen 400mg", "1", "12", "$60.00"),
        ("2", "Amoxicillin 250mg", "1", "10", "$90.00"),
    ]
    for idx, (mid, name, sc, us, tr) in enumerate(rep_rows):
        y = 1.7 - idx * 0.45
        rb = patches.Rectangle((0.5, y - 0.1), 9.0, 0.45, ec="#eeeeee", fc="#ffffff" if idx%2==0 else "#f8f9fa")
        ax.add_patch(rb)
        ax.text(0.8, y + 0.1, mid, fontsize=7.2, color="#555555", va='center')
        ax.text(1.5, y + 0.1, name, fontsize=7.5, fontweight='bold', color="#112233", va='center')
        ax.text(4.0, y + 0.1, sc, fontsize=7.2, fontweight='bold', color="#1565c0", va='center')
        ax.text(6.0, y + 0.1, us + " units", fontsize=7.2, fontweight='bold', color="#2e7d32", va='center')
        ax.text(8.0, y + 0.1, tr, fontsize=7.5, fontweight='bold', color="#112233", va='center')

    plt.tight_layout()
    save_path = os.path.join(IMG_DIR, "fig_7_7_reports_export.png")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Generated:", save_path)

if __name__ == "__main__":
    generate_fig_7_1()
    generate_fig_7_2()
    generate_fig_7_3()
    generate_fig_7_4()
    generate_fig_7_5()
    generate_fig_7_6()
    generate_fig_7_7()
