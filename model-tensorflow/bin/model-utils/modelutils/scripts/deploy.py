import subprocess
import sys
from .utils import get_project_dir


class Deployer:
    def deploy():
        project_path = get_project_dir()
        promoted_path = project_path / "promoted-model"
        deployment_path = project_path.parent / "frontend-js/public/model"
        files_in_promoted = list(promoted_path.iterdir())
        if len(files_in_promoted) == 1:
            model = files_in_promoted[0]
            # Delete old model
            for old_model in deployment_path.iterdir():
                old_model.unlink()
            subprocess.run(
                f"tensorflowjs_converter --input_format=keras \
                {str(model)} \
                {str(deployment_path) }/",
                shell=True,
            )
        else:
            print(
                "Can not deploy. There isn't any promoted models or there are more than one promoted models."
            )
            sys.exit(1)
