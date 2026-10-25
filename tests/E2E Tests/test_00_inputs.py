"""Tests for the helper that finds the employee folders. These run in a normal pytest run too."""

from pathlib import Path
from config import Inputs, find_employee_folders

YEAR = "2083-84"


def make_payslips_folder(tmp_path: Path) -> Path:
    payslips = tmp_path / "Payslips"
    for path in [
        (payslips / "Emp_11 - Rohit Sharma" / YEAR),
        (payslips / "Emp_12 - Anita KC" / YEAR),
        (payslips / "Emp_12 - Anita KC" / "2082-83"),
        (payslips / "Emp_13 - Old Year Only" / "2082-83"),
    ]:
        path.mkdir(parents=True, exist_ok=True)
    (payslips / "readme.txt").write_text("an extra file")
    return payslips


def test_only_folders_with_the_year_are_found(tmp_path: Path) -> None:
    payslips = make_payslips_folder(tmp_path)

    assert find_employee_folders(payslips, YEAR) == ["Emp_11 - Rohit Sharma", "Emp_12 - Anita KC"]


def test_a_file_named_like_the_year_does_not_count(tmp_path: Path) -> None:
    payslips = make_payslips_folder(tmp_path)
    (payslips / "Emp_14 - File Only").mkdir()
    (payslips / "Emp_14 - File Only" / YEAR).write_text("I am a file")

    assert "Emp_14 - File Only" not in find_employee_folders(payslips, YEAR)


def test_no_matching_folders_gives_an_empty_list(tmp_path: Path) -> None:
    payslips = make_payslips_folder(tmp_path)

    assert find_employee_folders(payslips, "1999-00") == []


def test_run_inputs_builds_the_employee_folder_list(tmp_path: Path) -> None:
    payslips = make_payslips_folder(tmp_path)
    inputs = Inputs(tmp_path / "payslips.xlsx", payslips, YEAR)

    assert inputs.get_employee_folders() == ["Emp_11 - Rohit Sharma", "Emp_12 - Anita KC"]
