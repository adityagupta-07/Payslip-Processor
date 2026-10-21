from directories import PathConfig
from pathlib import Path
import shutil

def get_cleaned_name(pdf_path: Path) -> str:
    """Return cleaned pdf name from fed pdf path.
    'Sushil Kumar Gupta May 2026 21' from
    'C:\Coding\Python\try\data\input\Ultra Payslips\pdf\protected_individual_pdfs\Sushil_Kumar_Gupta_May_2026_21.pdf'
    """

    return pdf_path.stem.replace("_", " ").strip()


def check_month(word: str) -> bool:
    """Checks if a word is month."""

    months = [
        "january", "february", "march", "april", "may", "june", 
        "july", "august", "september", "october", "november", "december"
    ]

    return True if word.lower() in months else False


def get_employee_name(name: str) -> str:
    """Returns name of employee.
    'Rohit Sharma' from 'Rohit Sharma May 2026 11'
    """

    words = name.split()
    words_list = []

    for word in words:
        if check_month(word):
            break
        words_list.append(word)

    emp_name = " ".join(words_list)

    return emp_name


def dict_of_password_protected_pdfs(paths: PathConfig) -> dict[Path, str]:
    """Return dict of all the files in the protected pdfs folder (pdf path: pdf name)."""

    folder = Path(paths.protected_individual_pdf_folder_path)

    return {
        item: get_cleaned_name(item)
        for item in folder.iterdir()
        if item.is_file() and item.suffix.lower() == ".pdf"
    }

def list_of_local_employee_folders_from_sharepoint(local_sharepoint_folder_path: Path) -> list[Path]:
    """Return employee folder paths mapped to employee names."""

    local_sharepoint_folder_path = Path(local_sharepoint_folder_path)
    year_dir = local_sharepoint_folder_path.name
    emp_dir = local_sharepoint_folder_path.parent.parent

    return [
        item / year_dir
        for item in emp_dir.iterdir()
        if item.is_dir()
    ]

def write_files_locally_in_sharepoint_folder(paths, local_sharepoint_folder_path: Path):

    password_protected_pdfs = dict_of_password_protected_pdfs(paths)
    local_employee_folders_from_sharepoint = list_of_local_employee_folders_from_sharepoint(local_sharepoint_folder_path)

    for key, value in password_protected_pdfs.items():
        pdf_path = key
        emp_name = get_employee_name(value)

        for emp_dir in local_employee_folders_from_sharepoint:
            if emp_name.casefold() in str(emp_dir).casefold():
                if not emp_dir.is_dir():
                    print(f"Destination folder does not exist for {emp_name}")
                    break

                try:
                    shutil.copy(pdf_path, emp_dir)
                except Exception as e:
                    print(f"An error occurred: {e}")
                break

