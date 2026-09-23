from pathlib import Path

class PathConfig():

    def __init__(self):

        base_dir = Path(__file__).resolve().parent

        self.output_folder_path = Path("/app/Payslip_Processor")
        # self.output_folder_path = Path("/home/aditya/wow man")
        self.output_docs_folder_path = Path(f"{self.output_folder_path}/docx")
        self.output_pdfs_folder_path = Path(f"{self.output_folder_path}/pdf")
        self.individual_pdfs_folder_path = Path(f"{self.output_pdfs_folder_path}/individual_pdfs")
        self.master_pdf_folder_path = Path(f"{self.output_pdfs_folder_path}/master_pdf")
        self.protected_individual_pdf_folder_path = Path(f"{self.output_pdfs_folder_path}/protected_individual_pdfs")
        self.template_id_path = base_dir / "templates" / "docx" / "template_id.docx"
        self.template_no_id_path = base_dir / "templates" / "docx" / "template_no_id.docx"

    def create_output_dir(self):
        self.output_folder_path.mkdir(parents=True, exist_ok=True)
        self.output_docs_folder_path.mkdir(parents=True, exist_ok=True)
        self.output_pdfs_folder_path.mkdir(parents=True, exist_ok=True)
        self.individual_pdfs_folder_path.mkdir(parents=True, exist_ok=True)
        self.master_pdf_folder_path.mkdir(parents=True, exist_ok=True)
        self.protected_individual_pdf_folder_path.mkdir(parents=True, exist_ok=True)


