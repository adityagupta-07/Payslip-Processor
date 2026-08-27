from python_docx_replace import docx_replace
from docx import Document
from datetime import datetime
import calendar
import openpyxl

current_month_num = 1
current_year = 0
def user_input():
    file_path = input("Provide file path: ")
    global current_year 
    current_year = datetime.now().year
    global current_month_num 
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

data_dict1 = {
    "SSF Contribution by Employer": "",
    "Financial_Year_Note": ""
}



emp = 0
for employee in employee_block:
    data_dict = {key: "" for key in data_dict}
    data_dict1 = {key: "" for key in data_dict1}
    found_ssf_contribution_by_employer = False
    for r in range(employee[0], employee[1] + 1): # r loops from 1 to 19
        for target_cell in sheet[r]: # target_cell loops through the cells in row(r), means row(1), row(2), row(3), ...
            target_value = target_cell.value.strip() if isinstance(target_cell.value, str) else target_cell.value            
            if target_value in data_dict:
                next_cell = sheet.cell(row=r, column=(target_cell.column+1))
                if found_ssf_contribution_by_employer is True and "SSF Contribution by Employer" in target_value:
                    data_dict1[target_value] = next_cell.value
                    break
                if "SSF Contribution by Employer" in target_value:
                    found_ssf_contribution_by_employer = True
                    data_dict1["Financial_Year_Note"] = sheet.cell(row=r, column=(target_cell.column+2)).value
                data_dict[target_value] = next_cell.value          
    # print(f"Employee no.: {emp+1}")
    emp += 1
    # print(data_dict)   
    # print(data_dict1)
    if data_dict["Employee ID"] != "":
        print(f"{data_dict["Employee Name"].strip().replace(" ", "_")}_{calendar.month_name[current_month_num].strip()}_{str(datetime.now().year).strip()}_{data_dict['Employee ID'].strip()}")
    else:
        print(f"{data_dict["Employee Name"].strip().replace(" ", "_")}_{calendar.month_name[current_month_num].strip()}_{str(datetime.now().year).strip()}")






