from .directories import PathConfig
from pathlib import Path
import shutil


def get_cleaned_name(pdf_path: Path) -> str:
    r"""Return cleaned pdf name from fed pdf path.
    'Sushil Kumar Gupta May 2026 21' from
    "C:\Coding\Python\try\data\input\Ultra Payslips\pdf\protected_individual_pdfs\Sushil_Kumar_Gupta_May_2026_21.pdf"
    """

    return pdf_path.stem.replace("_", " ").strip()


def check_month(word: str) -> bool:
    """Checks if a word is month."""

    months = [
        "january", "february", "march", "april", "may", "june", 
        "july", "august", "september", "october", "november", "december"
    ]

    return True if word.lower() in months else False


def get_employee_name_from_protected_pdf(name: str) -> str:
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


def get_employee_id_from_protected_pdf(name: str) -> int:
    """Returns employee id.
    '11' from from 'Rohit Sharma May 2026 11'
    """

    words = name.split()
    emp_id = int(words[-1].strip())
    return emp_id


def dict_of_password_protected_pdfs(paths: PathConfig) -> dict[Path, str]:
    """Return dict of all the files in the protected pdfs folder (pdf path: pdf name)."""

    folder = Path(paths.protected_individual_pdf_folder_path)

    return {
        item: get_cleaned_name(item)
        for item in folder.iterdir()
        if item.is_file() and item.suffix.lower() == ".pdf"
    }


def get_month_from_protected_pdf(name: str) -> str:
    """Returns month from pdf name.
    'May' from 'Rohit Sharma May 2026 11'
    """

    words = name.split()

    for word in words:
        if check_month(word):
            month = word

    return month


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


def get_emp_name_from_emp_dir(dir: Path) -> str:
    r"""Returns employee name from directory.
    'Rohit Sharma' from 
    "C:\Coding\Python\Sharepoint\Payslips\Emp_11 - Rohit Sharma\2083-84",
    "C:\Coding\Python\Sharepoint\Payslips\Emp_11 - Rohit  Sharma\2083-84", -> Double space between names
    "C:\Coding\Python\Sharepoint\Payslips\Emp_11 Rohit Sharma\2083-84",
    "C:\Coding\Python\Sharepoint\Payslips\Emp - Rohit Sharma\2083-84", 
    "C:\Coding\Python\Sharepoint\Payslips\Emp Rohit Sharma\2083-84", 
    "C:\Coding\Python\Sharepoint\Payslips\Emp Rohit  Sharma\2083-84" -> Double space between names
    "C:\Coding\Python\Sharepoint\Payslips\Rohit  Sharma\2083-84" -> Double space between names
    "C:\Coding\Python\Sharepoint\Payslips\Rohit Sharma\2083-84" 
    """

    emp_name = dir.parent.name.strip()

    if emp_name.startswith("Emp"):
        if "-" in emp_name:
            return " ".join(emp_name.split("-", 1)[1].split())
        return " ".join(emp_name.split()[1:])

    return " ".join(emp_name.split())


def get_emp_id_from_emp_dir(dir: Path) -> int:
    r"""Returns employee name from dir.
    '11' from 
    "C:\Coding\Python\Sharepoint\Payslips\Emp_11 - Rohit Sharma\2083-84",
    "C:\Coding\Python\Sharepoint\Payslips\Emp_11 - Rohit  Sharma\2083-84", -> Double space between names
    "C:\Coding\Python\Sharepoint\Payslips\Emp_11 Rohit Sharma\2083-84",  
    "C:\Coding\Python\Sharepoint\Payslips\Emp_11 Rohit  Sharma\2083-84" -> Double space between names
    """

    emp_dir = dir.parent.name.strip()

    if not emp_dir.startswith("Emp_"):
        raise ValueError('Directory name must start with "Emp_(id)..."')

    return int(emp_dir.split("_", 1)[1].split()[0])


def write_files_locally_in_sharepoint_folder(paths: PathConfig, local_sharepoint_folder_path: Path):
    password_protected_pdfs = dict_of_password_protected_pdfs(paths)
    local_employee_folders = list_of_local_employee_folders_from_sharepoint(local_sharepoint_folder_path)

    for protected_pdf_path, pdf_name in password_protected_pdfs.items():
        emp_name_from_pdf = get_employee_name_from_protected_pdf(pdf_name)
        emp_id_from_pdf = get_employee_id_from_protected_pdf(pdf_name)
        month_from_pdf = get_month_from_protected_pdf(pdf_name)

        # Find folders matching the employee name
        matching_folders = [
            emp_dir
            for emp_dir in local_employee_folders
            if emp_name_from_pdf.casefold() == get_emp_name_from_emp_dir(emp_dir).casefold()
        ]

        if not matching_folders:
            print(f"No destination folder found for {emp_name_from_pdf}")
            continue

        # If multiple folders have the same name, match by employee ID
        if len(matching_folders) > 1:
            matching_folders = [
                emp_dir
                for emp_dir in matching_folders
                if emp_id_from_pdf == get_emp_id_from_emp_dir(emp_dir)
            ]

        if len(matching_folders) != 1:
            print(f"Could not get unique destination folder for {emp_name_from_pdf} (ID: {emp_id_from_pdf})")
            continue

        destination_folder = matching_folders[0]

        try:
            shutil.copy(protected_pdf_path, destination_folder / f"{month_from_pdf}.pdf")
        except OSError as e:
            print(f"Failed to copy PDF for {emp_name_from_pdf}: {e}")