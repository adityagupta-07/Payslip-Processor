import shutil
from docxtpl import DocxTemplate
from .config import Employee
from .directories import PathConfig
from .constants import *

def fill_placeholders_in_docx(employee_obj: Employee):
    return {
        "MONTH_YEAR_UPPER": f"{employee_obj.get_atr(MONTH_YEAR).strftime("%B").upper()} {employee_obj.get_atr(MONTH_YEAR).strftime("%Y")}",
        "EMPLOYEE_ID": employee_obj.get_atr(EMPLOYEE_ID),
        "EMPLOYEE_NAME": employee_obj.get_atr(EMPLOYEE_NAME), 
        "DESIGNATION": employee_obj.get_atr(DESIGNATION), 
        "PAN": employee_obj.get_atr(PAN),
        "CONTACT_NUMBER": employee_obj.get_atr(CONTACT_NUMBER), 
        "BASIC_SALARY": employee_obj.get_atr(BASIC_SALARY), 
        "ALLOWANCES": employee_obj.get_atr(ALLOWANCES), 
        "GROSS_SALARY": employee_obj.get_atr(GROSS_SALARY), 
        "GROSS_SALARY_WORKING_HOURS": employee_obj.get_atr(GROSS_SALARY_AS_PER_WORKING_HOURS), 
        "UPPER_SSF_EMPLOYER": employee_obj.get_atr(SSF_EMPLOYER_UPPER), 
        "BONUS": employee_obj.get_atr(BONUS), 
        "TOTAL": employee_obj.get_atr(TOTAL), 
        "LOWER_SSF_EMPLOYER": employee_obj.get_atr(SSF_EMPLOYER_LOWER), 
        "SSF_EMPLOYEE": employee_obj.get_atr(SSF_EMPLOYEE), 
        "TDS_FOR_MONTH": employee_obj.get_atr(TDS_FOR_THE_MONTH), 
        "TOTAL_DEDUCTION": employee_obj.get_atr(TOTAL_DEDUCTION), 
        "NET_SALARY_PAID": employee_obj.get_atr(NET_SALARY_PAID), 
        "ACCOUNT_NUMBER": employee_obj.get_atr(ACCOUNT_NUMBER), 
        "BANK_NAME": employee_obj.get_atr(BANK_NAME), 
        "BRANCH": employee_obj.get_atr(BRANCH), 
        "MARITAL_STATUS": employee_obj.get_atr(MARITAL_STATUS), 
        "ANNUAL_TAXABLE_SALARY": employee_obj.get_atr(ANNUAL_TAXABLE_SALARY), 
        "ANNUAL_SSF_DEPOSIT": employee_obj.get_atr(ANNUAL_SSF_DEPOSIT), 
        "ANNUAL_TDS_PAYMENT": employee_obj.get_atr(ANNUAL_TDS_PAYMENT), 
        "ANNUAL_NET_SALARY": employee_obj.get_atr(ANNUAL_NET_SALARY), 
        "FINANCIAL_YEAR_NOTE": employee_obj.get_atr(FINANCIAL_YEAR_NOTE), 
        "MONTH_YEAR": employee_obj.get_atr(MONTH)
    }

def docx_creation(employee: Employee, path: PathConfig, placeholders_with_values):
    month_name = employee.get_atr(MONTH_YEAR).strftime("%B")
    year = employee.get_atr(MONTH_YEAR).strftime("%Y")
    if employee.get_atr(EMPLOYEE_ID) == "":
        template_file = path.get_template_no_id_path
        file_name = (f"{employee.get_atr(EMPLOYEE_NAME).strip().replace(" ", "_")}_{month_name}_{year}")
    else:
        template_file = path.get_template_id_path
        file_name = (f"{employee.get_atr(EMPLOYEE_NAME).strip().replace(" ", "_")}_{month_name}_{year}_{str(employee.get_atr(EMPLOYEE_ID)).strip()}")
    destination_file = f"{path.get_docs_folder_path}/{file_name}.docx"  
    shutil.copy2(template_file, destination_file)  
    doc = DocxTemplate(destination_file) 
    doc.render(placeholders_with_values)
    doc.save(destination_file)
    return
