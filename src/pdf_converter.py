import os, pymupdf, subprocess
from .directories import PathConfig
from pathlib import Path

def batch_convert_docx_to_pdf2(paths: PathConfig):
    # LibreOffice Dependent (Preserves the format)
    docx_dir = Path(paths.output_docs_folder_path)
    output_dir = Path(paths.individual_pdfs_folder_path)

    docx_files = []
    for p in docx_dir.iterdir():
        if p.suffix.lower() == ".docx" and not p.name.startswith("~$"):
            docx_files.append(str(p))

    if docx_files:
        try:
            subprocess.run(
                [
                    "libreoffice", 
                    "-env:UserInstallation=file:///tmp/lo_profile",
                    "--headless", 
                    "--convert-to", "pdf",
                    "--outdir", str(output_dir)] + docx_files,
                    check=True, capture_output=True, text=True
            )
            print(f"Successfully converted {len(docx_files)} files.")
        except subprocess.CalledProcessError as e:
            print(f"Batch conversion failed. Error: {e.stderr}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return

def master_pdf_creation(paths: PathConfig, month, year): 
    individual_pdfs_folder = paths.individual_pdfs_folder_path
    master_pdf_folder = paths.master_pdf_folder_path
    pdf_name_list = os.listdir(individual_pdfs_folder)
    result = pymupdf.open()
    for pdf in pdf_name_list:
        with pymupdf.open(f"{individual_pdfs_folder}/{pdf}") as mfile:
            result.insert_pdf(mfile)
    output_path = f"{master_pdf_folder}/Payslip - {month} {year}.pdf"
    result.save(output_path)
    result.close()
    return