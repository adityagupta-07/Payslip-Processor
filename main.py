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


wb_obj = openpyxl.load_workbook(user_input["file_path"])
sheet_obj = wb_obj.active

row = sheet_obj.max_row
column = sheet_obj.max_column

print("Total Rows:", row)
print("Total Columns:", column)