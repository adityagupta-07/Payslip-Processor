import shutil
from docxtpl import DocxTemplate
from src.payslip_processor import Employee

def fill_placeholders_in_docx(employee_obj: Employee):
    return {
        "MONTH_YEAR_UPPER": f"{employee_obj.get_atr("Month_year").strftime("%B").upper()} {employee_obj.get_atr("Month_year").strftime("%Y")}",
        "EMPLOYEE_ID": employee_obj.get_atr("Employee ID"),
        "EMPLOYEE_NAME": employee_obj.get_atr("Employee Name"), 
        "DESIGNATION": employee_obj.get_atr("Designation"), 
        "PAN": employee_obj.get_atr("PAN"),
        "CONTACT_NUMBER": employee_obj.get_atr("Contact Number"), 
        "BASIC_SALARY": employee_obj.get_atr("Basic Salary"), 
        "ALLOWANCES": employee_obj.get_atr("Allowances"), 
        "GROSS_SALARY": employee_obj.get_atr("Gross Salary"), 
        "GROSS_SALARY_WORKING_HOURS": employee_obj.get_atr("Gross Salary as per working hours"), 
        "UPPER_SSF_EMPLOYER": employee_obj.get_atr("Upper SSF Contribution by Employer"), 
        "BONUS": employee_obj.get_atr("Bonus"), 
        "TOTAL": employee_obj.get_atr("Total"), 
        "LOWER_SSF_EMPLOYER": employee_obj.get_atr("Lower SSF Contribution by Employer"), 
        "SSF_EMPLOYEE": employee_obj.get_atr("SSF Contribution by Employee"), 
        "TDS_FOR_MONTH": employee_obj.get_atr("TDS for the month"), 
        "TOTAL_DEDUCTION": employee_obj.get_atr("Total Deduction"), 
        "NET_SALARY_PAID": employee_obj.get_atr("Net Salary Paid"), 
        "ACCOUNT_NUMBER": employee_obj.get_atr("Account Number"), 
        "BANK_NAME": employee_obj.get_atr("Bank Name"), 
        "BRANCH": employee_obj.get_atr("Branch"), 
        "MARITAL_STATUS": employee_obj.get_atr("Marital Status"), 
        "ANNUAL_TAXABLE_SALARY": employee_obj.get_atr("Annual Taxable Salary"), 
        "ANNUAL_SSF_DEPOSIT": employee_obj.get_atr("Annual SSF deposit"), 
        "ANNUAL_TDS_PAYMENT": employee_obj.get_atr("Annual TDS Payment"), 
        "ANNUAL_NET_SALARY": employee_obj.get_atr("Annual Net Salary"), 
        "FINANCIAL_YEAR_NOTE": employee_obj.get_atr("Financial_Year_Note"), 
        "MONTH_YEAR": employee_obj.get_atr("Month")
    }

def docx_creation(employee: Employee, placeholders_with_values, get_template_id_path, get_template_no_id_path, get_docs_path):
    month_name = employee.get_atr("Month_year").strftime("%B")
    year = employee.get_atr("Month_year").strftime("%Y")
    if employee.get_atr("Employee ID") == "":
        template_file = get_template_no_id_path() 
        file_name = (f"{employee.get_atr("Employee Name").strip().replace(" ", "_")}_{month_name}_{year}")
    else:
        template_file = get_template_id_path()
        file_name = (f"{employee.get_atr("Employee Name").strip().replace(" ", "_")}_{month_name}_{year}_{str(employee.get_atr("Employee ID")).strip()}")
    destination_file = f"{get_docs_path()}/{file_name}.docx"  
    shutil.copy2(template_file, destination_file)  
    doc = DocxTemplate(destination_file) 
    doc.render(placeholders_with_values)
    doc.save(destination_file)
    return
