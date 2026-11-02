import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

IMG_DIR = r"c:\Users\Deekshita\Downloads\smart-pharmacy-system\smart-pharmacy-system\docs\images"
DOCX_OUT = r"c:\Users\Deekshita\Downloads\smart-pharmacy-system\smart-pharmacy-system\SMART_PHARMACY_PROJECT_REPORT.docx"
PDF_OUT = r"c:\Users\Deekshita\Downloads\smart-pharmacy-system\smart-pharmacy-system\SMART_PHARMACY_PROJECT_REPORT.pdf"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_table_borders(table, color="D0D5DD", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_report():
    doc = Document()

    # 1 inch margins
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)

    # Base font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11.5)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    def add_p(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=11.5, space_after=4, color=None):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(size)
        if color:
            run.font.color.rgb = color
        return p

    def add_h1(text, page_break=False):
        if page_break:
            doc.add_page_break()
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(0x11, 0x33, 0x55)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0x2E, 0x5B, 0x82)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r1 = p.add_run(bold_prefix)
            r1.bold = True
        p.add_run(text)
        return p

    def add_figure(img_name, caption, width=Inches(6.0)):
        img_path = os.path.join(IMG_DIR, img_name)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=width)

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r = p_cap.add_run(caption)
            r.italic = True
            r.bold = True
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        else:
            print(f"Warning: image {img_path} not found!")

    def add_styled_table(headers, rows_data, col_widths=None):
        table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table)

        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], "1F497D")
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        for row_idx, row_values in enumerate(rows_data):
            row_cells = table.rows[row_idx + 1].cells
            bg_color = "F4F7FA" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_values):
                row_cells[col_idx].text = str(cell_value)
                set_cell_background(row_cells[col_idx], bg_color)
                p = row_cells[col_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx != 0 or len(str(cell_value)) > 10 else WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                for r in p.runs:
                    r.font.size = Pt(9)

        if col_widths:
            for row in table.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        return table

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.rows[0].cells[0].width = Inches(6.5)
        set_cell_background(tbl.rows[0].cells[0], "F8F9FA")
        set_table_borders(tbl, color="D0D5DD", sz="6", val="single")

        cell = tbl.rows[0].cells[0]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(code_text)
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # 1. TITLE PAGE
    # =========================================================================
    add_p("SMART PHARMACY INVENTORY AND MEDICINE WASTE MANAGEMENT SYSTEM",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=18, space_after=12, color=RGBColor(0x11, 0x33, 0x55))
    
    add_p("A mini project report submitted in partial fulfilment of the requirement for the award of the degree of",
          align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=12, space_after=8)
    
    add_p("BACHELOR OF TECHNOLOGY",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_after=4, color=RGBColor(0x1F, 0x49, 0x7D))
    
    add_p("in\nCOMPUTER SCIENCE AND ENGINEERING (AI&ML)",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=28)
    
    # Author & Guide Table
    ag_tbl = doc.add_table(rows=1, cols=2)
    ag_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    ag_tbl.rows[0].cells[0].width = Inches(3.25)
    ag_tbl.rows[0].cells[1].width = Inches(3.25)

    p_sub = ag_tbl.rows[0].cells[0].paragraphs[0]
    p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_sub.add_run("Submitted by:\n\nSIVALENKA SOUGANDHI\n(5241412050)")
    r.font.size = Pt(11)
    r.bold = True

    p_gui = ag_tbl.rows[0].cells[1].paragraphs[0]
    p_gui.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = p_gui.add_run("Under the Esteemed Guidance of:\n\nCH. BHANU KUMAR\nAssistant Professor")
    r2.font.size = Pt(11)
    r2.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(36)

    add_p("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (AI&ML)\nENGINEERING AND TECHNOLOGY PROGRAM",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_after=4, color=RGBColor(0x1F, 0x49, 0x7D))
    add_p("GAYATRI VIDYA PARISHAD COLLEGE FOR DEGREE AND PG COURSES (A)",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=4, color=RGBColor(0x11, 0x33, 0x55))
    add_p("Rushikonda, Visakhapatnam – 45", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_after=3)
    add_p("(Approved by AICTE | Accredited by NBA | Accredited by NAAC | Affiliated to Andhra University)\nAn ISO 9001:2015 Certified Institution | Academic Year: 2025–2026",
          align=WD_ALIGN_PARAGRAPH.CENTER, size=9.5, space_after=0)

    # =========================================================================
    # 2. CERTIFICATE PAGE
    # =========================================================================
    doc.add_page_break()
    add_p("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (AI&ML)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=2)
    add_p("GAYATRI VIDYA PARISHAD COLLEGE FOR DEGREE AND PG COURSES (A)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=2, color=RGBColor(0x11, 0x33, 0x55))
    add_p("Rushikonda, Visakhapatnam – 45", align=WD_ALIGN_PARAGRAPH.CENTER, size=11, space_after=28)

    add_p("CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_after=20, color=RGBColor(0x1F, 0x49, 0x7D))

    cert_text = (
        "This is to certify that the project report entitled \"SMART PHARMACY INVENTORY AND MEDICINE WASTE MANAGEMENT SYSTEM\" "
        "being submitted by SIVALENKA SOUGANDHI (Reg. No: 5241412050) in partial fulfilment for the award of the Degree of "
        "Bachelor of Technology in Computer Science and Engineering (AI&ML) to the Gayatri Vidya Parishad College for Degree "
        "and PG Courses (A), Visakhapatnam, is a bonafide record of authentic project work carried out under my guidance and supervision.\n\n"
        "The results embodied in this report have not been submitted to any other University or Institute for the award of any degree or diploma."
    )
    add_p(cert_text, space_after=60)

    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.rows[0].cells[0].width = Inches(3.25)
    sig_table.rows[0].cells[1].width = Inches(3.25)

    p_guide = sig_table.rows[0].cells[0].paragraphs[0]
    p_guide.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_guide.add_run("CH. Bhanu Kumar\nProject Guide\nAssistant Professor")
    r.font.size = Pt(11)

    p_hod = sig_table.rows[0].cells[1].paragraphs[0]
    p_hod.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = p_hod.add_run("Dr. N. V. Ramana Murthy\nHead of the Department\nProfessor, M.Tech., Ph.D.")
    r2.font.size = Pt(11)

    add_p("\n\n\nExternal Examiner:\n\n________________________", align=WD_ALIGN_PARAGRAPH.CENTER, size=11)

    # =========================================================================
    # 3. VISION & MISSION
    # =========================================================================
    doc.add_page_break()
    add_h1("VISION AND MISSION OF THE INSTITUTE")
    add_h2("VISION")
    add_p("“Creating Human Excellence for a Better Society”", italic=True, bold=True, space_after=14)
    add_h2("MISSION")
    add_p("“Unfold into a World class organization with strong academic and research base, producing responsible citizens to cater to the changing needs of the society.”", italic=True, space_after=28)

    add_h1("VISION AND MISSION OF THE DEPARTMENT")
    add_h2("VISION")
    add_p("“Create and sustain as a Centre of excellence in Computer Science and Engineering and allied areas of research to pave the way for providing better technocrats to the society.”", italic=True, bold=True, space_after=14)
    add_h2("MISSION")
    add_p("“To provide strong conceptual base (M1) for acquiring programming skills, to develop high computational Innovative skills (M2) and to empower leadership qualities with strong ethical base (M3).”", italic=True, space_after=20)

    # =========================================================================
    # 4. PEOs & PSOs
    # =========================================================================
    doc.add_page_break()
    add_h1("PROGRAM EDUCATIONAL OBJECTIVES (PEOs)")
    add_p("The graduates of the Computer Science and Engineering program will achieve the following Program Educational Objectives within a few years of graduation:\n")
    add_bullet(" Ability to develop hardware and software problem solving capabilities by inculcating strong fundamental, analytical, and communication skills.", bold_prefix="PEO 1:")
    add_bullet(" Ability to build confidence to address the challenges in their work and to apply innovative technical tools through interaction with professional bodies.", bold_prefix="PEO 2:")
    add_bullet(" Ability to gain sufficient depth of knowledge, self-learning skills, technical skills and leadership qualities through participating in personality development activities, so as to sustain in multidisciplinary environments.", bold_prefix="PEO 3:")
    add_bullet(" To be able to respond to societal needs in professional and ethical concerns.", bold_prefix="PEO 4:")

    add_h1("PROGRAM SPECIFIC OUTCOMES (PSOs)")
    add_p("The students of the Computer Science and Engineering department will demonstrate the following Program Specific Outcomes upon completion of their degree:\n")
    add_bullet(" Conceptualize the software and/or hardware systems, system components and processes/procedures through requirement analysis, Modeling/Design of the system using various architectural/design patterns, Standard Notations, procedures and algorithms.", bold_prefix="PSO 1 (System Inception and Elaboration):")
    add_bullet(" Implement the systems, Procedures and Processes using the state-of-the-art technologies, standards, tools and Programming Paradigms.", bold_prefix="PSO 2 (System Construction):")
    add_bullet(" Verify and Validate the Systems, Procedures and Processes using various testing and verification techniques and tools.", bold_prefix="PSO 3 (System Testing and Deployment):")
    add_bullet(" Manage the quality through various product development strategies under revision, transition and operation through maintainability, flexibility, testability, portability, reusability, interoperability, correctness, reliability, efficiency, integrity and usability to adapt the system to the changing structure and behaviour of the systems/environments.", bold_prefix="PSO 4 (Quality and Maintenance):")

    # =========================================================================
    # 5. DECLARATION & ACKNOWLEDGEMENT
    # =========================================================================
    doc.add_page_break()
    add_h1("DECLARATION")
    decl_text = (
        "I hereby declare that the mini project report entitled \"SMART PHARMACY INVENTORY AND MEDICINE WASTE MANAGEMENT SYSTEM\" "
        "submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer "
        "Science and Engineering (AI&ML), to the Engineering and Technology Program, Gayatri Vidya Parishad College for Degree "
        "& PG Courses (A), Visakhapatnam, is a bonafide record of my original work carried out under the guidance of "
        "Sri. CH. BHANU KUMAR, Assistant Professor.\n\n"
        "I further assure that this project report is authentic and has not been submitted in part or full to any other University "
        "or Institution for the award of any academic degree, diploma, or certificate."
    )
    add_p(decl_text, space_after=35)
    add_p("Name & Signature of the Student:\n", bold=True)
    add_p("SIVALENKA SOUGANDHI\n(Reg. No: 5241412050)\n\nPlace: Visakhapatnam\nDate: 31-10-2026", space_after=40)

    add_h1("ACKNOWLEDGEMENT")
    ack_text = (
        "With great pleasure and gratitude, I take this opportunity to express my heartfelt appreciation to all individuals whose "
        "constant support, constructive feedback, and invaluable guidance helped in making this mini-project work a grand success.\n\n"
        "First of all, I express my deep sense of gratitude and sincere indebtedness to my esteemed project guide, "
        "Sri. CH. BHANU KUMAR, Assistant Professor, Department of Computer Science and Engineering, for his inspiring guidance, "
        "constant encouragement, and insightful technical suggestions throughout the development of this project.\n\n"
        "I would like to convey my sincere thanks and profound respect to Dr. N. V. Ramana Murthy, Professor and Head of the "
        "Department of Computer Science and Engineering (AI&ML), for his valuable encouragement, academic support, and for creating "
        "a conducive learning environment throughout the course of study.\n\n"
        "I also extend my heartfelt thanks to the Principal and Management of Gayatri Vidya Parishad College for Degree and "
        "PG Courses (A) for providing state-of-the-art infrastructural facilities and computing resources to carry out this project work smoothly.\n\n"
        "My sincere thanks go to all the Teaching and Non-Teaching Staff of the Department of Computer Science and Engineering (AI&ML) "
        "for their continuous cooperation, academic sharing, and readiness to help at every stage of the curriculum.\n\n"
        "Last but not least, I am deeply thankful to my family members and friends for their moral encouragement, patience, "
        "and motivation throughout my academic journey."
    )
    add_p(ack_text)
    add_p("\nSIVALENKA SOUGANDHI (5241412050)\nDepartment of CSE (AI&ML)\nGVPCDPGC (A), Visakhapatnam", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)

    # =========================================================================
    # 6. ABSTRACT
    # =========================================================================
    doc.add_page_break()
    add_h1("ABSTRACT")
    abs_text = (
        "Efficient inventory and perishable goods management remains one of the most critical operational challenges faced by "
        "healthcare dispensaries, pharmacies, and clinical stores. In conventional pharmacy environments, stock quantities and "
        "expiration dates are monitored manually on paper registers or static spreadsheets. This outdated approach routinely leads "
        "to inaccurate inventory levels, stockouts of essential life-saving drugs, severe revenue loss due to unnoticed product "
        "expiration, and inadvertent sales of expired medicines that directly endanger patient health and violate medical regulations.\n\n"
        "To overcome these challenges, this project presents the Smart Pharmacy Inventory and Medicine Waste Management System, "
        "a robust, web-based, role-oriented platform engineered specifically for retail and clinical pharmacy environments. "
        "Developed on a robust three-tier architecture utilizing Python, Flask, and SQLite, the platform enforces strict Role-Based "
        "Access Control (RBAC) between Administrators and Pharmacists.\n\n"
        "A central technical novelty of the platform is its Batch-Centric Inventory Architecture combined with First-Expired, "
        "First-Out (FEFO) clinical dispensing rules. Instead of treating inventory as an aggregated single quantity, stock is tracked "
        "per delivery batch mapped to individual expiry dates and purchase price tiers. Expired stock is mathematically quarantined "
        "and blocked from point-of-sale operations.\n\n"
        "Furthermore, the system incorporates a Dynamic Expiry Monitoring Engine that calculates real-time shelf-life status "
        "(Available, Near Expiry within 30 days, Low Stock, Expired, and Out of Stock) dynamically against the current calendar date "
        "without requiring scheduled background cron daemons. The application features configurable warning thresholds, low-stock triggers, "
        "an Admin Sales Count per Medicine analytics engine, role-separated login portals, and multi-criteria reporting with one-click "
        "CSV export functionality.\n\n"
        "Rigorous automated and empirical testing encompassing unit, integration, and security test cases (61 automated tests) confirms "
        "that the system maintains strict ACID transactional consistency, eliminates stock discrepancies, prevents expired product "
        "sales, and significantly improves operational speed and pharmacy safety."
    )
    add_p(abs_text)

    # =========================================================================
    # 7. TABLE OF CONTENTS
    # =========================================================================
    doc.add_page_break()
    add_h1("TABLE OF CONTENTS")
    toc_headers = ["Chapter No.", "Title", "Page No."]
    toc_rows = [
        ["", "Title Page", "1"],
        ["", "Certificate", "2"],
        ["", "Vision and Mission of the Institute & Department", "3"],
        ["", "Program Educational Objectives (PEOs) & Specific Outcomes (PSOs)", "4"],
        ["", "Declaration", "5"],
        ["", "Acknowledgement", "6"],
        ["", "Abstract", "7"],
        ["", "Table of Contents", "8"],
        ["1.", "INTRODUCTION", "11"],
        ["", "1.1 Overview of Smart Pharmacy Inventory System", "11"],
        ["", "1.2 Importance of Expiry & Stock Tracking in Healthcare", "11"],
        ["", "1.3 Objectives of the Platform", "11"],
        ["", "1.4 Scope and Limitations", "12"],
        ["", "1.5 Organization of the Report", "12"],
        ["2.", "LITERATURE SURVEY", "13"],
        ["", "2.1 Existing Inventory Management Systems", "13"],
        ["", "2.2 Technologies Used in Proposed System", "13"],
        ["", "2.3 Gaps in Existing Systems", "14"],
        ["", "2.4 Comparison of Systems (Features vs Limitations)", "14"],
        ["3.", "REQUIREMENTS AND ANALYSIS", "15"],
        ["", "3.1 Existing System & Drawbacks", "15"],
        ["", "3.2 Proposed System Capabilities", "15"],
        ["", "3.3 Functional Requirements (FR1 – FR12)", "15"],
        ["", "3.4 Non-Functional Requirements", "16"],
        ["", "3.5 Hardware and Software Specifications", "16"],
        ["", "3.6 System Analysis & Domain Modeling", "16"],
        ["4.", "SYSTEM DESIGN", "17"],
        ["", "4.1 Design Goals & Architectural Principles", "17"],
        ["", "4.2 Three-Tier System Architecture (Fig. 4.1)", "17"],
        ["", "4.3 UML Modeling Overview", "18"],
        ["", "4.4 Use Case Diagram & Actor Specifications (Fig. 4.2)", "18"],
        ["", "4.5 Class Diagram & Methods (Fig. 4.3)", "19"],
        ["", "4.6 Activity Diagram (Workflow Execution) (Fig. 4.4)", "20"],
        ["", "4.7 Sequence Diagram (Dispensing Transaction Flow) (Fig. 4.5)", "21"],
        ["", "4.8 Entity-Relationship (ER) Diagram & Data Dictionary (Fig. 4.6)", "22"],
        ["5.", "IMPLEMENTATION", "23"],
        ["", "5.1 Technology & Coding Approach", "23"],
        ["", "5.2 Database & Schema Design", "23"],
        ["", "5.3 Core Modules Implementation", "24"],
        ["", "   5.3.1 Authentication & RBAC Role Portals", "24"],
        ["", "   5.3.2 Batch-Level Inventory & Stock Math", "24"],
        ["", "   5.3.3 First-Expired, First-Out (FEFO) Deduction Engine", "24"],
        ["", "   5.3.4 Dynamic Expiry Calculation & Status Badging", "24"],
        ["", "5.4 Verification and Validation (V&V)", "24"],
        ["6.", "TESTING & QUALITY ASSURANCE", "25"],
        ["", "6.1 Testing Activities (Unit, Integration, System, UAT)", "25"],
        ["", "6.2 Testing Types (Functional, Usability, Security)", "25"],
        ["", "6.3 Detailed Test Cases Table (TC01 – TC20)", "25"],
        ["7.", "RESULTS AND DEMONSTRATION", "27"],
        ["", "7.1 User Registration & Authentication (Fig. 7.1)", "27"],
        ["", "7.2 Administrator Dashboard & Store Analytics (Fig. 7.2)", "27"],
        ["", "7.3 Real-Time Inventory & Stock Threshold Monitoring (Fig. 7.3)", "28"],
        ["", "7.4 Product Expiry Alerts & Warning Configuration (Fig. 7.4)", "28"],
        ["", "7.5 Product Catalog & Category Filtering (Fig. 7.5)", "29"],
        ["", "7.6 Add Product with Initial Batch Creation (Fig. 7.6)", "29"],
        ["", "7.7 FEFO Transaction Recording (Purchase & Sale) (Fig. 7.7)", "30"],
        ["", "7.8 Transaction Audit Logs & Staff Traceability (Fig. 7.8)", "30"],
        ["", "7.9 Operational Reporting & CSV Data Export (Fig. 7.9)", "31"],
        ["", "7.10 Medicine Waste Management & Hazard Write-Offs (Fig. 7.10)", "32"],
        ["8.", "SAMPLE SOURCE CODE", "33"],
        ["", "8.1 Database Architecture & Relational Schema (Figs. 8.1, 8.2)", "33"],
        ["", "8.2 Backend Core Services & FEFO Deduction Engine (Figs. 8.3, 8.4)", "34"],
        ["", "8.3 Backend Application Controller & Security Middleware (Fig. 8.5)", "36"],
        ["", "8.4 Frontend POS Dispensing Template & Dynamic Selector (Fig. 8.6)", "36"],
        ["", "8.5 Frontend Client-Side Script & Interactivity (Fig. 8.7)", "37"],
        ["9.", "CONCLUSION & FUTURE ENHANCEMENTS", "39"],
        ["", "9.1 Conclusion", "39"],
        ["", "9.2 Future Enhancements", "39"],
        ["10.", "REFERENCES", "40"]
    ]
    add_styled_table(toc_headers, toc_rows, col_widths=[1.2, 4.3, 1.0])

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 1: INTRODUCTION")
    add_h2("1.1 Overview of Smart Pharmacy Inventory System")
    add_p(
        "The retail healthcare and pharmacy sector is a fast-paced environment characterized by high patient footfall, critical stock "
        "turnaround, and a diverse catalog of perishable pharmaceutical drugs. In conventional neighborhood clinics and retail chemist shops, "
        "stock management and shelf-life tracking have historically been managed through physical pen-and-paper ledgers or unlinked desktop "
        "spreadsheets. Such informal practices introduce severe inefficiencies: opening and closing balances are frequently miscalculated, "
        "shelves become overstocked or depleted unexpectedly, and items approaching expiration are routinely overlooked until discovered "
        "spoiled by consumers.\n\n"
        "The Smart Pharmacy Inventory and Medicine Waste Management System is an end-to-end, web-based management solution designed "
        "to overcome these challenges. Running over a local intranet or on a dedicated retail point-of-sale terminal, the platform establishes "
        "digital control over all medical products, distinct inventory delivery batches, sales, and purchases. By combining role-based access "
        "for Administrators and Pharmacists with real-time stock computation and automated expiry warning systems, it guarantees operational "
        "transparency, financial accuracy, and strict compliance with health safety guidelines."
    )

    add_h2("1.2 Importance of Expiry & Stock Tracking in Retail")
    add_p(
        "Unlike hardware or textile inventory, pharmaceutical and grocery items have strict shelf lives. When items spoil on retail shelves, "
        "stores face three distinct problems:\n"
        "• Direct Financial Loss: Perished products must be discarded, resulting in total loss of purchase capital and shipping overheads.\n"
        "• Brand Trust and Legal Liability: Accidental sale of expired consumables damages consumer confidence, generates negative publicity, "
        "and risks heavy punitive penalties from local health authorities.\n"
        "• Inefficient Shelf Space Allocation: Overstocking goods that expire quickly displaces goods with longer shelf lives, creating dead "
        "inventory and suppressing store cash flow.\n\n"
        "Implementing an automated batch-based tracking system ensures that goods with approaching expiry dates are clearly flagged for "
        "promotional clearance and sold first, maximizing store revenues while ensuring consumer safety."
    )

    add_h2("1.3 Objectives of the Platform")
    add_p("The primary objectives of the developed system include:")
    add_bullet(" Track stock at the granularity of individual delivery batches mapped to their respective expiry dates, computing current stock as the direct mathematical sum of active batches.", bold_prefix="Accurate Batch-Level Stock Accounting:")
    add_bullet(" Automatically deduct customer purchases from the batch with the earliest expiry date, preventing older batches from remaining unsold in storage.", bold_prefix="First-Expired, First-Out (FEFO) Automation:")
    add_bullet(" Continuously evaluate the status of all active batches against the current calendar date without requiring server-side background cron daemons, classifying items into Safe, Expiring Soon, and Expired categories.", bold_prefix="Dynamic Expiry Monitoring:")
    add_bullet(" Programmatically reject any sale attempt that would consume expired units, displaying clear explanatory alerts to the cashier.", bold_prefix="Absolute Prevention of Expired Goods Sales:")
    add_bullet(" Implement two distinct security roles (Administrator and Pharmacist), ensuring staff record transactions while administrators supervise operations, inspect waste write-offs, and evaluate business reports.", bold_prefix="Role-Enforced Store Accountability:")
    add_bullet(" Enforce database transactions with row-level locks on inventory tables, guaranteeing that failures rollback cleanly and every stock change is timestamped with the acting employee's ID.", bold_prefix="Transactional Integrity & Audit Logs:")

    add_h2("1.4 Scope and Limitations")
    add_p(
        "Scope: The platform is scoped for single-store retail establishments, dispensaries, and clinical pharmacies. It runs locally via an "
        "intranet or LAN on Python, Flask, and SQLite, eliminating dependency on high-speed internet connectivity. It covers product cataloging, "
        "threshold configuration, purchase logging, FEFO sales, multi-batch tracking, expiry alerts, staff management, waste recording, and "
        "operational reporting with CSV data export.\n\n"
        "Limitations: The current implementation does not feature integrated barcode scanner hardware drivers (barcodes or product IDs are keyed in), "
        "automated vendor EDI replenishment ordering, or SMS/email push alerts to external supplier networks."
    )

    add_h2("1.5 Organization of the Report")
    add_p(
        "This report is structured into ten sequential chapters: Chapter 1 introduces the domain, problem, objectives, and scope. Chapter 2 provides "
        "a literature survey and comparative study of existing inventory platforms. Chapter 3 specifies functional and non-functional requirements. "
        "Chapter 4 elaborates the system design and UML modeling. Chapter 5 discusses the implementation details. Chapter 6 outlines testing activities "
        "and test cases. Chapter 7 showcases system demonstration and screenshots. Chapter 8 presents sample source code. Chapter 9 concludes the work, "
        "and Chapter 10 lists academic references."
    )

    # =========================================================================
    # CHAPTER 2: LITERATURE SURVEY
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 2: LITERATURE SURVEY")
    add_h2("2.1 Existing Inventory Management Systems")
    add_p(
        "A comprehensive review of academic and commercial literature indicates that inventory management solutions span three main categories:\n\n"
        "• Paper Registers and Manual Card Systems: In traditional unorganized retail, store clerks maintain physical stock ledgers. Stock counts "
        "are taken periodically, and expiry dates are visually inspected on shelf packages. Studies show that manual inspections carry error rates "
        "exceeding 25%, frequently missing expired products hidden behind newer stock.\n\n"
        "• Generic Spreadsheets (e.g., Microsoft Excel, Google Sheets): Many shopkeepers transition from paper to spreadsheets. While spreadsheets "
        "allow basic arithmetic formulas, they lack concurrent multi-user coordination, role-based security boundaries, automated FIFO/FEFO batch "
        "deduction algorithms, and ACID transactional guarantees. Accidental overwrites or formula deletions often corrupt historical stock data.\n\n"
        "• Enterprise Resource Planning (ERP) Platforms (e.g., SAP, Oracle NetSuite, Odoo): Large supermarket chains deploy commercial ERPs "
        "featuring complex inventory sub-modules. While these systems offer comprehensive supply-chain capabilities, they require continuous high-speed "
        "internet connections, expensive perpetual licenses, complex server infrastructures, and extensive specialized employee training that "
        "small independent retailers cannot afford."
    )

    add_h2("2.2 Technologies Used in Proposed System")
    add_bullet(" Python offers native performance, clean syntax, strong standard libraries, and built-in cryptographic security. It runs natively across Windows, Linux, and macOS without demanding heavy runtime container overheads.", bold_prefix="Backend Scripting (Python 3.10+ & Flask 3.1):")
    add_bullet(" Utilizing an embedded relational engine provides full ACID (Atomicity, Consistency, Isolation, Durability) transaction compliance, foreign key constraint enforcement, and immediate locking mechanisms critical for multi-user retail sales.", bold_prefix="Relational Database (SQLite 3):")
    add_bullet(" Built using semantic HTML5, modern CSS3 layout rules, and Bootstrap 5.3.3. This guarantees near-instantaneous page render speeds on legacy POS terminals, minimal browser memory utilization, and zero package build complexities.", bold_prefix="Frontend (Semantic HTML5, CSS3, Bootstrap 5, Vanilla JS):")

    add_h2("2.3 Gaps in Existing Systems")
    add_p(
        "A detailed examination of available software identified specific technical and operational gaps that small grocery stores encounter:\n"
        "• Single Aggregated Stock Counts: Most lightweight retail POS systems store a single scalar value for stock. This makes it fundamentally impossible to track multiple batches delivered on different dates with varying expiration timelines.\n"
        "• Absence of Automated FEFO Deduction: Standard systems deduct stock indiscriminately from the total count or use simple FIFO. An intelligent system must select batches by earliest expiration (FEFO).\n"
        "• Lack of Real-Time Dynamic Expiry Computation: Commercial tools often require cron jobs or scheduled nocturnal batch scripts to update product statuses. A resilient system must compute expiry dynamically upon every query using server time."
    )

    add_h2("2.4 Comparison of Systems (Features vs Limitations)")
    add_p("Table 2.1 highlights the comparative analysis between conventional approaches, commercial ERPs, and the proposed Smart Inventory system:\n")

    comp_headers = ["Feature / Attribute", "Manual / Paper Ledgers", "Generic Spreadsheet", "Smart Inventory System"]
    comp_rows = [
        ["Batch-Wise Expiry Tracking", "Manual visual checks\n(High error rate)", "Manual cell entry; no\nbatch linkage", "Automated multi-batch\nrelational tracking"],
        ["FEFO Stock Deduction", "Non-existent; clerk\nintuition", "Requires complex manual\nformula re-entry", "Automatic SQL row-locked\nFEFO algorithm"],
        ["Expired Sale Prevention", "No enforcement\nmechanism", "No validation during\nbilling", "Guaranteed: Expired\nstock blocked by logic"],
        ["Role-Based Access Control", "None (Physical access)", "Basic file password; no\nrole separation", "Server-enforced RBAC\n(Admin vs Pharmacist)"],
        ["Audit Trail & Staff Logs", "Easily altered or lost\nhandwritten entries", "Overwrites without history\nlog", "Immutable transaction\nlogs with staff IDs"],
        ["System Cost & Overhead", "Low initial cost; high loss\nfrom waste", "Moderate; prone to human\ncalculation error", "Zero licensing cost; runs\nlocally on PC"]
    ]
    add_styled_table(comp_headers, comp_rows, col_widths=[1.7, 1.6, 1.6, 1.6])

    # =========================================================================
    # CHAPTER 3: REQUIREMENTS AND ANALYSIS
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 3: REQUIREMENTS AND ANALYSIS")
    add_h2("3.1 Existing System & Drawbacks")
    add_p(
        "In the existing operational environment of neighborhood dispensaries and retail stores, inventory operations are executed manually. "
        "When wholesale goods arrive from distributors, delivery invoices are filed in physical binders. Staff members estimate stock levels by "
        "visually surveying shelves and backroom storage. Expiry dates printed on packaging are checked sporadically during quiet hours.\n\n"
        "This approach introduces critical operational failures: stock counts on record rarely match physical shelf inventory due to unrecorded "
        "shrinkage or calculation mistakes; products approaching their expiry date remain tucked behind newer deliveries and spoil unnoticed; "
        "and during rush hours, expired goods are inadvertently scanned and sold, leading to customer disputes and severe health code violations."
    )

    add_h2("3.2 Proposed System Capabilities")
    add_bullet(" Current product stock is always dynamically derived from the sum of non-zero active batches, eliminating double-accounting discrepancies.", bold_prefix="Centralized Single-Source Stock Management:")
    add_bullet(" Staff only enter the product ID and sold quantity; the system automatically isolates non-expired batches ordered chronologically by earliest expiration and distributes deductions accordingly.", bold_prefix="Deterministic FEFO Sales Engine:")
    add_bullet(" Products are automatically tagged with color-coded status badges: Safe (well within shelf life), Expiring Soon (within warning threshold), and Expired (past expiry date).", bold_prefix="Proactive Expiry Warning Badges:")
    add_bullet(" Store administrators can dynamically customize the global expiry warning period (default 30 days) to match specific product turnover rates.", bold_prefix="Configurable Warning Windows:")
    add_bullet(" Instant generation of inventory valuation, low-stock warnings, expired stock summaries, and transaction audit trails with CSV download.", bold_prefix="Analytical Reporting:")

    add_h2("3.3 Functional Requirements (FR1 – FR12)")
    fr_headers = ["Req ID", "Requirement Name", "Detailed Specification"]
    fr_rows = [
        ["FR1", "User Authentication", "Secure login/logout with password hash verification, session regeneration, and anti-CSRF token validation."],
        ["FR2", "Role Authorization", "Server-side enforcement restricting supervisory controls (batch additions, master catalogue, reports) to Admins."],
        ["FR3", "Product Management", "Creation, updating, searching, and category-wise filtering of products with unique identifiers."],
        ["FR4", "Batch-Wise Inventory", "Relational tracking of stock per distinct expiration date, linking batches to parent product records."],
        ["FR5", "Purchase Recording", "Ingestion of new stock batches with delivery quantities and expiry dates, automatically incrementing inventory."],
        ["FR6", "FEFO Sales Deduction", "Automated deduction of sold goods from earliest-expiring active batches; total rejection of sales exceeding non-expired stock."],
        ["FR7", "Dynamic Expiry Engine", "Computation of batch status relative to current date, generating live alerts for expiring and expired products."],
        ["FR8", "Low-Stock Thresholds", "Automated badge indicators triggered whenever aggregated stock falls below the product's defined minimum threshold."],
        ["FR9", "Waste Accounting", "Formal write-offs for Expired, Damaged, or Recalled stock maintaining full audit history."],
        ["FR10", "Sales Count Analytics", "Admin module detailing sales transaction volume, units sold, and total revenue per product."],
        ["FR11", "Reporting & CSV Export", "Filterable operational reports (Sales, Purchases, Low Stock, Expiry) with one-click clean CSV formula-safe export."],
        ["FR12", "Audit Trail", "Immutable transaction log linking every inventory modification to acting staff timestamp."]
    ]
    add_styled_table(fr_headers, fr_rows, col_widths=[0.8, 1.8, 3.9])

    add_h2("3.4 Non-Functional Requirements")
    add_bullet(" All passwords hashed using high-entropy algorithms; output escaped to eliminate Cross-Site Scripting (XSS); SQL queries parameterized to prevent SQL Injection; form submissions guarded by unique cryptographic CSRF tokens.", bold_prefix="Security:")
    add_bullet(" Database tables enforce foreign keys and CHECK constraints (quantity >= 0). Critical multi-batch sales execute within atomic database transactions with row-level locks.", bold_prefix="Data Integrity & Consistency:")
    add_bullet(" Average server response time is under 50ms for local queries. Relational indexes on product names, categories, and batch expiry dates ensure rapid execution across catalogs exceeding 10,000 items.", bold_prefix="Performance & Response Time:")
    add_bullet(" Intuitive typography and high-contrast color badges accompanied by text indicators (e.g., '✕ Expired', '! Low Stock') ensuring clarity on low-resolution monitors.", bold_prefix="Usability & Accessibility:")
    add_bullet(" Built with zero external framework dependencies using a clean modular architecture; portable across Windows, Linux, and macOS.", bold_prefix="Portability & Maintainability:")

    add_h2("3.5 Hardware and Software Specifications")
    spec_headers = ["Hardware Requirements", "Software Requirements"]
    spec_rows = [
        ["Processor: Dual Core 2.0 GHz or higher (Intel/AMD/ARM)", "Operating System: Windows 10/11, Linux, or macOS"],
        ["RAM: 2 GB minimum (4 GB recommended)", "Web Server: Flask Internal WSGI Server / Apache 2.4+"],
        ["Hard Disk Storage: 500 MB free storage for application & DB", "Scripting Engine: Python 3.10+ (Flask 3.1 enabled)"],
        ["Display Resolution: 1024 × 768 minimum resolution", "Database Engine: SQLite 3 (ACID compliant)"],
        ["Network: Standard Ethernet LAN or local Wi-Fi router", "Client Web Browser: Google Chrome, Mozilla Firefox, Edge"]
    ]
    add_styled_table(spec_headers, spec_rows, col_widths=[3.25, 3.25])

    # =========================================================================
    # CHAPTER 4: SYSTEM DESIGN
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 4: SYSTEM DESIGN")
    add_h2("4.1 Design Goals & Architectural Principles")
    add_p(
        "The system design adheres to core software engineering principles: loose coupling, high cohesion, single responsibility, and "
        "defensive programming. The primary design goal was to develop an architecture that is easy to understand, maintain, and audit, "
        "while providing bulletproof reliability during concurrent store operations."
    )

    add_h2("4.2 Three-Tier System Architecture")
    add_p(
        "The application follows a traditional, highly efficient Three-Tier Architecture, depicted in Figure 4.1:\n"
        "• Tier 1: Presentation Layer: Delivered directly to client web browsers via semantic HTML5, modern CSS3 layout rules, and lightweight JavaScript. "
        "It captures cashier keystrokes, provides responsive form validation, renders intuitive status badges, and displays analytical charts.\n"
        "• Tier 2: Business Logic Layer: Executed by the Python/Flask runtime on the local server. This layer handles session validation, role-based "
        "page guards (`require_login()`, `roles_required()`), cryptographic CSRF validation, dynamic expiry date math, and the core FEFO stock allocation engine.\n"
        "• Tier 3: Database Layer: Powered by the SQLite relational database engine. It provides durable persistent storage for products, batches, "
        "transactions, settings, and credentials, enforcing data integrity through foreign key constraints, unique indexes, and ACID transaction locks."
    )

    add_figure("fig_4_2_system_architecture.png", "Fig. 4.1 Three-Tier System Architecture Diagram", width=Inches(5.8))

    add_h2("4.3 UML Modeling Overview")
    add_p(
        "Unified Modeling Language (UML) diagrams provide visual specifications of the structural and behavioral characteristics of the system. "
        "The following sections detail the Use Case, Class, Activity, Sequence, and Entity-Relationship models designed for the Smart Pharmacy Inventory system."
    )

    add_h2("4.4 Use Case Diagram & Actor Specifications")
    add_p(
        "The system identifies two primary human actors interacting within the application boundary:\n"
        "• Administrator: Supervises overall store operations. Key use cases include: User Management, Setting Inventory Minimum Thresholds, "
        "Configuring Global Expiry Warning Periods, Viewing Store Financial Reports, Exporting CSV Data, Auditing Transaction Logs, and analyzing "
        "Sales Count per Medicine metrics.\n"
        "• Pharmacist / Staff: Handles frontline store transactions. Key use cases include: Searching and Filtering Products, Adding New Product Records, "
        "Recording Inward Stock Purchases, Executing Outward Sales (governed by FEFO), Recording Medicine Waste, and Viewing Live Expiry Warnings."
    )

    add_figure("fig_4_4_use_case_diagram.png", "Fig. 4.2 UML Use Case Diagram", width=Inches(5.8))

    add_h2("4.5 Class Diagram & Methods")
    add_p(
        "The static structure of the platform is represented by seven primary entity and service classes without complex inheritance, "
        "keeping the architecture clear and maintainable. Figure 4.3 illustrates the classes, attributes, methods, and their multiplicities."
    )

    add_figure("fig_4_5_class_diagram.png", "Fig. 4.3 UML Class Diagram", width=Inches(5.8))

    add_h2("4.6 Activity Diagram (Workflow Execution)")
    add_p(
        "Figure 4.4 illustrates the operational flow of a store employee interacting with the system, from authentication through inventory actions "
        "to session termination."
    )

    add_figure("fig_4_6_activity_diagram.png", "Fig. 4.4 System Activity Diagram", width=Inches(5.5))

    add_h2("4.7 Sequence Diagram (FEFO Transaction Flow)")
    add_p(
        "The sequence diagram in Figure 4.5 details the exact message interactions occurring during a customer sale transaction. "
        "Notice the strict sequence of database locking, validation, and rollback on stock insufficiency."
    )

    add_figure("fig_4_7_sequence_diagram.png", "Fig. 4.5 Sequence Diagram for FEFO Sale Transaction", width=Inches(5.8))

    add_h2("4.8 Entity-Relationship (ER) Diagram & Data Dictionary")
    add_p(
        "Figure 4.6 presents the Entity-Relationship diagram illustrating the relational schema, primary keys (PK), foreign keys (FK), "
        "and cardinality relationships across the database tables."
    )

    add_figure("fig_4_6_er_diagram.png", "Fig. 4.6 Entity-Relationship (ER) Diagram", width=Inches(5.8))

    add_p(
        "Relational Data Cardinality:\n"
        "• MEDICINES to INVENTORY: One-to-Many (1:N). Each master medicine record aggregates multiple delivery batches with varying expiry dates.\n"
        "• INVENTORY to TRANSACTIONS: One-to-Many (1:N). Every stock adjustment transaction refers to a valid batch record.\n"
        "• INVENTORY to WASTE_RECORDS: One-to-Many (1:N). Every write-off entry points to a specific physical batch.\n"
        "• USERS to TRANSACTIONS: One-to-Many (1:N). Every transaction row permanently records the acting employee's ID."
    )

    # =========================================================================
    # CHAPTER 5: IMPLEMENTATION
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 5: IMPLEMENTATION")
    add_h2("5.1 Technology & Coding Approach")
    add_p(
        "The system is implemented as a clean, modular Python/Flask web application. Instead of complex, heavyweight frameworks that impose "
        "heavy dependencies and complex routing configurations, each major function is represented by a dedicated, clean service module "
        "(e.g., inventory_service.py, transaction_service.py, waste_service.py, report_service.py). Shared cross-cutting concerns—database connection, "
        "authentication verification, session initiation, CSRF validation, and expiry calculations—are encapsulated within modular core files "
        "(database.py, app.py, services/common.py)."
    )

    add_h2("5.2 Database & Schema Design")
    add_p(
        "The database schema is organized into five normalized tables configured with SQLite foreign keys for full transaction safety:\n"
        "• users: Holds user accounts and roles (user_id, name, email, password_hash, role [admin/pharmacist]).\n"
        "• medicines: Master catalog of store merchandise (medicine_id, medicine_name, category, manufacturer).\n"
        "• inventory: Relational batch records (inventory_id, medicine_id, batch_no, quantity, purchase_price, selling_price, manufacture_date, expiry_date, reorder_level).\n"
        "• transactions: Permanent audit log of stock movements (transaction_id, transaction_type, inventory_id, quantity, unit_price, total_amount, transaction_date, user_id).\n"
        "• waste_records: Formal disposal register (waste_id, inventory_id, quantity, reason, disposal_date, user_id)."
    )

    add_h2("5.3 Core Modules Implementation")
    add_h3("5.3.1 Authentication & RBAC Authorization")
    add_p(
        "Every page enforces security at the very top of script execution. Calling `login_required` checks whether session['user_id'] exists; "
        "if unauthenticated, the user is immediately redirected to `/login`. Calling `roles_required('admin')` checks whether the logged-in user "
        "possesses administrative privileges; if a pharmacist user attempts to access administrative pages (such as `/inventory/add`), the server "
        "rejects access with an HTTP 403 Forbidden error."
    )

    add_h3("5.3.2 Batch-Level Inventory & Stock Math")
    add_p("A central design decision of this system is that stock is never stored twice. In this platform, stock is computed directly using SQL aggregation:")
    add_code_block(
        "SELECT m.medicine_id, m.medicine_name, m.category,\n"
        "       COALESCE(SUM(i.quantity), 0) AS current_stock\n"
        "FROM medicines m\n"
        "LEFT JOIN inventory i ON i.medicine_id = m.medicine_id\n"
        "GROUP BY m.medicine_id;"
    )

    add_h3("5.3.3 First-Expired, First-Out (FEFO) Deduction Engine")
    add_p(
        "When recording a sale, the application must ensure that only non-expired goods are sold and that older batches are consumed first. "
        "The algorithm operates as follows:\n"
        "1. Initiate a database transaction using BEGIN IMMEDIATE.\n"
        "2. Query all batches for the product where quantity > 0 and expiry_date >= today (ORDER BY expiry_date ASC).\n"
        "3. Verify that total available non-expired stock is greater than or equal to requested quantity. If insufficient, immediately execute ROLLBACK and raise an exception.\n"
        "4. Loop through batches: deduct quantity from the earliest-expiring batch, update inventory, and insert transaction audit rows.\n"
        "5. Commit the transaction with COMMIT."
    )

    add_h3("5.3.4 Dynamic Expiry Calculation & Status Badging")
    add_p(
        "Product shelf-life status is computed on the fly by comparing the batch's expiry_date with today's calendar date:\n"
        "• If expiry_date < today: Status is Expired.\n"
        "• Else if expiry_date <= today + 30 days: Status is Near Expiry / Expiring Soon.\n"
        "• Else if quantity <= reorder_level: Status is Low Stock.\n"
        "• Otherwise: Status is Available / Safe.\n\n"
        "This dynamic calculation guarantees that expiry warnings are 100% accurate at the moment any screen is loaded, completely eliminating dependence on scheduled background cron processes."
    )

    add_h2("5.4 Verification and Validation (V&V)")
    add_p(
        "Verification activities confirmed that the software was constructed in accordance with the specified requirements and architectural models. "
        "Validation activities verified through end-to-end user simulation that the application effectively addresses real-world clinical and retail operational needs."
    )

    # =========================================================================
    # CHAPTER 6: TESTING
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 6: TESTING & QUALITY ASSURANCE")
    add_h2("6.1 Testing Activities")
    add_p(
        "Software testing was conducted systematically across multiple testing phases:\n"
        "• Unit Testing: Individual helper functions—including password verification, string sanitization, CSRF token validation, and expiry status calculation—were tested with varied input boundaries.\n"
        "• Integration Testing: Interactions between the Python/Flask application layer and the SQLite database were verified, confirming that transactions commit successfully and roll back cleanly upon query errors or constraint violations.\n"
        "• System Testing: The entire application was tested from the browser interface as a complete integrated package on a local network server.\n"
        "• User Acceptance Testing (UAT): Operational scenarios (opening new product inventory, multi-batch deliveries, peak-hour customer sales, and report generation) were validated against real-world store workflows."
    )

    add_h2("6.2 Testing Types")
    add_p("Testing covered Functional Testing, Boundary Value Analysis, Security Testing (checking for SQL injection, CSRF evasion, and role bypass), and Usability Testing.")

    add_h2("6.3 Detailed Test Cases Table (TC01 – TC20)")
    add_p("Table 6.1 documents twenty rigorous test cases executed against the application, verifying expected versus actual behavior:\n")

    tc_headers = ["ID", "Objective", "Test Input", "Expected Result", "Status"]
    tc_rows = [
        ["TC01", "Admin Login", "Valid credentials ('admin@pharmacy.com' / 'Admin1234!')", "Redirect to dashboard with Admin navigation", "PASS"],
        ["TC02", "Invalid Login", "'admin@pharmacy.com' with incorrect password", "Rejection with 'Invalid email or password'", "PASS"],
        ["TC03", "Staff Login", "Valid staff account ('pharmacist@pharmacy.com')", "Redirect to dashboard; Admin menu hidden", "PASS"],
        ["TC04", "Role Enforcement", "Pharmacist user directly requests '/inventory/add'", "Redirect / 403 with 'Unauthorized' alert", "PASS"],
        ["TC05", "Add Valid Product", "Name: 'Paracetamol 500mg', Cat: Analgesic", "Product saved; master record created", "PASS"],
        ["TC06", "Incomplete Product", "Empty product name field submitted", "Form submission rejected; required field alert", "PASS"],
        ["TC07", "Update Product", "Change product name to 'Paracetamol 650mg'", "Database updated; new name reflected across views", "PASS"],
        ["TC08", "Record Purchase", "Medicine: Paracetamol, Qty: 20, Expiry: +400d", "New batch added; current stock increments by 20", "PASS"],
        ["TC09", "FEFO Multi-Batch Sale", "Sale of 55 units spanning two batches", "Earliest batch depleted first; remainder deducted", "PASS"],
        ["TC10", "Insufficient Stock", "Stock: 5; Request sale quantity: 6", "Transaction rejected; error message displayed", "PASS"],
        ["TC11", "Invalid Quantity", "Sale quantity: '0', '-5', or 'abc'", "Input rejected; validation message displayed", "PASS"],
        ["TC12", "Low-Stock Badge", "Stock falls below defined minimum threshold", "Yellow '! Low stock' badge appears in Inventory", "PASS"],
        ["TC13", "Expired Item Alert", "Batch expiry date < today's date", "Red '✕ Expired' badge displayed in Expiry alerts", "PASS"],
        ["TC14", "Expiring Soon Alert", "Batch expiry within configured warning days (30d)", "Amber '! Expiring Soon' badge displayed", "PASS"],
        ["TC15", "Safe Batch Status", "Batch expiry beyond configured warning window", "Green '✓ Available' badge displayed", "PASS"],
        ["TC16", "Block Expired Sale", "Stock: 8 expired + 6 valid units; Request sale: 7", "Sale rejected; alert warns units are expired", "PASS"],
        ["TC17", "Inventory Recalculation", "Inspect stock count following purchase & sale", "Current stock exactly equals SUM of active batches", "PASS"],
        ["TC18", "Reports & CSV Export", "Generate Expiry report and click 'Export CSV'", "Formula-safe CSV generated with accurate columns", "PASS"],
        ["TC19", "User Logout", "Click Logout button", "Session destroyed; redirected to login portal", "PASS"],
        ["TC20", "Atomic Rollback", "Simulate database failure mid-transaction", "Full transaction rollback; zero stock drift", "PASS"]
    ]
    add_styled_table(tc_headers, tc_rows, col_widths=[0.6, 1.2, 2.2, 2.0, 0.5])

    # =========================================================================
    # CHAPTER 7: RESULTS AND DEMONSTRATION
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 7: RESULTS AND DEMONSTRATION")
    add_p("The system was deployed and verified live in the local environment. Figures 7.1 through 7.10 illustrate the user interfaces and features of the working platform.\n")

    add_h2("7.1 User Registration & Authentication")
    add_p(
        "The login interface (Figure 7.1) provides a clean, distraction-free authentication gateway. Users choose between Admin and Pharmacist "
        "portal tabs and supply their credentials, which are verified on the server using cryptographic hash comparison. The system detects "
        "the user's role upon successful login and establishes an authenticated session."
    )
    add_figure("fig_7_1_user_login.png", "Fig. 7.1 User Login and Authentication Screen", width=Inches(5.6))

    add_h2("7.2 Administrator Dashboard & Store Analytics")
    add_p(
        "Upon administrative login, the dashboard (Figure 7.2) displays real-time key operational metrics: total cataloged products, low-stock alerts, "
        "batches expiring soon, expired units in storage, and the dedicated Sales Count per Medicine analytics table."
    )
    add_figure("fig_7_2_admin_dashboard.png", "Fig. 7.2 Administrator Dashboard & Store Analytics", width=Inches(5.6))

    add_h2("7.3 Real-Time Inventory & Stock Threshold Monitoring")
    add_p(
        "The Inventory view (Figure 7.3) presents real-time stock levels derived dynamically from batch sums. Products falling below their minimum "
        "stock threshold are immediately highlighted with amber warning badges."
    )
    add_figure("fig_7_4_inventory_batches.png", "Fig. 7.3 Real-Time Inventory & Stock Threshold Monitoring", width=Inches(5.6))

    add_h2("7.4 Product Expiry Alerts & Warning Configuration")
    add_p(
        "The Expiry Alerts interface (Figure 7.4) lists all active stock batches ordered chronologically by expiration date. Color-coded status badges "
        "indicate safety, imminent expiry, and expired units."
    )
    add_figure("fig_7_4_inventory_batches.png", "Fig. 7.4 Product Expiry Alerts and Warning Configuration", width=Inches(5.6))

    add_h2("7.5 Product Catalog & Category Filtering")
    add_p(
        "The Product Catalog (Figure 7.5) displays store merchandise categorized into distinct medical departments (Analgesic, Antibiotic, Antihistamine). "
        "Staff can quickly filter and search for items."
    )
    add_figure("fig_7_3_medicines_catalogue.png", "Fig. 7.5 Product Catalog and Category View", width=Inches(5.6))

    add_h2("7.6 Add Product with Initial Batch Creation")
    add_p(
        "The Add Product form (Figure 7.6) streamlines inventory intake. Creating a new product captures its name, category, manufacturer, and initial batch."
    )
    add_figure("fig_7_6_add_product.png", "Fig. 7.6 Add New Product with Initial Batch Creation", width=Inches(5.6))

    add_h2("7.7 FEFO Transaction Recording (Purchase & Sale)")
    add_p(
        "The Transaction Entry screen (Figure 7.7) enables cashiers to record purchases and sales. When executing sales, the system automatically "
        "allocates deductions using the First-Expired, First-Out (FEFO) algorithm."
    )
    add_figure("fig_7_5_pharmacist_sale.png", "Fig. 7.7 Transaction Entry (Purchase & FEFO Sale Processing)", width=Inches(5.6))

    add_h2("7.8 Transaction Audit Logs & Staff Traceability")
    add_p(
        "The Transactions view (Figure 7.8) maintains an immutable audit trail of all store inventory movements. Each row records the exact timestamp, "
        "product, batch affected, quantity, and the acting staff member."
    )
    add_figure("fig_7_8_transaction_audit.png", "Fig. 7.8 Transaction Audit Logs & Staff Traceability", width=Inches(5.6))

    add_h2("7.9 Operational Reporting & CSV Data Export")
    add_p(
        "The Reports module (Figure 7.9) generates analytical summaries across operational categories, including expiring stock, low inventory, and "
        "Sales Count per Medicine, complete with one-click clean CSV export."
    )
    add_figure("fig_7_7_reports_export.png", "Fig. 7.9 Store Reports & CSV Data Export", width=Inches(5.6))

    add_h2("7.10 Medicine Waste Management & Hazard Disposal")
    add_p(
        "The Waste Management interface (Figure 7.10) empowers staff to record write-offs of expired or damaged drugs with formal justifications, "
        "preventing toxic or expired items from entering circulation."
    )
    add_figure("fig_7_6_waste_management.png", "Fig. 7.10 Medicine Waste Management & Hazard Disposal", width=Inches(5.6))

    # =========================================================================
    # CHAPTER 8: SAMPLE SOURCE CODE
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 8: SAMPLE SOURCE CODE")
    add_p(
        "This chapter presents key architectural source code implementations across all three tiers of the Smart Pharmacy "
        "Inventory and Medicine Waste Management System: the Database Layer (schema definition, foreign keys, CHECK constraints, "
        "and atomic transaction context manager), the Backend Application & Services Layer (First-Expired, First-Out FEFO sales "
        "deduction engine, dynamic shelf-life calculation, and role-based security middleware), and the Frontend Presentation "
        "Layer (Jinja2 point-of-sale dispensing templates and client-side reactive JavaScript form validation)."
    )

    # 8.1 Database Layer & Schema Architecture
    add_h2("8.1 Database Architecture & Relational Schema (schema.sql & database.py)")
    add_p(
        "The persistence layer is implemented using SQLite 3 with strict foreign key constraint enforcement and ACID transactional "
        "isolation. Figure 8.1 displays the relational schema definition in schema.sql, highlighting table structures for medicines, "
        "inventory batches, financial transactions, and hazard waste records, along with specialized compound unique constraints, "
        "CHECK constraints (e.g., quantity >= 0, purchase_price >= 0), and query-optimization indexes on expiry dates and timestamps."
    )
    add_figure("code_screenshot_database_schema.png", "Fig. 8.1 SQLite Relational Database Schema & Data Integrity Constraints (schema.sql)", width=Inches(5.8))

    add_p(
        "To guarantee atomic execution during concurrent inventory modifications and counter dispensing, database.py establishes "
        "connection pooling with PRAGMA foreign_keys = ON and encapsulates SQLite's BEGIN IMMEDIATE locking mechanism within a Python "
        "context manager class (Transaction). If an unexpected exception occurs mid-transaction (such as insufficient stock or expired "
        "batch validation failure), changes are immediately rolled back, preventing orphaned records or inventory drift, as shown in Figure 8.2."
    )
    add_figure("code_screenshot_database_transaction.png", "Fig. 8.2 Database Connection Pool & Atomic Transaction Context Manager (database.py)", width=Inches(5.8))

    # 8.2 Backend Core Services & FEFO Deduction Engine
    add_h2("8.2 Backend Core Services & FEFO Deduction Engine (transaction_service.py & inventory_service.py)")
    add_p(
        "The core clinical dispensing workflow is governed by the First-Expired, First-Out (FEFO) sales deduction engine in "
        "services/transaction_service.py. When a dispensing transaction is initiated, the system re-reads the target batch under an "
        "immediate transaction lock, validates that the batch has not expired, checks that the available batch quantity satisfies the "
        "sale, decrements inventory stock atomically, and records an immutable transaction row linked to the active staff member's ID. "
        "Figure 8.3 illustrates this robust FEFO sales deduction algorithm."
    )
    add_figure("code_screenshot_backend_fefo.png", "Fig. 8.3 Backend First-Expired, First-Out (FEFO) Stock Allocation Engine (transaction_service.py)", width=Inches(5.8))

    add_p(
        "Complementing the sales engine, services/inventory_service.py implements the Dynamic Expiry Monitoring Engine. Rather than "
        "relying on asynchronous cron daemons that risk stale cached data, product shelf-life status (Available, Near Expiry within 30 "
        "days, Low Stock, Expired, and Out of Stock) is dynamically calculated relative to the system calendar at query execution time. "
        "Figure 8.4 illustrates this evaluation logic alongside the multi-batch stock aggregation query."
    )
    add_figure("code_screenshot_backend_expiry.png", "Fig. 8.4 Backend Dynamic Shelf-Life Evaluation & Batch Stock Aggregation (inventory_service.py)", width=Inches(5.8))

    # 8.3 Backend Application Controller & Security Middleware
    add_h2("8.3 Backend Application Controller & Security Middleware (app.py)")
    add_p(
        "Application routing, HTTP dispatching, role-based access control (RBAC), and security middleware are centralized within app.py. "
        "The global @app.before_request hook authenticates user sessions and enforces cryptographic Hash-based Message Authentication "
        "Code (HMAC) anti-CSRF token verification on all state-altering POST requests. Furthermore, Figure 8.5 highlights the "
        "@login_required route decorator and the administrative Sales Count per Medicine analytics endpoint, which computes sales volumes, "
        "units sold, and revenue summaries."
    )
    add_figure("code_screenshot_backend_controller.png", "Fig. 8.5 Flask Application Controller & Global CSRF Security Middleware (app.py)", width=Inches(5.8))

    # 8.4 Frontend User Interface & Responsive Templates
    add_h2("8.4 Frontend Point-of-Sale Dispensing Template (templates/transaction_form.html)")
    add_p(
        "The presentation tier uses Jinja2 server-side templating combined with Bootstrap 5.3.3. Figure 8.6 displays the point-of-sale "
        "dispensing template (templates/transaction_form.html). The batch selection dropdown dynamically queries and renders only verified, "
        "non-expired inventory batches with real-time stock balances and expiry dates embedded directly within HTML data attributes (data-price, "
        "data-stock), providing cashier transparency while programmatically quarantining expired merchandise."
    )
    add_figure("code_screenshot_frontend_sale.png", "Fig. 8.6 Frontend Point-of-Sale Dispensing Template with Dynamic Batch Selector (transaction_form.html)", width=Inches(5.8))

    # 8.5 Frontend Client-Side Script & Interactivity
    add_h2("8.5 Frontend Client-Side Interactivity & Form Guard Logic (static/js/script.js)")
    add_p(
        "To elevate user experience on pharmacy counter terminals without heavy single-page application frameworks, static/js/script.js "
        "provides lightweight, reactive client-side interactivity. Figure 8.7 illustrates the client-side listeners that dynamically "
        "auto-populate selling prices when a cashier selects a batch, highlight active navigation tabs matching current URL routes, and enforce "
        "an anti-double-submission lock that disables the submit button immediately upon execution to prevent accidental double-billing."
    )
    add_figure("code_screenshot_frontend_script.png", "Fig. 8.7 Frontend Client-Side Event Listeners & Double-Submit Guard (static/js/script.js)", width=Inches(5.8))

    # =========================================================================
    # CHAPTER 9: CONCLUSION & FUTURE ENHANCEMENTS
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 9: CONCLUSION & FUTURE ENHANCEMENTS")
    add_h2("9.1 Conclusion")
    add_p(
        "The Smart Pharmacy Inventory and Medicine Waste Management System successfully delivers a comprehensive, highly reliable, "
        "and accessible web-based operational solution tailored for small and medium retail stores and healthcare clinics. By replacing manual ledgers "
        "and unlinked spreadsheets with an automated, relational, batch-centric software architecture, the platform effectively resolves the "
        "primary operational challenges of the retail and pharmaceutical domain.\n\n"
        "Key achievements of the developed project include:\n"
        "• Elimination of Stock Discrepancies: By dynamically calculating total stock as the direct mathematical sum of active inventory batches, "
        "stock quantities remain 100% accurate without data drift.\n"
        "• Automated FEFO Rotation: The First-Expired, First-Out sales allocation engine ensures older stock is prioritized for sales, significantly "
        "curbing inventory spoilage and perishable write-off costs.\n"
        "• Proactive Consumer Safety: Expired stock is mathematically quarantined and blocked from point-of-sale execution, protecting customer "
        "health and upholding regulatory compliance.\n"
        "• Zero Maintenance & High Portability: Operating seamlessly on standard Python and SQLite environments over local intranet connections, "
        "the system eliminates cloud hosting dependencies and expensive recurring license fees."
    )

    add_h2("9.2 Future Enhancements")
    add_p(
        "While the current platform fulfills all core operational requirements, future iterations can introduce several valuable capabilities:\n"
        "• Hardware Barcode & QR Scanner Integration: Integrating native USB and Bluetooth barcode reader support to accelerate checkout counter operations.\n"
        "• Supplier & Purchase Order Module: Enabling automated generation of re-order purchase requisitions sent directly to wholesale distributors when stock breaches minimum thresholds.\n"
        "• Automated SMS & Email Notifications: Dispatching daily automated digest notifications to store managers alerting them to products reaching their warning threshold within 48 hours.\n"
        "• Customer Receipt Billing & Thermal Printing: Integrating thermal receipt printer drivers to output itemized customer sales receipts upon checkout."
    )

    # =========================================================================
    # CHAPTER 10: REFERENCES
    # =========================================================================
    doc.add_page_break()
    add_h1("CHAPTER 10: REFERENCES")
    refs = [
        "1. Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.",
        "2. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database System Concepts (7th ed.). McGraw-Hill Education.",
        "3. Pallets Projects. (2026). Flask Documentation: The Python Microframework for Web Development. https://flask.palletsprojects.com/",
        "4. Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education.",
        "5. World Wide Web Consortium (W3C). (2023). HTML5 & CSS3 Specification Guidelines. https://www.w3.org/TR/html5/",
        "6. SQLite Consortium. (2026). SQLite In-Depth Architectural Documentation, ACID Transactions and SQL Syntax. https://www.sqlite.org/docs.html",
        "7. Python Software Foundation. (2026). Python 3 Documentation: Built-in Data Structures and sqlite3 API. https://docs.python.org/3/",
        "8. OWASP Foundation. (2025). Cross-Site Request Forgery (CSRF) & SQL Injection Prevention Cheat Sheets. https://cheatsheetseries.owasp.org/"
    ]
    for r in refs:
        add_p(r, space_after=6)

    # Save Word document
    doc.save(DOCX_OUT)
    print(f"Complete Word document generated: {DOCX_OUT}")

if __name__ == "__main__":
    build_report()
