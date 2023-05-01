import pathlib
import json
import sys
import re
import importlib

import click
import pytest

from .scripts import Clearer, Deployer, Promoter
from .scripts.utils import get_project_dir, save_model_hyperparams, query_model_hyperparams
from .scripts.tests.configs import test_configs


@click.group()
def cli():
    """Model utilities to automate common model related tasks."""
    pass


@cli.command()
@click.argument("project_path", default=pathlib.Path(), type=click.Path(exists=True))
def init(project_path: pathlib.Path):
    """Must run in the modelling project's root."""
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
    """Promote a created model. Promoted model will be deployed if it passes the tests."""
    model_path = pathlib.Path(model_path)
    if model_path.exists():
        # TODO: promote script
        Promoter.promote(model_path)
        pass
    else:
        print("File does not exists.")
        sys.exit(1)


@cli.command()
def clear():
    """Delete the promoted model."""
    Clearer.clear_promoted()


@cli.command()
def exists():
    """Check if there is a promoted model."""
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
@click.argument("training_script", type=click.Path(exists=True))
@click.option("-b", "--batch-size", default=64, show_default=True, help="Training batch size.")
@click.option("-h", "--img-height", default=100, show_default=True, help="Images resized height.")
@click.option("-w", "--img-width", default=100, show_default=True, help="Images resized width.")
@click.option("-e", "--epochs", default=5, show_default=True, help="Number of training epochs.")
def train(training_script: pathlib.Path, **kwargs):
    """Train a model using a training script."""
    training_script = pathlib.Path(training_script)
    sys.path.append(str(training_script.parent))
    module_name = re.sub(r"\.py$", "", training_script.name)
    module = importlib.import_module(module_name)
    trainer = module.Trainer(**kwargs)
    model_path = trainer.run()
    save_model_hyperparams(model_path, training_script=str(training_script), **kwargs)


@cli.command()
@click.option("-a", "--acc-value", default=95, show_default=True, help="Model accuracy threshold. ex 95.")
def test(acc_value):
    """Run model tests."""
    test_configs["acc_value"] = acc_value
    opts = ["-v", "-s", "-p", "no:warnings"]
    tests_dir = pathlib.Path(__file__).parent / "scripts/tests/"
    sys.exit(pytest.main(opts + [str(tests_dir)]))


@cli.command()
def deploy():
    """Deploy the promoted model."""
    Deployer.deploy()

@cli.command()
@click.argument("model_path", type=click.Path(exists=True))
def info(model_path: pathlib.Path):
    """Get model hyperparameter info."""
    query_model_hyperparams(model_path)



if __name__ == "__main__":
    cli()
