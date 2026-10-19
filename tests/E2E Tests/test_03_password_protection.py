from docx import Document
from pypdf import PdfReader
from helpers import get_pan_from_docx


def test_protected_pdfs_unlock_with_pan(run):
    """This tests opens docx and access PAN number as password and again opens password
    protected PDF with same name as docx and tries to unlock with the accessed PAN 
    number."""

    docx_files = [p for p in run.docx_dir.glob("*.docx") if not p.name.startswith("~$")]

    assert docx_files, "No docx files found"

    problems = []

    for docx_file in docx_files:
        pan = get_pan_from_docx(docx_file)
        if pan is None:
            problems.append(f"{docx_file.name}: no PAN value found")
            continue

        pdf_file = run.protected_dir / f"{docx_file.stem}.pdf"
        if not pdf_file.is_file():
            problems.append(f"{pdf_file.name}: protected PDF missing")
            continue

        reader = PdfReader(pdf_file)
        if not reader.is_encrypted:
            problems.append(f"{pdf_file.name}: PDF is not password protected")
        elif reader.decrypt(pan) == 0:
            problems.append(f"{pdf_file.name}: could not unlock with PAN '{pan}'")

    assert problems == [], "\n".join(problems)