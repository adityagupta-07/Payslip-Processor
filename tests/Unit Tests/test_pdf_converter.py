from pathlib import Path
import pytest
import pymupdf
from src import append_pdf, build_libreoffice_command, create_master_pdf, create_master_pdf_path, get_docx_files, get_pdf_files, save_master_pdf

def test_get_docx_files_returns_docx_files(tmp_path: Path):
    (tmp_path / "one.docx").touch()
    (tmp_path / "two.docx").touch()
    (tmp_path / "notes.txt").touch()
    (tmp_path / "~$temporary.docx").touch()
    result = get_docx_files(tmp_path)
    assert sorted(result) == sorted(
        [tmp_path / "one.docx", tmp_path / "two.docx"]
    )


def test_get_docx_files_returns_empty_list_when_no_docx_files(tmp_path: Path):
    (tmp_path / "notes.txt").touch()
    result = get_docx_files(tmp_path)

    assert result == []


def test_get_docx_files_raises_for_missing_directory(tmp_path: Path):
    missing_dir = tmp_path / "missing"
    with pytest.raises(FileNotFoundError):
        get_docx_files(missing_dir)

    assert True


def test_build_libreoffice_command_returns_expected_command(tmp_path: Path):
    docx_files = [tmp_path / "one.docx", tmp_path / "two.docx"]
    output_dir = tmp_path / "pdfs"
    result = build_libreoffice_command(docx_files, output_dir)

    assert result == [
        "libreoffice",
        "-env:UserInstallation=file:///tmp/lo_profile",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir),
        str(tmp_path / "one.docx"),
        str(tmp_path / "two.docx"),
    ]


def test_build_libreoffice_command_handles_empty_file_list(tmp_path: Path):
    output_dir = tmp_path / "pdfs"
    result = build_libreoffice_command([], output_dir)
    assert result == [
        "libreoffice",
        "-env:UserInstallation=file:///tmp/lo_profile",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir),
    ]


def test_get_pdf_files_returns_pdf_files(tmp_path: Path):
    (tmp_path / "one.pdf").touch()
    (tmp_path / "two.PDF").touch()
    (tmp_path / "notes.txt").touch()
    result = get_pdf_files(tmp_path)
    assert sorted(result) == sorted(
        [tmp_path / "one.pdf", tmp_path / "two.PDF"]
    )


def test_get_pdf_files_returns_empty_list_when_no_pdf_files(tmp_path: Path):
    (tmp_path / "notes.txt").touch()
    result = get_pdf_files(tmp_path)
    assert result == []


def test_get_pdf_files_raises_for_missing_directory(tmp_path: Path):
    missing_dir = tmp_path / "missing"
    with pytest.raises(FileNotFoundError):
        get_pdf_files(missing_dir)

    assert True


def test_create_master_pdf_returns_empty_document():
    result = create_master_pdf()

    assert len(result) == 0
    result.close()


def test_create_master_pdf_path_returns_expected_path(tmp_path: Path):
    result = create_master_pdf_path(tmp_path, "September", 2026)

    assert result == tmp_path / "Payslip - September 2026.pdf"


def test_create_master_pdf_path_handles_empty_month(tmp_path: Path):
    result = create_master_pdf_path(tmp_path, "", 2026)

    assert result == tmp_path / "Payslip -  2026.pdf"


def test_append_pdf_appends_pages(tmp_path: Path):
    source_path = tmp_path / "source.pdf"
    source_pdf = pymupdf.open()
    source_pdf.new_page()
    source_pdf.save(source_path)
    source_pdf.close()
    master_pdf = pymupdf.open()
    append_pdf(master_pdf, source_path)

    assert len(master_pdf) == 1
    master_pdf.close()


def test_append_pdf_raises_for_missing_pdf(tmp_path: Path):
    master_pdf = pymupdf.open()
    missing_pdf = tmp_path / "missing.pdf"
    with pytest.raises(pymupdf.FileNotFoundError):
        append_pdf(master_pdf, missing_pdf)

    master_pdf.close()



def test_save_master_pdf_creates_pdf_file(tmp_path: Path):
    output_path = tmp_path / "master.pdf"
    master_pdf = pymupdf.open()
    master_pdf.new_page()
    save_master_pdf(master_pdf, output_path)

    assert output_path.exists()
    master_pdf.close()


def test_save_master_pdf_raises_when_output_directory_does_not_exist(
    tmp_path: Path,
):
    output_path = tmp_path / "missing" / "master.pdf"
    master_pdf = pymupdf.open()
    master_pdf.new_page()
    with pytest.raises(pymupdf.mupdf.FzErrorSystem):
        save_master_pdf(master_pdf, output_path)
    master_pdf.close()

