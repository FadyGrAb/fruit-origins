import json
import subprocess
import sys

from .utils import get_project_dir, cprint


class Deployer:
    def deploy():
        project_path = get_project_dir()
        promoted_path = project_path / "promoted-model"
        deployment_path = project_path.parent / "frontend-js/public/model"
        assets_path = project_path.parent / "frontend-js/src/assets"
        files_in_promoted = list(promoted_path.iterdir())
        if len(files_in_promoted) == 1:
            model = files_in_promoted[0]
            # Delete old model from production
            for old_model in deployment_path.iterdir():
                old_model.unlink()
            # Convert model to tfjs model.
            subprocess.run(
                f"tensorflowjs_converter --input_format=keras --output_format=tfjs_graph_model\
                {str(model)} \
                {str(deployment_path) }/",
                shell=True,
            )
            cprint(f"[deployment] model:{model.name} is converted and deployed.", color="green", bright=True)
            # Get and copy the class_names
            models_json = project_path / "models/models.json"
            if models_json.exists():
                with models_json.open("r") as j:
                    data = json.load(j).get(model.name, None)
                    classes = data.get("class_names", None)
                if classes:
                    with (assets_path / "classNames.json").open("w") as j:
                        json.dump({"classNames": classes}, j)
                    cprint(f"[deployment] Class names are exported in src/assets.", color="green", bright=True)
                else:
                    cprint("[deployment] WARNING: classes can't be found in models.json.", color="yellow", bright=True)
                    
        else:
            cprint(
                "[deployment] Can not deploy. There isn't any promoted models or there are more than one promoted models.",
                color="red",
                bright=True
            )
            sys.exit(1)
