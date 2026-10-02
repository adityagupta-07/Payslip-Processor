import openpyxl
from pathlib import Path


def matching_rows(sheet, text):
    """Row numbers of the cells that equal 'text' exactly."""

    rows = []
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value == text and cell.row not in rows:
                rows.append(cell.row)
    return rows


def count_employees_in_excel(excel_file):
    sheet = openpyxl.load_workbook(excel_file, data_only=True).active
    return len(matching_rows(sheet, "Net Salary Paid"))


def pdfs_in(folder):
    return sorted(Path(folder).glob("*.pdf"))