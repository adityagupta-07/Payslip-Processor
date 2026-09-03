import shutil
from docxtpl import DocxTemplate

def fill_placeholders_in_docx(employee):
    return {
        "MONTH_YEAR_UPPER": f"{employee["specials"]["Month_year"].strftime("%B").upper()} {employee["specials"]["Month_year"].strftime("%Y")}",
        "EMPLOYEE_ID": employee["Employee ID"], 
        "EMPLOYEE_NAME": employee["Employee Name"], 
        "DESIGNATION": employee["Designation"], 
        "PAN": employee["PAN"],
        "CONTACT_NUMBER": employee["Contact Number"], 
        "BASIC_SALARY": employee["Basic Salary"], 
        "ALLOWANCES": employee["Allowances"], 
        "GROSS_SALARY": employee["Gross Salary"], 
        "GROSS_SALARY_WORKING_HOURS": employee["Gross Salary as per working hours"], 
        "SSF_EMPLOYER": employee["SSF Contribution by Employer"], 
        "BONUS": employee["Bonus"], 
        "TOTAL": employee["Total"], 
        "SSF_EMPLOYER1": employee["duplicates"]["SSF Contribution by Employer"], 
        "SSF_EMPLOYEE": employee["SSF Contribution by Employee"], 
        "TDS_FOR_MONTH": employee["TDS for the month"], 
        "TOTAL_DEDUCTION": employee["Total Deduction"], 
        "NET_SALARY_PAID": employee["Net Salary Paid"], 
        "ACCOUNT_NUMBER": employee["Account Number"], 
        "BANK_NAME": employee["Bank Name"], 
        "BRANCH": employee["Branch"], 
        "MARITAL_STATUS": employee["Marital Status"], 
        "ANNUAL_TAXABLE_SALARY": employee["Annual Taxable Salary"], 
        "ANNUAL_SSF_DEPOSIT": employee["Annual SSF deposit"], 
        "ANNUAL_TDS_PAYMENT": employee["Annual TDS Payment"], 
        "ANNUAL_NET_SALARY": employee["Annual Net Salary"], 
        "FINANCIAL_YEAR_NOTE": employee["specials"]["Financial_Year_Note"], 
        "MONTH_YEAR": employee["Month"]
    }

def docx_creation(employee, placeholders_with_values):
    month_name = employee["specials"]["Month_year"].strftime("%B")
    year = employee["specials"]["Month_year"].strftime("%Y")
    if employee["Employee ID"] == "":
        template_file = "Files/Templates/Template_no_id.docx"
        file_name = (f"{employee["Employee Name"].strip().replace(" ", "_")}_{month_name}_{year}")
    else:
        template_file = "Files/Templates/Template_id.docx"
        file_name = (f"{employee["Employee Name"].strip().replace(" ", "_")}_{month_name}_{year}_{str(employee['Employee ID']).strip()}")
    destination_file = f"Files/Docs/{file_name}.docx"  
    shutil.copy2(template_file, destination_file)  
    doc = DocxTemplate(destination_file) 
    doc.render(placeholders_with_values)
    doc.save(destination_file)
    return
