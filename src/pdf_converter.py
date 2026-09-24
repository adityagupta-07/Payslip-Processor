import pymupdf, subprocess
from .directories import PathConfig
from pathlib import Path

def get_docx_files(docx_dir: Path) -> list[Path]:
    return [
        path
        for path in docx_dir.iterdir()
        if path.suffix.lower() == ".docx"
        and not path.name.startswith("~$")
    ]


def build_libreoffice_command(
    docx_files: list[Path],
    output_dir: Path,
) -> list[str]:
    return [
        "libreoffice",
        "-env:UserInstallation=file:///tmp/lo_profile",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir),
        *[str(path) for path in docx_files],
    ]


def convert_docx_files(
    docx_files: list[Path],
    output_dir: Path,
) -> subprocess.CompletedProcess[str]:
    command = build_libreoffice_command(docx_files, output_dir)

    return subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )


def batch_convert_docx_to_pdf2(paths: PathConfig) -> None:
    docx_dir = Path(paths.output_docs_folder_path)
    output_dir = Path(paths.individual_pdfs_folder_path)

    docx_files = get_docx_files(docx_dir)

    if not docx_files:
        return

    try:
        convert_docx_files(docx_files, output_dir)
        print(f"Successfully converted {len(docx_files)} files.")
    except subprocess.CalledProcessError as e:
        print(f"Batch conversion failed. Error: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_pdf_files(pdf_folder: Path) -> list[Path]:
    return [
        pdf
        for pdf in pdf_folder.iterdir()
        if pdf.suffix.lower() == ".pdf"
    ]


def create_master_pdf() -> pymupdf.Document:
    return pymupdf.open()


def append_pdf(
    master_pdf: pymupdf.Document,
    pdf_path: Path,
) -> None:
    with pymupdf.open(pdf_path) as pdf:
        master_pdf.insert_pdf(pdf)


def create_master_pdf_path(
    master_pdf_folder: Path,
    month: str,
    year: int,
) -> Path:
    return master_pdf_folder / f"Payslip - {month} {year}.pdf"


def save_master_pdf(
    master_pdf: pymupdf.Document,
    output_path: Path,
) -> None:
    master_pdf.save(output_path)


def master_pdf_creation(
    paths: PathConfig,
    month: str,
    year: int,
) -> None:
    individual_pdfs_folder = Path(paths.individual_pdfs_folder_path)
    master_pdf_folder = Path(paths.master_pdf_folder_path)

    pdf_files = get_pdf_files(individual_pdfs_folder)
    master_pdf = create_master_pdf()

    for pdf_path in pdf_files:
        append_pdf(master_pdf, pdf_path)

    output_path = create_master_pdf_path(master_pdf_folder, month, year)

    save_master_pdf(master_pdf, output_path)
    master_pdf.close()