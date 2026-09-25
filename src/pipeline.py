from datetime import datetime
from pathlib import Path
from .config import Employee
from .directories import PathConfig
from .excel_reader import user_input, load_excel_file
from .password_protect_pdf import password_protect_pdfs
from .docx_generator import fill_placeholders_in_docx, docx_creation
from .employee_parser import get_details_per_employee, get_employee_block
from .pdf_converter import master_pdf_creation, batch_convert_docx_to_pdf


def get_input_file(
    input_excel_file_path: str | Path | None
) -> str | Path:
    """Get the Excel file path from the user if it was not provided."""

    if input_excel_file_path is None:
        return user_input()

    return input_excel_file_path


def get_month_year(employee: Employee) -> datetime:
    """Get the month and year from the first employee processed."""

    return employee.get_atr("Month_year")


def create_employee_doc_per_emp(sheet, block, paths: PathConfig) -> Employee:
    """Create the DOCX file for one employee and return its Employee object."""
    employee_obj = Employee()

    filled_employee_obj = get_details_per_employee(sheet, block, employee_obj)
    placeholders_values = fill_placeholders_in_docx(filled_employee_obj)

    docx_creation(filled_employee_obj, paths, placeholders_values)

    return filled_employee_obj


def convert_docx_files_to_pdf(paths: PathConfig) -> None:
    """Convert every employee's DOCX file into its own PDF."""
    batch_convert_docx_to_pdf(paths)


def create_master_pdf(paths: PathConfig, month_year: datetime) -> None:
    """Combine every employee's PDF into one big master PDF."""
    master_pdf_creation(
        paths,
        month_year.strftime("%B"),
        month_year.strftime("%Y"),
    )


def main(
    input_excel_file_path: str | Path | None,
    paths: PathConfig
) -> None:
    """Create payslip PDFs from an Excel file."""

    input_excel_file_path = get_input_file(input_excel_file_path)

    paths.create_output_dir()

    sheet = load_excel_file(input_excel_file_path)

    employee_blocks = get_employee_block(
        sheet,
        "EMPLOYEE INFORMATION",
        "Net Salary Paid",
    )

    first_employee = None
    for block in employee_blocks:
        employee_obj = create_employee_doc_per_emp(sheet, block, paths)
        if first_employee is None:
            first_employee = employee_obj

    month_year = get_month_year(first_employee)

    convert_docx_files_to_pdf(paths)

    create_master_pdf(paths, month_year)

    password_protect_pdfs(paths)