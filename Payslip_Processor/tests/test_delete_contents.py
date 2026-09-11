from src.delete_contents import delete_contents, check_dir
from src.directories import PathConfig
import pytest
from pathlib import Path

def test_directory_is_empty():
    delete_contents()
    result = check_dir()
    
    assert result == set()

