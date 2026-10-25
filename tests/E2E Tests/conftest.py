from types import SimpleNamespace

import pytest

from config import Inputs, ask_for_inputs
from helpers import write_result_files
from src.payslip_runner import generate_payslips


@pytest.fixture(scope="session")
def run_inputs() -> Inputs:
    """Accepts Excel file path, Payslips folder and year from terminal."""
    try:
        inputs = ask_for_inputs()
    except OSError:
        pytest.skip('E2E tests ask for Excel file. Enable it with: pytest -s "tests/E2E Tests"')

    assert inputs.excel_file.is_file(), f"Excel file not found: {inputs.excel_file}"
    assert inputs.payslips_folder.is_dir(), f"Payslips folder not found: {inputs.payslips_folder}"
    return inputs


@pytest.fixture(scope="session")
def run(run_inputs: Inputs, tmp_path_factory: pytest.TempPathFactory) -> SimpleNamespace:
    output_dir = tmp_path_factory.mktemp("output")
    sharepoint_dir = tmp_path_factory.mktemp("sharepoint")

    employee_folders = run_inputs.get_employee_folders()

    result = None
    error = None
    try:
        result = generate_payslips(
            run_inputs.excel_file.read_bytes(),
            employee_folders,
            run_inputs.year,
        )
    except Exception as exc:
        error = exc

    if result is not None:
        write_result_files(output_dir, result["output"])
        write_result_files(sharepoint_dir, result["sharepoint"])

    root = output_dir / "Ultra Payslips"
    return SimpleNamespace(
        error=error,
        result=result,
        messages=result["messages"] if result else [],
        excel_file=run_inputs.excel_file,
        employee_folders=employee_folders,
        year=run_inputs.year,
        root=root,
        docx_dir=root / "docx",
        individual_dir=root / "pdf" / "individual_pdfs",
        master_dir=root / "pdf" / "master_pdf",
        protected_dir=root / "pdf" / "protected_individual_pdfs",
        sharepoint_dir=sharepoint_dir,
    )