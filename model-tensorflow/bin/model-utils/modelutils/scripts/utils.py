import pathlib
import os
import sys
import shutil
import json
import datetime

from colorama import Fore, Style


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


def cprint(*args, color: str = "white", bright=False, header=False) -> None:
    color = Fore.__dict__.get(color.upper())
    color_control = color + Style.BRIGHT if bright else ""
    text = "".join(args)
    if header:
        terminal_columns = shutil.get_terminal_size().columns
        text = "\n" + text.center(terminal_columns, "_")
    print(color_control + text + Style.RESET_ALL)


def save_model_hyperparams(model_path: pathlib.Path, **kwargs):
    models_json = model_path.parent / "models.json"
    if models_json.exists():
        with models_json.open(mode="r") as j:
            data = json.load(j)
            kwargs["created"] = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
            data[model_path.name] = kwargs
        with models_json.open(mode="w") as j:
            json.dump(data, j, indent=2)
    else:
        with models_json.open(mode="w") as j:
            kwargs["created"] = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
            data = {model_path.name: kwargs}
            json.dump(data, j, indent=2)

def query_model_hyperparams(model_path: pathlib.Path):
    model_path = pathlib.Path(model_path)
    models_json = model_path.parent / "models.json"
    if models_json.exists():
        with models_json.open(mode="r") as j:
            data = json.load(j)
        model_data = data.get(model_path.name, None)
        if model_data:
            for param, value in model_data.items():
                print(f"{param}: {value}")
        else:
            print("No data were found for this model in models.json")
    else:
        print("Can not find models.json")