import openpyxl

def user_input():
    file_path = input("Provide file path: ")
    return file_path.replace('"', '')

def load_excel_file(input_file_path):
    workbook = openpyxl.load_workbook(input_file_path, data_only=True)
    return workbook.active

