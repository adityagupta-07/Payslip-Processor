from pathlib import Path

import pytest
from openpyxl import Workbook
from pypdf import PdfReader, PdfWriter

from src import get_payslip_paths, extract_pan_from_pdf, extract_pan_from_table, get_next_non_empty_value, protect_pdf


def create_pdf(file_path: Path, text: str = "Test PDF") -> None:
    """Create a simple real PDF for testing"""
    writer = PdfWriter()
    writer.add_blank_page(width=600, height=750)

    with file_path.open("wb") as output_file:
        writer.write(output_file)


def test_get_payslip_paths(tmp_path):
    pdf_file = tmp_path / "payslip.pdf"
    txt_file = tmp_path / "notes.txt"
    pdf_file.touch()
    txt_file.touch()
    result = get_payslip_paths(tmp_path)

    assert result == [pdf_file, txt_file]


def test_get_payslip_paths_empty_folder(tmp_path):
    result = get_payslip_paths(tmp_path)

    assert result == []


def test_get_payslip_paths_ignores_directories(tmp_path):
    pdf_file = tmp_path / "payslip.pdf"
    directory = tmp_path / "folder"

    pdf_file.touch()
    directory.mkdir()
    result = get_payslip_paths(tmp_path)

    assert result == [pdf_file]


def test_get_payslip_paths_missing_folder(tmp_path):
    missing_folder = tmp_path / "missing"

    with pytest.raises(FileNotFoundError):
        get_payslip_paths(missing_folder)


def test_extract_pan_from_table():
    table = [
        ["Name", "John Doe", None],
        ["PAN", None, "123456789"],
    ]
    result = extract_pan_from_table(table)
    assert result == "123456789"


def test_extract_pan_from_table_pan_with_empty_cells():
    table = [
        ["Name", "John Doe"],
        ["PAN", None, "", "123456789"],
    ]
    result = extract_pan_from_table(table)
    assert result == "123456789"


def test_extract_pan_from_table_pan_lowercase():
    table = [
        ["Name", "John Doe"],
        ["pan", "123456789"],
    ]
    result = extract_pan_from_table(table)
    assert result == "123456789"


def test_extract_pan_from_table_pan_not_found():
    table = [
        ["Name", "John Doe"],
        ["Address", "Kathmandu"],
    ]

    result = extract_pan_from_table(table)
    assert result is None


def test_extract_pan_from_table_pan_without_value():
    table = [
        ["Name", "John Doe"],
        ["PAN", None, ""],
    ]
    result = extract_pan_from_table(table)
    assert result is None


def test_extract_pan_from_table_empty_table():
    result = extract_pan_from_table([])

    assert result is None


def test_extract_pan_from_table_empty_rows():
    table = [
        [],
        [None, None],
        ["Name", "John Doe"],
    ]
    result = extract_pan_from_table(table)

    assert result is None


def test_get_next_non_empty_value():
    row = ["PAN", None, "", "123456789"]
    result = get_next_non_empty_value(row, 1)

    assert result == "123456789"


def test_get_next_non_empty_value_immediate_value():
    row = ["PAN", "123456789"]
    result = get_next_non_empty_value(row, 1)

    assert result == "123456789"


def test_get_next_non_empty_value_no_value():
    row = ["PAN", None, ""]
    result = get_next_non_empty_value(row, 1)

    assert result is None


def test_get_next_non_empty_value_start_index_at_end():
    row = ["PAN", "123456789"]
    result = get_next_non_empty_value(row, 2)

    assert result is None


def test_get_next_non_empty_value_start_index_zero():
    row = ["123456789", None, "PAN"]
    result = get_next_non_empty_value(row, 0)

    assert result == "123456789"


def test_protect_pdf(tmp_path):
    input_path = tmp_path / "input.pdf"
    output_path = tmp_path / "protected.pdf"
    create_pdf(input_path)
    protect_pdf(input_path, output_path, "123456789")
    reader = PdfReader(output_path)

    assert reader.is_encrypted is True


def test_protect_pdf_output_exists(tmp_path):
    input_path = tmp_path / "input.pdf"
    output_path = tmp_path / "protected.pdf"
    create_pdf(input_path)
    protect_pdf(input_path, output_path, "password")

    assert output_path.exists()


def test_protect_pdf_requires_password(tmp_path):
    input_path = tmp_path / "input.pdf"
    output_path = tmp_path / "protected.pdf"
    create_pdf(input_path)
    protect_pdf(input_path, output_path, "secret")
    reader = PdfReader(output_path)
    reader.decrypt("secret")

    assert len(reader.pages) == 1


def test_protect_pdf_wrong_password_fails(tmp_path):
    input_path = tmp_path / "input.pdf"
    output_path = tmp_path / "protected.pdf"
    create_pdf(input_path)
    protect_pdf(input_path, output_path, "correct-password")
    reader = PdfReader(output_path)
    result = reader.decrypt("wrong-password")

    assert result == 0


def test_extract_pan_from_pdf_no_pan(tmp_path):
    pdf_path = tmp_path / "payslip.pdf"
    create_pdf(pdf_path)
    result = extract_pan_from_pdf(pdf_path)

    assert result is None
