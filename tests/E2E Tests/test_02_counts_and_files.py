import pytest
from helpers import count_employees_in_excel, pdfs_in


def test_counts(run) -> None:
    expected = count_employees_in_excel(run.excel_file)
    docx_files = [p for p in run.docx_dir.glob("*.docx") if not p.name.startswith("~$")]
    assert len(docx_files) == expected
    assert len(pdfs_in(run.individual_dir)) == len(docx_files)


def test_exactly_one_master_pdf(run) -> None:
    assert len(pdfs_in(run.master_dir)) == 1


def test_no_temp_or_lock_files(run) -> None:
    leftovers = []
    for path in run.root.rglob("*"):
        name = path.name.lower()
        if (
            name.startswith("~$")
            or name.startswith(".~lock")
            or name.endswith(".tmp")
            or name.endswith(".lock")
        ):
            leftovers.append(str(path))
    assert leftovers == []


def test_file_types(run) -> None:
    unwanted_files = []
    for path in run.docx_dir.iterdir():
        if path.suffix.lower() != ".docx":
            unwanted_files.append(path)
    for folder in (run.individual_dir, run.master_dir, run.protected_dir):
        for path in folder.iterdir():
            if path.suffix.lower() != ".pdf":
                unwanted_files.append(path)
    assert unwanted_files == []
