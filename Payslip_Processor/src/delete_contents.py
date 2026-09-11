from pathlib import Path
from .directories import PathConfig

dir = PathConfig()
root_dir = Path(dir.get_output_folder_path)

def delete_contents():

    for file_path in root_dir.glob("**/*"):
        if file_path.is_file():
            file_path.unlink()
    return

def check_dir1():

    files = []
    for file_path in root_dir.glob("**/*"):
            if file_path.is_file():
                files.append(file_path)
    # print(f"found files: {files}")
    return files

def check_dir():

    non_empty_dir = set()
    for file in root_dir.rglob('*'):
        if file.is_file():
            non_empty_dir.add(str(file.parent)) 
    # print(non_empty_dir)
    return non_empty_dir