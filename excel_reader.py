import openpyxl

def user_input():
    file_path = input("Provide file path: ")
    return file_path.replace('"', '')

def load_excel_file(user_input):
    workbook = openpyxl.load_workbook(user_input, data_only=True)
    return workbook.active

def matching_row_numbers(search_string, sheet):
    matching_rows = []
    for target_row in sheet.iter_rows():
        for cell in target_row:
            if cell.value == search_string:
                if cell.row not in matching_rows:
                    matching_rows.append(cell.row)
    return matching_rows