import pytest
import pathlib
from ..utils import get_project_dir


@pytest.fixture
def model_path():
    project_path = get_project_dir()
    model_dir = project_path / "promoted-model"
    files_in_dir = list(model_dir.iterdir())
    if len(files_in_dir) != 1:
        raise Exception(
            "There is more that one model or the 'model' directory (for test) is empty."
        )
    return list(model_dir.iterdir())[0]
