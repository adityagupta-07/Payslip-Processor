from .config import Employee
from .constants import ExcelConstants
from typing import Any
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

excel_constants = ExcelConstants()


class ScanState:
    """Updates the state of found_ssf_contribution_by_employer."""

    def __init__(self) -> None:
        self.found_ssf_contribution_by_employer = False


def cell_matches(cell: Cell, search_string: str) -> bool:
    """Check whether a cell's value matches the given search string."""

    return cell.value == search_string


def row_matches(row: list[Cell], search_string: str) -> bool:
    """Check whether any cell in a row matches the given search string."""

    return any(cell_matches(cell, search_string) for cell in row)


def matching_row_numbers(
    search_string: str,
    sheet: Worksheet,
) -> set[int]:
    """Find all row numbers containing the given search string."""
    matching_rows: set[int] = set()

    for row in sheet.iter_rows():
        if row_matches(row, search_string):
            matching_rows.add(row[0].row)

    return matching_rows


def get_employee_block(
    sheet: Worksheet,
    string1: str,
    string2: str,
) -> list[tuple[int, int]]:
    """Find employee block boundaries."""
    string1_rows = matching_row_numbers(string1, sheet)
    string2_rows = matching_row_numbers(string2, sheet)

    return list(zip(string1_rows, string2_rows))


def clean_cell_value(cell: Cell) -> Any:
    """Get the value from a cell and remove spaces if it is text."""
    if isinstance(cell.value, str):
        return cell.value.strip()

    return cell.value


def set_money_value_for_attribute(
    employee_obj: Employee,
    attribute: str,
    value: int | float,
) -> None:
    """Set an employee attribute with numbers formatted as Rupees."""
    if isinstance(value, (int, float)):
        formatted_value = f"Rs. {value:,.2f}"
        employee_obj.set_atr(attribute, formatted_value)
    # else:
    #     employee_obj.set_atr(attribute, value)


def set_ssf_employer_amount(
    employee_obj: Employee,
    atr_name: str,
    value: int | float,
) -> None:
    """Set a formatted SSF employer contribution amount."""
    employee_obj.set_atr(
        excel_constants.get_atr(atr_name),
        f"Rs. {value:,.2f}",
    )


def set_financial_year_note(
    employee_obj: Employee,
    sheet: Worksheet,
    row: int,
    target_cell: Cell,
) -> None:
    """Set the employee's financial year note from the worksheet."""
    financial_year_note = sheet.cell(
        row=row,
        column=target_cell.column + 2,
    ).value

    employee_obj.set_atr(
        excel_constants.get_atr("FINANCIAL_YEAR_NOTE"),
        financial_year_note,
    )


def handle_ssf_employer(
    employee_obj: Employee,
    sheet: Worksheet,
    row: int,
    target_cell: Cell,
    next_cell: Cell,
    state: ScanState,
) -> None:
    """
    Handle SSF employer contribution.
    """
    if state.found_ssf_contribution_by_employer:
        set_ssf_employer_amount(
            employee_obj,
            "SSF_EMPLOYER_LOWER",
            next_cell.value,
        )
        return

    set_ssf_employer_amount(
        employee_obj,
        "SSF_EMPLOYER_UPPER",
        next_cell.value,
    )

    set_financial_year_note(
        employee_obj,
        sheet, row,
        target_cell,
    )


def handle_month_year(
    employee_obj: Employee,
    sheet: Worksheet,
    row: int,
    target_cell: Cell,
    target_value: str,
) -> None:
    """Store the month/year value in both raw and readable formats."""
    next_cell = sheet.cell(
        row=row,
        column=target_cell.column + 1,
    )

    # Store the original datetime value
    employee_obj.set_atr(
        excel_constants.get_atr("MONTH_YEAR"),
        next_cell.value,
    )

    # Store formatted form "May 2026".
    employee_obj.set_atr(
        target_value,
        next_cell.value.strftime("%b %Y"),
    )


def process_cell(
    employee_obj: Employee,
    sheet: Worksheet,
    block: tuple[int, int],
    row: int,
    target_cell: Cell,
    state: ScanState,
) -> bool:
    """Process cells."""
    target_value = clean_cell_value(target_cell)

    # Does this cell contain an attribute that we care about?
    if not employee_obj.check_attribute(str(target_value)):
        return False

    next_cell = sheet.cell(
        row=row,
        column=target_cell.column + 1,
    )

    # Handle SSF employer separately.
    if excel_constants.get_atr("SSF_EMPLOYER") in target_value:
        was_already_found = state.found_ssf_contribution_by_employer

        handle_ssf_employer(
            employee_obj,
            sheet, row,
            target_cell,
            next_cell,
            state,
        )

        if was_already_found:
            return True

    is_money_value = (
        isinstance(next_cell.value, (int, float))
        and row > block[1] - 13
        and row < block[1] + 1
    )

    if is_money_value:
        set_money_value_for_attribute(
            employee_obj,
            str(target_value),
            next_cell.value,
        )
    else:
        employee_obj.set_atr(
            str(target_value),
            next_cell.value,
        )

    # Handle the month/year field separately.
    if row == block[1] - 2 and target_cell.column == 3:
        handle_month_year(
            employee_obj,
            sheet, row,
            target_cell,
            str(target_value),
        )

    return False


def get_details_per_employee(
    sheet: Worksheet,
    block: tuple[int, int],
    employee_obj: Employee,
) -> Employee:
    """Read employee information from the given Excel file."""
    state = ScanState()

    start_row = block[0]
    end_row = block[1]

    for row in range(start_row, end_row + 1):
        for target_cell in sheet[row]:
            should_break = process_cell(
                employee_obj,
                sheet,
                block,
                row,
                target_cell,
                state,
            )

            if should_break:
                break

    return employee_obj