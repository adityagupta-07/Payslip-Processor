from pathlib import Path
from types import SimpleNamespace
import pytest
from src import write_files_into_local_sharepoint_folder as write_sharepoint_files


def make_paths(folder: Path) -> SimpleNamespace:
    """Create the paths object needed by these functions."""
    return SimpleNamespace(protected_individual_pdf_folder_path=folder)


def test_get_cleaned_name():
    path = Path("Sushil_Kumar_Gupta_May_2026_21.pdf")

    assert write_sharepoint_files.get_cleaned_name(path) == "Sushil Kumar Gupta May 2026 21"


@pytest.mark.parametrize(
    "month",
    [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December",
        "may", "MAY",
    ],
)
def test_check_month_returns_true_for_months(month):
    assert write_sharepoint_files.check_month(month) is True


@pytest.mark.parametrize("word", ["Rohit", "2026", "May2026", ""])
def test_check_month_returns_false_for_non_months(word):
    assert write_sharepoint_files.check_month(word) is False


def test_get_employee_name_from_protected_pdf():
    assert (
        write_sharepoint_files.get_employee_name_from_protected_pdf(
            "Rohit Sharma May 2026 11"
        ) == "Rohit Sharma"
    )


def test_get_employee_id_from_protected_pdf():
    assert (
        write_sharepoint_files.get_employee_id_from_protected_pdf(
            "Rohit Sharma May 2026 11"
        ) == 11
    )


def test_get_month_from_protected_pdf():
    assert (
        write_sharepoint_files.get_month_from_protected_pdf(
            "Rohit Sharma May 2026 11"
        ) == "May"
    )


def test_dict_of_password_protected_pdfs_returns_only_pdfs(tmp_path):
    (tmp_path / "Rohit_Sharma_May_2026_11.pdf").touch()
    (tmp_path / "Priya_Sharma_June_2026_12.PDF").touch()
    (tmp_path / "notes.txt").touch()
    (tmp_path / "subfolder").mkdir()

    result = write_sharepoint_files.dict_of_password_protected_pdfs(make_paths(tmp_path))

    assert len(result) == 2
    assert all(path.suffix.lower() == ".pdf" for path in result)
    assert result[tmp_path / "Rohit_Sharma_May_2026_11.pdf"] == ("Rohit Sharma May 2026 11")


@pytest.mark.parametrize(
    ("folder_name", "expected"),
    [
        ("Emp_11 - Rohit Sharma", "Rohit Sharma"),
        ("Emp_11 Rohit Sharma", "Rohit Sharma"),
        ("Emp - Rohit  Sharma", "Rohit Sharma"),
        ("Emp Rohit Sharma", "Rohit Sharma"),
        ("Rohit  Sharma", "Rohit Sharma"),
    ],
)
def test_get_emp_name_from_emp_dir(tmp_path, folder_name, expected):
    employee_dir = tmp_path / folder_name / "2083-84"

    assert write_sharepoint_files.get_emp_name_from_emp_dir(employee_dir) == expected


def test_get_emp_id_from_emp_dir(tmp_path):
    employee_dir = tmp_path / "Emp_11 - Rohit Sharma" / "2083-84"

    assert write_sharepoint_files.get_emp_id_from_emp_dir(employee_dir) == 11


def test_get_emp_id_from_emp_dir_raises_for_invalid_name(tmp_path):
    employee_dir = tmp_path / "Rohit Sharma" / "2083-84"

    with pytest.raises(ValueError, match="must start with"):
        write_sharepoint_files.get_emp_id_from_emp_dir(employee_dir)


def test_list_of_local_employee_folders_from_sharepoint(tmp_path):
    payslips = tmp_path / "Payslips"
    (payslips / "Emp_11 - Rohit Sharma" / "2083-84").mkdir(parents=True)
    (payslips / "Emp_12 - Priya Sharma" / "2083-84").mkdir(parents=True)
    (payslips / "notes.txt").touch()

    sharepoint_path = (payslips / "Emp_11 - Rohit Sharma" / "2083-84")

    result = write_sharepoint_files.list_of_local_employee_folders_from_sharepoint(sharepoint_path)

    assert set(result) == {
        payslips / "Emp_11 - Rohit Sharma" / "2083-84",
        payslips / "Emp_12 - Priya Sharma" / "2083-84",
    }


def test_write_files_copies_pdf_to_employee_folder(tmp_path):
    payslips = tmp_path / "Payslips"
    employee_year = (payslips / "Emp_11 - Rohit Sharma" / "2083-84")
    employee_year.mkdir(parents=True)

    protected = tmp_path / "protected"
    protected.mkdir()
    pdf = protected / "Rohit_Sharma_May_2026_11.pdf"
    pdf.write_bytes(b"fake PDF content")

    messages = write_sharepoint_files.write_files_locally_in_sharepoint_folder(
        make_paths(protected), employee_year
    )

    assert messages == []
    assert (employee_year / "May.pdf").read_bytes() == b"fake PDF content"


def test_write_files_warns_when_employee_folder_not_found(tmp_path):
    payslips = tmp_path / "Payslips"
    employee_year = (payslips / "Emp_99 - Someone Else" / "2083-84")
    employee_year.mkdir(parents=True)

    protected = tmp_path / "protected"
    protected.mkdir()
    (protected / "Rohit_Sharma_May_2026_11.pdf").touch()

    messages = write_sharepoint_files.write_files_locally_in_sharepoint_folder(
        make_paths(protected), employee_year
    )

    assert messages == ["No destination folder found for Rohit Sharma"]
