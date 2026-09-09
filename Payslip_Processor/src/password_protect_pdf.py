from pathlib import Path
import pdfplumber

from .directories import PathConfig

path = PathConfig()

payslips = []
payslip_paths = []

individual_pdf_folder_path = Path(path.get_individual_pdfs_folder_path)
password_protected_pdf_folder_path = Path(path.get_protected_individual_pdf_folder_path)

for item in individual_pdf_folder_path.iterdir():
    if item.is_file():
        payslips.append(item.name)
        payslip_paths.append(item)

for payslip in payslip_paths:
    pdf_path = payslip
    protected_pdf_path = password_protected_pdf_folder_path / pdf_path.name
    password = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()

            if table:
                for row in table:
                    for i, cell in enumerate(row):
                        if cell is not None and cell.upper() == "PAN":
                            for cell in row[i + 1:]: # iterate over elements after "PAN" to the end in the row
                                if cell is not None: # select the next non none value in same row after finding "PAN"
                                    password = cell
                                    print(f"{payslip.name}, {"PAN"}: {password}")
                                    break