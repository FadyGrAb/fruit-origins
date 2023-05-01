import pathlib
import sys

import tensorflow as tf

from .configs import test_configs
from ..utils import get_project_dir, cprint


def test_model_accuracy(model_path: pathlib.Path):
    acc_value = test_configs.get("acc_value", 95)
    cprint(f"Model Accuracy Test for {acc_value}%", color="blue", bright=True, header=True)
    cprint(f"Model {model_path.name}", color="blue", bright=True, header=True)
    acc_test_value = acc_value / 100
    model = tf.keras.models.load_model(model_path)
    test_data_path = get_project_dir() / "data/test"
    test_ds = tf.keras.utils.image_dataset_from_directory(
        test_data_path, image_size=(100, 100), batch_size=64
    )
    _, accuracy = model.evaluate(test_ds)
    test_pass = accuracy >= acc_test_value
    color = "green" if test_pass else "red"
    cprint(f"Model accuracy: {accuracy:.2%} - Threshold value: {acc_test_value:.2%}", color=color, bright=True)
    if not test_pass:
        sys.exit(1)
