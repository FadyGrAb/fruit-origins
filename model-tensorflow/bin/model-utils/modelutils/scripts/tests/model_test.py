import pathlib
import tensorflow as tf
from ..utils import get_project_dir


def test_model_accuracy(model_path: pathlib.Path):
    model = tf.keras.models.load_model(model_path)
    test_data_path = get_project_dir() / "data/test"
    test_ds = tf.keras.utils.image_dataset_from_directory(
        test_data_path, image_size=(100, 100), batch_size=64
    )
    _, accuracy = model.evaluate(test_ds)
    assert accuracy >= 0.95
