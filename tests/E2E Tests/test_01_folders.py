import pytest

SUB_FOLDERS = [
    "docx",
    "pdf",
    "pdf/individual_pdfs",
    "pdf/master_pdf",
    "pdf/protected_individual_pdfs",
]


def test_program_finished_cleanly(run) -> None:
    assert run.error is None, f"generate_payslips failed: {run.error!r}"
    assert set(run.result) == {"output", "sharepoint", "messages"}


def test_main_folder_created(run) -> None:
    assert run.root.is_dir()


@pytest.mark.parametrize("sub_folder", SUB_FOLDERS)
def test_sub_folders_created(run, sub_folder: str) -> None:
    assert (run.root / sub_folder).is_dir()
