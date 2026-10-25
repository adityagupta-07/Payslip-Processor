from pathlib import Path
import pytest

from helpers import pdfs_in


MESSAGE_STARTS = (
    "No destination folder found",
    "Could not get unique destination folder",
    "Failed to copy PDF",
)


def sharepoint_files(run) -> list[Path]:
    return sorted(path for path in run.sharepoint_dir.rglob("*") if path.is_file())


def test_every_protected_pdf_is_copied_or_reported(run) -> None:
    protected_count = len(pdfs_in(run.protected_dir))

    assert len(sharepoint_files(run)) + len(run.messages) == protected_count


def test_files_sit_under_employee_and_year_folder(run) -> None:
    for file in sharepoint_files(run):
        parts = file.relative_to(run.sharepoint_dir).parts

        assert len(parts) == 3, parts
        assert parts[0] in run.employee_folders
        assert parts[1] == run.year
        assert file.suffix == ".pdf"


def test_files_are_copies_of_the_protected_pdfs(run) -> None:
    protected_bytes = [path.read_bytes() for path in pdfs_in(run.protected_dir)]

    for file in sharepoint_files(run):
        assert file.read_bytes() in protected_bytes


def test_messages_are_of_the_expected_kinds(run) -> None:
    for message in run.messages:
        assert message.startswith(MESSAGE_STARTS), message
