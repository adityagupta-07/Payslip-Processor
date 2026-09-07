from pathlib import Path
from src.payslip_processor import PathConfig

def delete_contents(dir: PathConfig):
    root_dir = Path(dir.get_output_folder_path)

    for file_path in root_dir.glob("**/*"):
        if file_path.is_file():
            file_path.unlink()
    return