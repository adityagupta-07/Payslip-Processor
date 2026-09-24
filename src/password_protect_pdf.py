from pathlib import Path
import pdfplumber
from pypdf import PdfReader, PdfWriter
from .directories import PathConfig

def get_payslip_paths(folder_path: str | Path) -> list[Path]:
    """Return all files in the payslip folder."""
    folder = Path(folder_path)
    return [item for item in folder.iterdir() if item.is_file()]


def extract_pan_from_pdf(pdf_path: Path) -> str | None:
    """Extract the value immediately after 'PAN' in a PDF table."""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()

            if table:
                password = extract_pan_from_table(table)
                if password:
                    return password

    return None


def extract_pan_from_table(table: list[list[str | None]]) -> str | None:
    """Find PAN in a table and return the next non-empty cell in its row."""
    for row in table:
        for index, cell in enumerate(row):
            if cell and cell.upper() == "PAN":
                return get_next_non_empty_value(row, index + 1)

    return None


def get_next_non_empty_value(
    row: list[str | None], 
    start_index: int,
) -> str | None:
    """Return the first non-empty value after start_index."""
    for cell in row[start_index:]:
        if cell:
            return cell

    return None


def protect_pdf(
    input_path: Path, output_path: Path, password: str
) -> None:
    """Create a password-protected copy of a PDF."""
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with output_path.open("wb") as output_file:
        writer.write(output_file)


def password_protect_pdfs(paths: PathConfig) -> None:
    """Password-protect all payslip PDFs using their PAN."""
    input_folder = Path(paths.individual_pdfs_folder_path)
    output_folder = Path(paths.protected_individual_pdf_folder_path)

    payslip_paths = get_payslip_paths(input_folder)

    for payslip_path in payslip_paths:
        password = extract_pan_from_pdf(payslip_path)

        if not password:
            continue

        output_path = output_folder / payslip_path.name

        protect_pdf(
            input_path=payslip_path,
            output_path=output_path,
            password=password,
        )