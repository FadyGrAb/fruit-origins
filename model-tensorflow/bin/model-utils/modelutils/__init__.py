import pathlib
import sys

import click
import pytest

from .scripts import Clearer, Promoter
from .scripts.utils import get_project_dir


@click.group()
def cli():
    pass


@cli.command()
@click.argument("project_path", default=pathlib.Path(), type=click.Path(exists=True))
def init(project_path: pathlib.Path):
    config_file = project_path / ".modelutils"
    if config_file.exists():
        print("Project already initiated.")
        sys.exit(1)
    else:
        with config_file.open(mode="w") as f:
            f.write(" ")


@cli.command()
@click.argument("model_path", type=click.Path(exists=True))
def promote(model_path):
    model_path = pathlib.Path(model_path)
    if model_path.exists():
        # TODO: promote script
        Promoter.promote(model_path)
        pass
    else:
        print("File does not exists.")
        sys.exit(1)


@cli.command()
def clear_promoted():
    Clearer.clear_promoted()


@cli.command()
def promoted_exists():
    project_path = get_project_dir()
    promoted_path = project_path / "promoted-model"
    promoted_models = list(promoted_path.iterdir())
    if len(promoted_models) == 1:
        print(f"Found one promoted model: {promoted_models[0].name}")
    elif len(promoted_models) > 1:
        print("WARNING: Multiple promoted model found:")
        for model in promoted_models:
            print(model.name)
    else:
        print("No promoted models.")


@cli.command()
def train():
    # TODO add training script
    pass


@cli.command()
def test():
    pytest.main(pathlib.Path(__file__).parent / "scripts/tests/")


if __name__ == "__main__":
    cli()
