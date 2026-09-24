import openpyxl

def get_file_path() -> str:
    return input("Provide file path: ")


def clean_file_path(file_path: str) -> str:
    return file_path.replace('"', "")


def load_workbook(file_path: str) -> openpyxl.Workbook:
    return openpyxl.load_workbook(file_path, data_only=True)


def get_active_sheet(workbook: openpyxl.Workbook):
    return workbook.active