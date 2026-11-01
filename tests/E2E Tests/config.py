from pathlib import Path


def clean_path(text: str) -> Path:
    """Turn str path into a Path."""
    return Path(text.strip().strip('"'))


def find_employee_folders(payslips_folder: Path, year: str) -> list[str]:
    """List of names of the folders inside payslips_folder that contain a folder named year like '2083-84')."""
    emp_folders_list = []

    for emp_folder in sorted(payslips_folder.iterdir()):
        if emp_folder.is_dir() and (emp_folder / year).is_dir():
            emp_folders_list.append(emp_folder.name)

    return emp_folders_list


class Inputs:
    def __init__(self, excel_file, payslips_folder, year):
        self.excel_file = excel_file
        self.payslips_folder = payslips_folder
        self.year = year

    def get_employee_folders(self):
        """Get employee folders that contain the specified year folder like '2083-84'.
        Employee folders with only different year like '2082-83' will be skipped.
        Employee folders with '2083-84' and '2082-83' will be included."""
        return find_employee_folders(self.payslips_folder, self.year)


def ask_for_inputs() -> Inputs:
    """Ask for the inputs."""
    excel_file = clean_path(input("Enter Excel file path: "))
    payslips_folder = clean_path(input("Enter Payslips folder path (contains the 'Emp_...' folders): "))
    year = input("Year folder name (e.g. 2083-84): ").strip()

    return Inputs(excel_file, payslips_folder, year)
