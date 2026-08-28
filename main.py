from python_docx_replace import docx_replace
from docx import Document
from docxtpl import DocxTemplate
from datetime import datetime
from docx2pdf import convert
import dxpdf
import calendar
import openpyxl
import shutil
import os

current_month_num = 1
current_year = 0
def user_input():
    file_path = input("Provide file path: ")
    global current_year 
    current_year = datetime.now().year
    global current_month_num 
    current_month_num = int(datetime.now().month)
    year = input(f"Current year: {current_year}. \nEnter year to overwrite or press enter to skip: ")  
    current_year = int(year) if year != "" else current_year
    month = input(f"Current month: {calendar.month_name[current_month_num]}. \nEnter month in number to overwrite or press enter to skip: ")
    current_month_num = int(month) if month != "" else current_month_num
    return {
        "file_path": file_path.replace('"', ''),
        "year": current_year,
        "month": calendar.month_name[current_month_num]
    }

user_input = user_input()

workbook = openpyxl.load_workbook(user_input["file_path"], data_only=True)
sheet = workbook.active

def row_range_per_employee_block(search_string):
    matching_rows = []
    for target_row in sheet.iter_rows():
        for cell in target_row:
            if cell.value == search_string:
                if cell.row not in matching_rows:
                    matching_rows.append(cell.row)
    return matching_rows

employee_information_row_numbers = row_range_per_employee_block("EMPLOYEE INFORMATION")
net_salary_paid_row_numbers = row_range_per_employee_block("Net Salary Paid")

employee_block = list(zip(employee_information_row_numbers, net_salary_paid_row_numbers))

data_dict = {
    "Employee ID": "",
    "Employee Name": "",
    "Designation": "",
    "PAN": "",
    "Contact Number": "",
    "Basic Salary": "",
    "Allowances": "",
    "Gross Salary": "",
    "Gross Salary as per working hours": "",
    "SSF Contribution by Employer": "",
    "Bonus": "",
    "Total": "",
    "SSF Contribution by Employee": "", 
    "TDS for the month": "", 
    "Total Deduction": "", 
    "Net Salary Paid": "", 
    "Account Number": "", 
    "Bank Name": "",
    "Branch": "",
    "Marital Status": "",
    "Annual Taxable Salary": "",
    "Annual SSF deposit": "",
    "Annual TDS Payment": "",
    "Annual Net Salary": "",
    "Month": ""
}

data_dict1 = {
    "SSF Contribution by Employer": "",
    "Financial_Year_Note": ""
}

def placeholders_docx_with_id():
    return {
        "MONTH_YEAR_UPPER": f"{user_input["month"].upper()} {user_input["year"]}",
        "EMPLOYEE_ID": data_dict["Employee ID"], 
        "EMPLOYEE_NAME": data_dict["Employee Name"], 
        "DESIGNATION": data_dict["Designation"], 
        "PAN": data_dict["PAN"],
        "CONTACT_NUMBER": data_dict["Contact Number"], 
        "BASIC_SALARY": data_dict["Basic Salary"], 
        "ALLOWANCES": data_dict["Allowances"], 
        "GROSS_SALARY": data_dict["Gross Salary"], 
        "GROSS_SALARY_WORKING_HOURS": data_dict["Gross Salary as per working hours"], 
        "SSF_EMPLOYER": data_dict["SSF Contribution by Employer"], 
        "BONUS": data_dict["Bonus"], 
        "TOTAL": data_dict["Total"], 
        "SSF_EMPLOYER1": data_dict1["SSF Contribution by Employer"], 
        "SSF_EMPLOYEE": data_dict["SSF Contribution by Employee"], 
        "TDS_FOR_MONTH": data_dict["TDS for the month"], 
        "TOTAL_DEDUCTION": data_dict["Total Deduction"], 
        "NET_SALARY_PAID": data_dict["Net Salary Paid"], 
        "ACCOUNT_NUMBER": data_dict["Account Number"], 
        "BANK_NAME": data_dict["Bank Name"], 
        "BRANCH": data_dict["Branch"], 
        "MARITAL_STATUS": data_dict["Marital Status"], 
        "ANNUAL_TAXABLE_SALARY": data_dict["Annual Taxable Salary"], 
        "ANNUAL_SSF_DEPOSIT": data_dict["Annual SSF deposit"], 
        "ANNUAL_TDS_PAYMENT": data_dict["Annual TDS Payment"], 
        "ANNUAL_NET_SALARY": data_dict["Annual Net Salary"], 
        "FINANCIAL_YEAR_NOTE": data_dict1["Financial_Year_Note"], 
        "MONTH_YEAR": data_dict["Month"]
    }

def delete_contents(folder_path):
    shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

delete_contents("Tmp")
delete_contents("PDFs")

emp = 0
for employee in employee_block:
    found_ssf_contribution_by_employer = False
    for r in range(employee[0], employee[1] + 1): # r loops from 1 to 19
        for target_cell in sheet[r]: # target_cell loops through the cells in row(r), means row(1), row(2), row(3), ...
            target_value = target_cell.value.strip() if isinstance(target_cell.value, str) else target_cell.value            
            if target_value in data_dict:
                next_cell = sheet.cell(row=r, column=(target_cell.column+1))
                if found_ssf_contribution_by_employer is True and "SSF Contribution by Employer" in target_value:
                    data_dict1[target_value] = f"Rs. {next_cell.value:,.2f}"
                    break
                if "SSF Contribution by Employer" in target_value:
                    found_ssf_contribution_by_employer = True
                    data_dict1["Financial_Year_Note"] = sheet.cell(row=r, column=(target_cell.column+2)).value
                if isinstance(next_cell.value, (int, float)) and (r > employee[1]-13 and r < employee[1]+1):
                    data_dict[target_value] = f"Rs. {next_cell.value:,.2f}"
                else:
                    data_dict[target_value] = next_cell.value
                if r == (employee[1]-2) and target_cell.column == 3:
                    # next_cell.value is returning <class 'datetime.datetime'> (2026-05-01 00:00:00) so we can change the format (%B = August, %Y = 2026)
                    data_dict[target_value] = next_cell.value.strftime("%B %Y")
    placeholder = placeholders_docx_with_id()
    if data_dict["Employee ID"] != "":
        file_name = (f"{data_dict["Employee Name"].strip().replace(" ", "_")}_{calendar.month_name[current_month_num].strip()}_{str(user_input["year"]).strip()}_{str(data_dict['Employee ID']).strip()}")
        destination_file = f"Tmp/{file_name}.docx"
        shutil.copy2("Templates/Template_id.docx", destination_file)    
        doc = DocxTemplate(destination_file) 
        doc.render(placeholder)
        doc.save(destination_file)
    else:
        file_name = (f"{data_dict["Employee Name"].strip().replace(" ", "_")}_{calendar.month_name[current_month_num].strip()}_{str(user_input["year"]).strip()}")
        destination_file = f"Tmp/{file_name}.docx"
        shutil.copy2("Templates/Template_no_id.docx", destination_file)  
        doc = DocxTemplate(destination_file) 
        doc.render(placeholder)
        doc.save(destination_file)
    data_dict = {key: "" for key in data_dict}
    data_dict1 = {key: "" for key in data_dict1}

# Docx to Pdf conversion
def batch_convert_docx_to_pdf(input_dir, output_dir):
    # MS Word Independent (but messes up the format)
    for filename in os.listdir(input_dir):
        if filename.endswith(".docx") and not filename.startswith("~$"):
            docx_path = os.path.join(input_dir, filename)
            pdf_filename = filename.rsplit(".", 1)[0] + ".pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)
            
            try:
                with open(docx_path, "rb") as f:
                    docx_bytes = f.read()
                
                pdf_bytes = dxpdf.convert(docx_bytes)
                
                with open(pdf_path, "wb") as f:
                    f.write(pdf_bytes)
                # print(f"Created: {pdf_filename}")

            except Exception as e:
                print(f"Failed to convert {filename}. Error: {e}")

    # MS Word Dependent (Preserves the format)
    # convert(input_dir, output_dir)


docs_folder = "./Tmp"
destination_folder = "./PDFs"

batch_convert_docx_to_pdf(docs_folder, destination_folder)


