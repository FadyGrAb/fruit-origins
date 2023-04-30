import pathlib
import tensorflow as tf
import numpy as np
import datetime

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Sequential

class Trainer:
    def __init__(self):
        print("Running CNN classifier v1")
        self.project_path = pathlib.Path(__file__).parents[1]
        train_ds_path = self.project_path / "data/train"
        self.BATH_SIZE = 64
        self.IMG_HEIGHT = 100
        self.IMG_WIDTH = 100

        self.train_ds = tf.keras.utils.image_dataset_from_directory(
            train_ds_path,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
            batch_size=self.BATH_SIZE
        )
        self.val_ds = tf.keras.utils.image_dataset_from_directory(
            train_ds_path,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
            batch_size=self.BATH_SIZE
        )
        self.num_classes = len(self.train_ds.class_names)

        AUTOTUNE = tf.data.AUTOTUNE

        self.train_ds = self.train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        self.val_ds = self.val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    def __create_model(self):
        preprocess = keras.Sequential(
            [
                layers.RandomFlip("horizontal", input_shape=(self.IMG_HEIGHT, self.IMG_WIDTH, 3)),
                layers.RandomRotation(0.1),
                layers.RandomZoom(0.1),
            ]
        )

        model = Sequential([
            preprocess,
            layers.Rescaling(1./255),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Dropout(0.2),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(self.num_classes),
            ])
        model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
        return model


    def run(self):
        model = self.__create_model()
        epochs = 5
        history = model.fit(
            self.train_ds,
            validation_data=self.val_ds,
            epochs=epochs
        )
        timestamp = int(datetime.datetime.now().timestamp())
        model_name = f"fruit-origins-model-{timestamp}.h5"
        model_path = self.project_path / f"models/{model_name}"
        model.save(model_path)
        print(f"Model saved: {str(model_path)}")