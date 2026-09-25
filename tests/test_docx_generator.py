from datetime import datetime
import pytest

from src import docx_generator
from src.config import Employee
from src.directories import PathConfig
from src.constants import ExcelConstants

excel_constants = ExcelConstants()


@pytest.fixture
def employee_with_id():
    employee = Employee()
    employee.set_atr(excel_constants.MONTH_YEAR, datetime(2024, 5, 1))
    employee.set_atr(excel_constants.EMPLOYEE_ID, "1")
    employee.set_atr(excel_constants.EMPLOYEE_NAME, "John Doe")
    return employee


@pytest.fixture
def employee_without_id():
    employee = Employee()
    employee.set_atr(excel_constants.MONTH_YEAR, datetime(2024, 5, 1))
    employee.set_atr(excel_constants.EMPLOYEE_ID, "")
    employee.set_atr(excel_constants.EMPLOYEE_NAME, "Jane Smith")
    return employee


@pytest.fixture
def path_config(tmp_path):
    config = PathConfig()
    # Point everything to a temporary test folder instead of the real /app path
    config.output_docs_folder_path = tmp_path
    config.template_id_path = tmp_path / "template_id.docx"
    config.template_no_id_path = tmp_path / "template_no_id.docx"
    return config


def test_get_month_name(employee_with_id):
    assert docx_generator.get_month_name(employee_with_id) == "May"


def test_get_year(employee_with_id):
    assert docx_generator.get_year(employee_with_id) == "2024"


def test_employee_has_id_true(employee_with_id):
    assert docx_generator.employee_has_id(employee_with_id) is True


def test_employee_has_id_false(employee_without_id):
    assert docx_generator.employee_has_id(employee_without_id) is False


def test_get_file_name_with_id(employee_with_id):
    file_name = docx_generator.get_file_name(employee_with_id, "May", "2024", True)
    assert file_name == "John_Doe_May_2024_1"


def test_get_file_name_without_id(employee_without_id):
    file_name = docx_generator.get_file_name(employee_without_id, "May", "2024", False)
    assert file_name == "Jane_Smith_May_2024"


def test_get_template_file_path_with_id(path_config):
    result = docx_generator.get_template_file_path(True, path_config)
    assert result == path_config.template_id_path


def test_get_template_file_path_without_id(path_config):
    result = docx_generator.get_template_file_path(False, path_config)
    assert result == path_config.template_no_id_path


def test_get_destination_file_path(path_config):
    result = docx_generator.get_destination_file_path(path_config, "John_Doe_May_2024")
    assert result == path_config.output_docs_folder_path / "John_Doe_May_2024.docx"

