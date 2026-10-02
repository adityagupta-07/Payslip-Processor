import pytest


def test_program_finished_cleanly(run):
    message = f"STDOUT:\n{run.result.stdout}\nSTDERR:\n{run.result.stderr}"
    assert run.result.returncode == 0, message
    assert "Traceback" not in run.result.stderr, message
    assert "Traceback" not in run.result.stdout, message


def test_main_folder_created(run):
    assert run.root.is_dir()


@pytest.mark.parametrize(
    "sub_folder",
    ["docx", "pdf", "pdf/individual_pdfs", "pdf/master_pdf", "pdf/protected_individual_pdfs"],
)
def test_sub_folders_created(run, sub_folder):
    assert (run.root / sub_folder).is_dir()
