import os
import pathlib
import sys

from .utils import get_project_dir


class Clearer:
    def __clear_promoted_model():
        project_path = get_project_dir()
        promoted_dir = project_path / "promoted-model"
        for file in promoted_dir.iterdir():
            file.unlink()

    def __clear_test_model():
        project_path = get_project_dir()
        test_dir = project_path / "model-tests/model"
        for file in test_dir.iterdir():
            file.unlink()

    def clear_promoted():
        Clearer.__clear_promoted_model()
        Clearer.__clear_test_model()
