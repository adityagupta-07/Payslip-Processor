"""Payslip Processor package."""

from .config import Employee
from .excel_reader import user_input, load_excel_file, matching_row_numbers
from .employee_parser import get_employee_block, empty_nested_dict, get_details_per_employee
from .docx_generator import fill_placeholders_in_docx, docx_creation
from .pdf_converter import batch_convert_docx_to_pdf, batch_convert_docx_to_pdf1, master_pdf_creation
from .file_utils import delete_contents
from .directories import PathConfig
from .delete_contents import delete_contents
from .gui import launch_gui
from .constants import *

__all__ = [
    "Employee", "PathConfig", "user_input", "load_excel_file", "matching_row_numbers",
    "get_employee_block", "empty_nested_dict", "get_details_per_employee",
    "fill_placeholders_in_docx", "docx_creation",
    "batch_convert_docx_to_pdf", "batch_convert_docx_to_pdf1", "master_pdf_creation",
    "delete_contents", delete_contents, launch_gui
]