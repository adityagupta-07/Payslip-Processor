from python_docx_replace import docx_replace
from docx import Document
from datetime import datetime
import calendar
import openpyxl

def user_input():
    file_path = input("Provide file path: ")
    current_year = datetime.now().year
    current_month_num = int(datetime.now().month)
    year = input(f"Current year: {current_year}. \nEnter year to overwrite or press enter to skip: ")  
    current_year = year if year != "" else current_year
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
    "SSF Contribution by Employer": "",
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
    "Month": "",
    "Method": ""
}


for employee in employee_block:
    print(f"Employee block: {employee}") # employee = (1, 19) tuple 
    for r in range(employee[0], employee[1] + 1): # r loops from 1 to 19
        for target_cell in sheet[r]: # target_cell loops through the cells in row(r), means row(1), row(2), row(3), ...
            target_value = target_cell.value.strip() if isinstance(target_cell.value, str) else target_cell.value            
            if target_value in data_dict:
                next_cell = sheet.cell(row=r, column=(target_cell.column+1))
                data_dict[target_value] = next_cell.value
                

    print(data_dict)   

