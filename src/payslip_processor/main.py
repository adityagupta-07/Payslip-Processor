from datetime import datetime
import copy
# from gui import launch_gui
from src.payslip_processor import (
    new_employee_dictionary, fill_placeholders_in_docx, docx_creation,
    get_employee_block, empty_nested_dict, get_details_per_employee,
    user_input, load_excel_file, matching_row_numbers, batch_convert_docx_to_pdf1, 
    master_pdf_creation, delete_contents, output_folder_path, delete_contents, 
    get_template_no_id_path, get_template_id_path, get_docs_path, get_individual_pdfs_folder,
    get_master_pdf_folder, launch_gui
)

def main(input_excel_file_path):

    delete_contents(output_folder_path())
    
    if input_excel_file_path is None:
        input_excel_file_path = user_input()
    sheet = load_excel_file(input_excel_file_path)

    employee_blocks = get_employee_block(sheet, "EMPLOYEE INFORMATION", "Net Salary Paid", matching_row_numbers)


    employee_details = [] # stores dictionary per employee in a list
    for block in employee_blocks: #[(1, 19), (22, 41), ......]
        employee_dict = new_employee_dictionary()
        # employee_dict = empty_nested_dict(employee_dict)
        employee_dict = get_details_per_employee(sheet, block, employee_dict)
        employee_details.append(copy.deepcopy(employee_dict)) # Without copy.deepcopy(), it appends reference to the same underlying dictionary every time. With copy.deepcopy(), it appends a fresh original dictionary, not its reference or instance.

    for employee in employee_details:
        placeholders_in_docx_with_values = fill_placeholders_in_docx(employee)
        docx_creation(employee, placeholders_in_docx_with_values, get_template_id_path, get_template_no_id_path, get_docs_path)

    # docs_folder = "./Files/Docs"
    # individual_pdfs_folder = "./Files/PDFs/Individual PDFs"
    # batch_convert_docx_to_pdf(docs_folder, destination_folder) # messes up format
    batch_convert_docx_to_pdf1(get_docs_path(), get_individual_pdfs_folder()) # preserves format

    # master_pdf_dir = "./Files/PDFs/Master PDF"
    master_pdf_creation(
        get_individual_pdfs_folder(), get_master_pdf_folder(),
        employee_details[0]["specials"]["Month_year"].strftime("%B"), 
        employee_details[0]["specials"]["Month_year"].strftime("%Y")
    )

if __name__ == "__main__":
    # main(None) 
    launch_gui(main, get_master_pdf_folder())

