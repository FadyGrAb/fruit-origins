import pathlib
import os
import sys


def get_project_dir() -> pathlib.Path:
    current_dir = pathlib.Path(os.getcwd())
    if (current_dir / ".modelutils").exists():
        return current_dir
    else:
        parents = current_dir.parents
        for idx in range(0, len(parents)):
            if (parents[idx] / ".modelutils").exists():
                return parents[idx]
    print("Project isn't initiated. Run 'model-utils init'.")
    sys.exit(1)
