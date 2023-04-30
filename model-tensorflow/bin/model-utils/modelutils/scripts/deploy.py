import subprocess
import sys

from .utils import get_project_dir


class Deployer:
    def deploy():
        project_path = get_project_dir()
        promoted_path = project_path / "promoted-model"
        files_in_promoted = list(promoted_path.iterdir())
        if len(files_in_promoted) == 1:
            model = files_in_promoted[0]
            subprocess.run(
                f"tensorflowjs_converter --input_format=keras \
                {str(model)} \
                {str(project_path.parent / f'frontend-js/model/{model.name}/')}",
                shell=True,
            )
        else:
            print(
                "Can not deploy. There isn't any promoted models or there are more than one promoted models."
            )
            sys.exit(1)
