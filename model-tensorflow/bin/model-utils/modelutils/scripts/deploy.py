import json
import subprocess
import os
import sys
import pathlib

import boto3

from .utils import get_project_dir, cprint


class Deployer:
    def __init__(self, production: bool) -> None:
        # Setup directories.
        self.production = production
        self.project_path = get_project_dir()
        self.promoted_path = self.project_path / "promoted-model"
        if production:
            self.deployment_path = self.project_path / "converted-model"
            if not self.deployment_path.exists():
                self.deployment_path.mkdir(exist_ok=True)
        else:
            self.deployment_path = self.project_path.parent / "frontend-js/public/model"
        self.assets_path = self.project_path.parent / "frontend-js/src/assets"
        self.files_in_promoted = list(self.promoted_path.iterdir())

    def __convert_model(self) -> pathlib.Path:
        if len(self.files_in_promoted) == 1:
            model = self.files_in_promoted[0]
            # Delete old model from production
            for old_model in self.deployment_path.iterdir():
                old_model.unlink()
            # Convert model to tfjs model.
            subprocess.run(
                f"tensorflowjs_converter --input_format=keras --output_format=tfjs_graph_model\
                {str(model)} \
                {str(self.deployment_path) }/",
                shell=True,
            )
            cprint(f"[deployment] model:{model.name} is converted and deployed.", color="green", bright=True)
            return model
        else:
            cprint(
                "[deployment] Can not deploy. There isn't any promoted models or there are more than one promoted models.",
                color="red",
                bright=True
            )
            sys.exit(1)

    def __get_classes_names(self, model: pathlib.Path) -> pathlib.Path:
        # Get and copy the class_names
        models_json = self.project_path / "models/models.json"
        if models_json.exists():
            with models_json.open("r") as j:
                data = json.load(j).get(model.name, None)
                classes = data.get("class_names", None)
            if classes:
                target_path = self.deployment_path if self.production else self.assets_path
                with (target_path / "classNames.json").open("w") as j:
                    json.dump({"classNames": classes}, j)
                cprint(f"[deployment] Class names are exported in {str(target_path)}", color="green", bright=True)
                return target_path
            else:
                cprint(f"[deployment] ERROR: classes for model {model.name} can't be found in models.json.", color="red", bright=True)
                sys.exit(1)
        else:
            cprint(f"[deployment] ERROR: Can't locate models.json in {models_json.parent}.", color="red", bright=True)
            sys.exit(1)  

    def __upload_to_s3(self, source_path: pathlib.Path):
        destination_bucket = os.getenv("MODEL_BUCKET")
        cprint(f"[deployment] Initiating upload from {str(source_path)} to {destination_bucket}", color="blue", bright=True)
        s3 = boto3.resource("s3")
        if destination_bucket:
            for file in source_path.iterdir():
                with file.open("rb") as f:
                    s3.Bucket(destination_bucket).put_object(Key=file.name, Body=f)
                    cprint(f"[deployment] {file.name} is uploaded.", color="blue", bright=True)
            cprint(f"[deployment] Model is successfully uploaded", color="green", bright=True)
        else:
            cprint(f"[deployment] ERROR: MODEL_BUCKET is not set.", color="red", bright=True)

    def deploy(self):
        model = self.__convert_model()
        source_path = self.__get_classes_names(model)
        if self.production:
            self.__upload_to_s3(source_path)

        
            
        

