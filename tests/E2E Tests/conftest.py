import subprocess
import sys
from types import SimpleNamespace
import pytest
from config import EXCEL_FILE, PACKAGE_NAME, PROJECT_FOLDER


@pytest.fixture(scope="session")
def run(tmp_path_factory):
    """Run the whole pipeline once for the Excel file."""
    assert EXCEL_FILE.is_file(), f"Excel file not found: {EXCEL_FILE}"

    out_dir = tmp_path_factory.mktemp("output")

    result = subprocess.run(
        [sys.executable, "-m", PACKAGE_NAME],
        input=f"{EXCEL_FILE}\n{out_dir}\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=PROJECT_FOLDER,
        timeout=900,
    )

    root = out_dir / "Ultra Payslips"
    return SimpleNamespace(
        excel_file=EXCEL_FILE,
        result=result,
        root=root,
        docx_dir=root / "docx",
        individual_dir=root / "pdf" / "individual_pdfs",
        master_dir=root / "pdf" / "master_pdf",
        protected_dir=root / "pdf" / "protected_individual_pdfs",
        template_dir=PROJECT_FOLDER / PACKAGE_NAME / "templates" / "docx",
    )