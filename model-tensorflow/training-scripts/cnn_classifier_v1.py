import pathlib
import tensorflow as tf
import numpy as np
import datetime
import textwrap

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Sequential


class Trainer:
    def __init__(self, **kwargs):
        print("Running CNN classifier v1")
        self.project_path = pathlib.Path(__file__).parents[1]
        train_ds_path = self.project_path / "data/train"
        self.BATCH_SIZE = kwargs.get("batch_size", 64)
        self.IMG_HEIGHT = kwargs.get("img_height", 100)
        self.IMG_WIDTH = kwargs.get("img_width", 100)
        self.EPOCHS = kwargs.get("epochs", 5)
        self.TAG = kwargs.get("tag", "")

        self.train_ds = tf.keras.utils.image_dataset_from_directory(
            train_ds_path,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
            batch_size=self.BATCH_SIZE,
        )
        self.val_ds = tf.keras.utils.image_dataset_from_directory(
            train_ds_path,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
            batch_size=self.BATCH_SIZE,
        )
        self.class_names = self.train_ds.class_names

        AUTOTUNE = tf.data.AUTOTUNE

        self.train_ds = (
            self.train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        )
        self.val_ds = self.val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    def __create_model(self):
        # tfjs has problems with the RandomFlip layer so I've excluded the
        # data augmentation all together.
        preprocess = keras.Sequential(
            [
                layers.RandomFlip(
                    "horizontal", input_shape=(self.IMG_HEIGHT, self.IMG_WIDTH, 3)
                ),
                layers.RandomRotation(0.1),
                layers.RandomZoom(0.1),
            ]
        )

        model = Sequential(
            [
                preprocess,
                layers.Rescaling(
                    1.0 / 255, input_shape=(self.IMG_HEIGHT, self.IMG_WIDTH, 3)
                ),
                layers.Conv2D(16, 3, padding="same", activation="relu"),
                layers.MaxPooling2D(),
                layers.Conv2D(32, 3, padding="same", activation="relu"),
                layers.MaxPooling2D(),
                layers.Conv2D(64, 3, padding="same", activation="relu"),
                layers.MaxPooling2D(),
                layers.Dropout(0.2),
                layers.Flatten(),
                layers.Dense(128, activation="relu"),
                layers.Dense(len(self.class_names)),
            ]
        )
        model.compile(
            optimizer="adam",
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=["accuracy"],
        )
        return model

    def run(self):
        model = self.__create_model()
        print(
            textwrap.dedent(
                f"""
        BATCH_SIZE: {self.BATCH_SIZE}
        IMG_Height: {self.IMG_HEIGHT}
        IMG_WIDTH: {self.IMG_WIDTH}
        EPOCHS: {self.EPOCHS}
        """
            )
        )
        model.fit(self.train_ds, validation_data=self.val_ds, epochs=self.EPOCHS)
        timestamp = int(datetime.datetime.now().timestamp())
        tag = f"-{self.TAG}" if self.TAG else ""
        model_name = f"fruit-model-{timestamp}{tag}.h5"
        model_path = self.project_path / f"models/{model_name}"
        model.save(model_path)
        print(f"Model saved: {str(model_path)}")
        return model_path, self.class_names
