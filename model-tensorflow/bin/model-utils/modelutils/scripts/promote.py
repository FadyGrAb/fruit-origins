import os
import pathlib
import shutil
import sys

from .utils import get_project_dir


class Promoter:
    def __move_to_promoted_model(model_path: pathlib.Path) -> None:
        # TODO: model file integrity test.
        project_path = get_project_dir()
        promoted_dir = project_path / "promoted-model"
        if len(list(promoted_dir.iterdir())) == 0:
            shutil.copy(model_path, promoted_dir)
        else:
            print("'promoted-model' directory isn't empty")
            sys.exit(1)

    def promote(model_path):
        Promoter.__move_to_promoted_model(model_path)
