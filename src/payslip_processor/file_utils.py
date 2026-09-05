import shutil
import os

def delete_contents(folder_paths):
    for folder_path in folder_paths:
        shutil.rmtree(folder_path)
        os.makedirs(folder_path, exist_ok=True)
    return