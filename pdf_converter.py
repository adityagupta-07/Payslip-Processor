import os
import dxpdf
from docx2pdf import convert
import pymupdf

def batch_convert_docx_to_pdf(input_dir, output_dir):
    # MS Word Independent (but messes up the format)
    for filename in os.listdir(input_dir):
        if filename.endswith(".docx") and not filename.startswith("~$"):
            docx_path = os.path.join(input_dir, filename)
            pdf_filename = filename.rsplit(".", 1)[0] + ".pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)
            try:
                with open(docx_path, "rb") as f:
                    docx_bytes = f.read()
                pdf_bytes = dxpdf.convert(docx_bytes)
                with open(pdf_path, "wb") as f:
                    f.write(pdf_bytes)
            except Exception as e:
                print(f"Failed to convert {filename}. Error: {e}")
    return

def batch_convert_docx_to_pdf1(input_dir, output_dir):
    # MS Word Dependent (Preserves the format)
    convert(input_dir, output_dir)
    return

def master_pdf_creation(individual_pdfs_folder, master_pdf_dir, month, year): 
    pdf_name_list = os.listdir(individual_pdfs_folder)
    result = pymupdf.open()
    for pdf in pdf_name_list:
        with pymupdf.open(f"{individual_pdfs_folder}/{pdf}") as mfile:
            result.insert_pdf(mfile)
    output_path = f"{master_pdf_dir}/Payslip - {month} {year}.pdf"
    result.save(output_path)
    result.close()
    return