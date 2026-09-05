from pathlib import Path

def delete_contents(dir):
    root_dir = Path(dir)

    for file_path in root_dir.glob("**/*"):
        if file_path.is_file() and file_path.suffix.lower() in (".docx", ".pdf"):
            file_path.unlink()
    return