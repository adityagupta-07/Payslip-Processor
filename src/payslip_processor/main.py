from src.payslip_processor import (
    Employee, fill_placeholders_in_docx, docx_creation,
    get_employee_block, empty_nested_dict, get_details_per_employee,
    user_input, load_excel_file, matching_row_numbers, batch_convert_docx_to_pdf1, 
    master_pdf_creation, delete_contents, output_folder_path, delete_contents, 
    get_template_no_id_path, get_template_id_path, get_docs_path, get_individual_pdfs_folder,
    get_master_pdf_folder, launch_gui, get_output_pdfs_folder
)

def main(input_excel_file_path):

    delete_contents(output_folder_path())
    
    if input_excel_file_path is None:
        input_excel_file_path = user_input()
    sheet = load_excel_file(input_excel_file_path)

    employee_blocks = get_employee_block(sheet, "EMPLOYEE INFORMATION", "Net Salary Paid", matching_row_numbers)

    for block in employee_blocks: #[(1, 19), (22, 41), ......]
        employee_obj = Employee()
        employee_obj = get_details_per_employee(sheet, block, employee_obj)
        placeholders_in_docx_with_values = fill_placeholders_in_docx(employee_obj)
        docx_creation(employee_obj, placeholders_in_docx_with_values, get_template_id_path, get_template_no_id_path, get_docs_path)

    # batch_convert_docx_to_pdf(docs_folder, destination_folder) # messes up format
    batch_convert_docx_to_pdf1(get_docs_path(), get_individual_pdfs_folder()) # preserves format

    master_pdf_creation(
        get_individual_pdfs_folder(), get_master_pdf_folder(),
        employee_obj.get_atr("Month_year").strftime("%B"), 
        employee_obj.get_atr("Month_year").strftime("%Y")
    )

if __name__ == "__main__":
    # main(None) 
    launch_gui(main, get_output_pdfs_folder())

