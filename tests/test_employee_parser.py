import pytest
from openpyxl import Workbook

from src.employee_parser import (
    get_employee_block,
    get_details_per_employee,
    matching_row_numbers,
    normalize_cell_value,
)
from src.config import Employee


@pytest.fixture
def sheet():
    return Workbook().active


def test_matching_row_numbers(sheet):
    sheet["A1"] = "Employee"
    sheet["B2"] = "Employee"
    sheet["C2"] = "Other"

    result = matching_row_numbers("Employee", sheet)

    assert result == [1, 2]


def test_matching_row_numbers_no_match(sheet):
    sheet["A1"] = "Employee"
    sheet["B2"] = "Other"

    result = matching_row_numbers("Missing", sheet)

    assert result == []


def test_matching_row_numbers_duplicate_matches_same_row(sheet):
    sheet["A1"] = "Employee"
    sheet["B1"] = "Employee"
    sheet["C2"] = "Employee"

    result = matching_row_numbers("Employee", sheet)

    assert result == [1, 2]


def test_get_employee_block(sheet):
    sheet["A1"] = "Start"
    sheet["A3"] = "End"
    sheet["B5"] = "Start"
    sheet["B7"] = "End"

    result = get_employee_block(sheet, "Start", "End")

    assert result == [(1, 3), (5, 7)]


def test_get_employee_block_no_matching_start(sheet):
    sheet["A3"] = "End"

    result = get_employee_block(sheet, "Missing", "End")

    assert result == []


def test_get_employee_block_no_matching_end(sheet):
    sheet["A1"] = "Start"

    result = get_employee_block(sheet, "Start", "Missing")

    assert result == []


def test_get_employee_block_empty_sheet(sheet):
    result = get_employee_block(sheet, "Start", "End")

    assert result == []


def test_normalize_cell_value_with_string():
    result = normalize_cell_value("  Employee  ")

    assert result == "Employee"


def test_normalize_cell_value_with_empty_string():
    result = normalize_cell_value("")

    assert result == ""


def test_normalize_cell_value_with_whitespace_string():
    result = normalize_cell_value("   ")

    assert result == ""


def test_normalize_cell_value_with_non_string():
    result = normalize_cell_value(123)

    assert result == 123


def test_normalize_cell_value_with_none():
    result = normalize_cell_value(None)

    assert result is None


def test_normalize_cell_value_with_float():
    result = normalize_cell_value(123.45)

    assert result == 123.45


def test_get_details_per_employee(sheet):
    employee = Employee()

    sheet["A1"] = "Employee Name"
    sheet["B1"] = "John Doe"

    result = get_details_per_employee(sheet, (1, 1), employee)

    assert result is employee


def test_get_details_per_employee_empty_block(sheet):
    employee = Employee()

    result = get_details_per_employee(sheet, (1, 0), employee)

    assert result is employee


def test_get_details_per_employee_no_matching_attribute(sheet):
    employee = Employee()

    sheet["A1"] = "Unknown Field"
    sheet["B1"] = "Some Value"

    result = get_details_per_employee(sheet, (1, 1), employee)

    assert result is employee
