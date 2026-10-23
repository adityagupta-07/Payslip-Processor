from pathlib import Path

class PathConfig:
    def __init__(self, output_folder_path):

        base_dir = Path(__file__).resolve().parent
        
        # self.output_folder_path = Path("/app/Payslip_Processor")
        self.output_folder_path = Path(output_folder_path) / "Ultra Payslips"
        self.output_docs_folder_path = self.output_folder_path / "docx"
        self.output_pdfs_folder_path = self.output_folder_path / "pdf"
        self.individual_pdfs_folder_path = self.output_pdfs_folder_path / "individual_pdfs"
        self.master_pdf_folder_path = self.output_pdfs_folder_path / "master_pdf"
        self.protected_individual_pdf_folder_path = self.output_pdfs_folder_path / "protected_individual_pdfs"
        self.template_id_path = base_dir / "templates" / "docx" / "template_id.docx"
        self.template_no_id_path = base_dir / "templates" / "docx" / "template_no_id.docx"

    def create_output_dir(self):
        for folder in (
            self.output_folder_path,
            self.output_docs_folder_path,
            self.output_pdfs_folder_path,
            self.individual_pdfs_folder_path,
            self.master_pdf_folder_path,
            self.protected_individual_pdf_folder_path,
        ):
            folder.mkdir(parents=True, exist_ok=True)


def validate_output_folder(path: str) -> Path:
    """Validate and return a valid folder path."""

    cleaned_path = path.strip().replace('"', "")
    
    if not cleaned_path:
        raise ValueError("Folder path cannot be empty.")

    folder_path = Path(cleaned_path)

    if not folder_path.exists():
        raise FileNotFoundError("Folder does not exist.")

    if not folder_path.is_dir():
        raise NotADirectoryError(f"Path exists but not a folder.")

    return folder_path


def output_folder_by_user() -> Path:
    """Prompt the user until they provide a valid output folder to write files & folders."""

    while True:
        try:
            path = input("Provide output folder path: ")
            return validate_output_folder(path)
        except FileNotFoundError as error:
            print(f"Error: {error}")

def local_sharepoint_folder_by_user() -> Path:
    """Prompt the user until they provide a valid sharepoint local folder to write files."""

    while True:
        try:
            path = input("Provide local sharepoint folder to upload an employee's payslip: ")
            return validate_output_folder(path)
        except FileNotFoundError as error:
            print(f"Error: {error}")

