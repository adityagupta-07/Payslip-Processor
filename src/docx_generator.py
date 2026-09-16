import shutil
from docxtpl import DocxTemplate
from .config import Employee
from .directories import PathConfig
from .constants import ExcelConstants, DocxConstants

excel_constants = ExcelConstants()
docx_constants = DocxConstants()

def fill_placeholders_in_docx(employee_obj: Employee):
    return {
        docx_constants.get_atr("MONTH_YEAR_UPPER"): f"{employee_obj.get_atr(excel_constants.MONTH_YEAR).strftime('%B').upper()} {employee_obj.get_atr(excel_constants.MONTH_YEAR).strftime('%Y')}",
        docx_constants.get_atr("EMPLOYEE_ID"): employee_obj.get_atr(excel_constants.EMPLOYEE_ID),
        docx_constants.get_atr("EMPLOYEE_NAME"): employee_obj.get_atr(excel_constants.EMPLOYEE_NAME),
        docx_constants.get_atr("DESIGNATION"): employee_obj.get_atr(excel_constants.DESIGNATION),
        docx_constants.get_atr("PAN"): employee_obj.get_atr(excel_constants.PAN),
        docx_constants.get_atr("CONTACT_NUMBER"): employee_obj.get_atr(excel_constants.CONTACT_NUMBER),
        docx_constants.get_atr("BASIC_SALARY"): employee_obj.get_atr(excel_constants.BASIC_SALARY),
        docx_constants.get_atr("ALLOWANCES"): employee_obj.get_atr(excel_constants.ALLOWANCES),
        docx_constants.get_atr("GROSS_SALARY"): employee_obj.get_atr(excel_constants.GROSS_SALARY),
        docx_constants.get_atr("GROSS_SALARY_WORKING_HOURS"): employee_obj.get_atr(excel_constants.GROSS_SALARY_AS_PER_WORKING_HOURS),
        docx_constants.get_atr("UPPER_SSF_EMPLOYER"): employee_obj.get_atr(excel_constants.SSF_EMPLOYER_UPPER),
        docx_constants.get_atr("BONUS"): employee_obj.get_atr(excel_constants.BONUS),
        docx_constants.get_atr("TOTAL"): employee_obj.get_atr(excel_constants.TOTAL),
        docx_constants.get_atr("LOWER_SSF_EMPLOYER"): employee_obj.get_atr(excel_constants.SSF_EMPLOYER_LOWER),
        docx_constants.get_atr("SSF_EMPLOYEE"): employee_obj.get_atr(excel_constants.SSF_EMPLOYEE),
        docx_constants.get_atr("TDS_FOR_MONTH"): employee_obj.get_atr(excel_constants.TDS_FOR_THE_MONTH),
        docx_constants.get_atr("TOTAL_DEDUCTION"): employee_obj.get_atr(excel_constants.TOTAL_DEDUCTION),
        docx_constants.get_atr("NET_SALARY_PAID"): employee_obj.get_atr(excel_constants.NET_SALARY_PAID),
        docx_constants.get_atr("ACCOUNT_NUMBER"): employee_obj.get_atr(excel_constants.ACCOUNT_NUMBER),
        docx_constants.get_atr("BANK_NAME"): employee_obj.get_atr(excel_constants.BANK_NAME),
        docx_constants.get_atr("BRANCH"): employee_obj.get_atr(excel_constants.BRANCH),
        docx_constants.get_atr("MARITAL_STATUS"): employee_obj.get_atr(excel_constants.MARITAL_STATUS),
        docx_constants.get_atr("ANNUAL_TAXABLE_SALARY"): employee_obj.get_atr(excel_constants.ANNUAL_TAXABLE_SALARY),
        docx_constants.get_atr("ANNUAL_SSF_DEPOSIT"): employee_obj.get_atr(excel_constants.ANNUAL_SSF_DEPOSIT),
        docx_constants.get_atr("ANNUAL_TDS_PAYMENT"): employee_obj.get_atr(excel_constants.ANNUAL_TDS_PAYMENT),
        docx_constants.get_atr("ANNUAL_NET_SALARY"): employee_obj.get_atr(excel_constants.ANNUAL_NET_SALARY),
        docx_constants.get_atr("FINANCIAL_YEAR_NOTE"): employee_obj.get_atr(excel_constants.FINANCIAL_YEAR_NOTE),
        docx_constants.get_atr("MONTH_YEAR"): employee_obj.get_atr(excel_constants.MONTH),
    }

def docx_creation(employee: Employee, path: PathConfig, placeholders_with_values):
    month_name = employee.get_atr(excel_constants.MONTH_YEAR).strftime("%B")
    year = employee.get_atr(excel_constants.MONTH_YEAR).strftime("%Y")
    if employee.get_atr(excel_constants.EMPLOYEE_ID) == "":
        template_file = path.get_template_no_id_path
        file_name = (f"{employee.get_atr(excel_constants.EMPLOYEE_NAME).strip().replace(" ", "_")}_{month_name}_{year}")
    else:
        template_file = path.get_template_id_path
        file_name = (f"{employee.get_atr(excel_constants.EMPLOYEE_NAME).strip().replace(" ", "_")}_{month_name}_{year}_{str(employee.get_atr(excel_constants.EMPLOYEE_ID)).strip()}")
    destination_file = f"{path.get_docs_folder_path}/{file_name}.docx"  
    shutil.copy2(template_file, destination_file)  
    doc = DocxTemplate(destination_file) 
    doc.render(placeholders_with_values)
    doc.save(destination_file)
    return
