import base64
import tempfile
from pathlib import Path
from .pipeline import main as run_pipeline


def validate_year(year: str) -> None:
    """Check that year is a valid folder name."""
    if Path(year).name != year:
        raise ValueError("Year must be a folder name, like 2083-84.")


def validate_employee_folders(employee_folders: list[str], year: str) -> None:
    """Check that at least one employee folder was found."""
    if not employee_folders:
        raise ValueError(f"No employee folder contains a '{year}' folder.")


def create_workspace(temp_folder: Path) -> dict[str, Path]:
    """Return the paths for the job's working files and folders."""
    return {
        "excel_file": temp_folder / "Payslips.xlsx",
        "output_folder": temp_folder / "Payslips",
        "sharepoint_folder": temp_folder / "Sharepoint",
    }


def create_sharepoint_folder_skeleton(folder: Path, employee_folders: list[str], year: str) -> Path:
    """Create empty employee/year folders that look like the real SharePoint folder.
    Returns a path of '2083-84' folder, which is needed by the pipeline.
    """
    year_folders = [folder / name / year for name in employee_folders]

    for year_folder in year_folders:
        year_folder.mkdir(parents=True)

    return year_folders[0]


def prepare_workspace(excel_bytes: bytes, paths: dict[str, Path], employee_folders: list[str], year: str) -> Path:
    """Save the Excel file, create the folders, and return the year folder from sharepoint folder."""
    paths["excel_file"].write_bytes(excel_bytes)
    paths["output_folder"].mkdir()
    year_folder = create_sharepoint_folder_skeleton(paths["sharepoint_folder"], employee_folders, year)

    return year_folder


def read_files_as_base64(folder: Path) -> list[dict]:
    """Read every file in the fed folder so it can be sent to the web page for writing into host disk."""
    files = []

    for path in sorted(folder.rglob("*")):
        if path.is_file():
            files.append({
                "path": path.relative_to(folder).as_posix(),
                "data": base64.b64encode(path.read_bytes()).decode(),
            })

    return files


def collect_results(output_folder: Path, sharepoint_folder: Path, messages: list[str]) -> dict:
    """Collect the generated files and the warning messages."""
    return {
        "output": read_files_as_base64(output_folder),
        "sharepoint": read_files_as_base64(sharepoint_folder),
        "messages": messages
    }


def generate_payslips(excel_bytes: bytes, employee_folders: list[str], year: str) -> dict:
    """Run the pipeline in a temporary folder and return its files with path and content in base64."""

    validate_year(year)
    validate_employee_folders(employee_folders, year)

    with tempfile.TemporaryDirectory() as temp:
        paths = create_workspace(Path(temp))

        year_folder = prepare_workspace(excel_bytes, paths, employee_folders, year)

        messages = run_pipeline(paths["excel_file"], paths["output_folder"], year_folder)

        return collect_results(paths["output_folder"], paths["sharepoint_folder"], messages)