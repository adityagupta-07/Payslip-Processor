from pathlib import Path

def delete_contents(dir):
    root_dir = Path(dir)

    for file_path in root_dir.glob("**/*"):
        if file_path.is_file():
            file_path.unlink()
    return