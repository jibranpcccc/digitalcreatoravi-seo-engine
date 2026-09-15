#!/usr/bin/env python3
"""
Filter MASTER_LIVE_BACKLINKS_REPORT.xlsx and .csv to contain exclusively 100% verified live backlinks.
Guarantees zero 400/404/0 errors in the final published reporting deliverables.
"""

import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
CSV_PATH = os.path.join(REPORTS_DIR, "MASTER_LIVE_BACKLINKS_REPORT.csv")
XLSX_PATH = os.path.join(REPORTS_DIR, "MASTER_LIVE_BACKLINKS_REPORT.xlsx")

def main():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    live_rows = [r for r in rows if r["Live Verified"] == "YES"]
    print(f"Total rows: {len(rows)}, Verified live: {len(live_rows)}")

    # Re-number records
    for idx, r in enumerate(live_rows, 1):
        r["Record #"] = str(idx)

    # 1. Rewrite CSV
    fieldnames = list(live_rows[0].keys())
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(live_rows)
    print(f"[+] Updated CSV with {len(live_rows)} pristine verified backlinks.")

    # 2. Rewrite Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Master Verified Backlinks"

    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    pass_fill = PatternFill(start_color="ECFDF5", end_color="ECFDF5", fill_type="solid")
    pass_font = Font(name="Calibri", size=10, color="065F46", bold=True)
    border_thin = Border(
        left=Side(style='thin', color='E2E8F0'), right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'), bottom=Side(style='thin', color='E2E8F0')
    )

    ws.append(fieldnames)
    for col_idx in range(1, len(fieldnames) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for row_idx, r in enumerate(live_rows, 2):
        row_vals = [r[k] for k in fieldnames]
        ws.append(row_vals)
        for col_idx in range(1, len(fieldnames) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.border = border_thin
            if fieldnames[col_idx - 1] in ("HTTP Status", "Live Verified"):
                cell.fill = pass_fill
                cell.font = pass_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 65)

    wb.save(XLSX_PATH)
    print(f"[+] Updated Excel with {len(live_rows)} pristine verified backlinks.")

if __name__ == "__main__":
    main()
