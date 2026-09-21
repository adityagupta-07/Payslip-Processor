import os, pymupdf, subprocess
# import os, pymupdf, subprocess
# from docx2pdf import convert
from .directories import PathConfig

# def batch_convert_docx_to_pdf(paths: PathConfig):
#     # MS Word Independent (but messes up the format)
#     input_dir = paths.get_docs_folder_path
#     output_dir = paths.get_individual_pdfs_folder_path
#     for filename in os.listdir(input_dir):
#         if filename.endswith(".docx") and not filename.startswith("~$"):
#             docx_path = os.path.join(input_dir, filename)
#             pdf_filename = filename.rsplit(".", 1)[0] + ".pdf"
#             pdf_path = os.path.join(output_dir, pdf_filename)
#             try:
#                 with open(docx_path, "rb") as f:
#                     docx_bytes = f.read()
#                 pdf_bytes = dxpdf.convert(docx_bytes)
#                 with open(pdf_path, "wb") as f:
#                     f.write(pdf_bytes)
#             except Exception as e:
#                 print(f"Failed to convert {filename}. Error: {e}")
#     return

# def batch_convert_docx_to_pdf1(paths: PathConfig):
#     # MS Word Dependent (Preserves the format)
#     input_dir = paths.get_docs_folder_path
#     output_dir = paths.get_individual_pdfs_folder_path
#     convert(input_dir, output_dir)
#     return

def batch_convert_docx_to_pdf2(paths: PathConfig):
    # LibreOffice Dependent (Preserves the format)
    input_dir = paths.output_docs_folder_path
    output_dir = paths.individual_pdfs_folder_path
    output_dir.mkdir(parents=True, exist_ok=True)
    for docx_path in input_dir.iterdir():
        if docx_path.suffix == ".docx" and not docx_path.name.startswith("~$"):
            try:
                subprocess.run(
                    ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(docx_path)],
                    check=True, capture_output=True, text=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Failed to convert {docx_path.name}. " f"Error: {e.stderr}")
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