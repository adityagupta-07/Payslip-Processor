from .directories import PathConfig
from .delete_contents import delete_contents
from .excel_reader import user_input, load_excel_file, matching_row_numbers
from .employee_parser import get_details_per_employee, get_employee_block
from .config import Employee
from .docx_generator import fill_placeholders_in_docx, docx_creation
from .pdf_converter import master_pdf_creation, batch_convert_docx_to_pdf, batch_convert_docx_to_pdf1
from .password_protect_pdf import password_protect_pdfs

def main(input_excel_file_path):

    paths = PathConfig()
    delete_contents(paths)
    
    if input_excel_file_path is None:
        input_excel_file_path = user_input()
    sheet = load_excel_file(input_excel_file_path)

    employee_blocks = get_employee_block(sheet, "EMPLOYEE INFORMATION", "Net Salary Paid", matching_row_numbers)

    for block in employee_blocks: #[(1, 19), (22, 41), ......]
        employee_obj = Employee()
        employee_obj = get_details_per_employee(sheet, block, employee_obj)
        placeholders_in_docx_with_values = fill_placeholders_in_docx(employee_obj)
        docx_creation(employee_obj, paths, placeholders_in_docx_with_values)

    # batch_convert_docx_to_pdf(docs_folder, destination_folder) # messes up format
    batch_convert_docx_to_pdf1(paths) # preserves format

    master_pdf_creation(
        paths,
        employee_obj.get_atr("Month_year").strftime("%B"), 
        employee_obj.get_atr("Month_year").strftime("%Y")
    )

    password_protect_pdfs()





