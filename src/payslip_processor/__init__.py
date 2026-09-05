"""Payslip Processor package."""

from .config import new_employee_dictionary
from .excel_reader import user_input, load_excel_file, matching_row_numbers
from .employee_parser import get_employee_block, empty_nested_dict, get_details_per_employee
from .docx_generator import fill_placeholders_in_docx, docx_creation
from .pdf_converter import batch_convert_docx_to_pdf, batch_convert_docx_to_pdf1, master_pdf_creation
from .file_utils import delete_contents
from .directories import output_folder_path, get_template_id_path, get_template_no_id_path, get_docs_path, get_individual_pdfs_folder, get_master_pdf_folder
from .delete_contents import delete_contents
from .gui import launch_gui

__all__ = [
    "new_employee_dictionary",
    "user_input", "load_excel_file", "matching_row_numbers",
    "get_employee_block", "empty_nested_dict", "get_details_per_employee",
    "fill_placeholders_in_docx", "docx_creation",
    "batch_convert_docx_to_pdf", "batch_convert_docx_to_pdf1", "master_pdf_creation",
    "delete_contents", output_folder_path, delete_contents, get_template_no_id_path, 
    get_template_id_path, get_docs_path, get_individual_pdfs_folder, get_master_pdf_folder,
    launch_gui
]