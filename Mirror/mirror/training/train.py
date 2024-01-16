import logging
import string
import uuid

import numpy as np
import pandas as pd
import random as rand
import pymongo

from mirror.model.keys import Keys
from mirror.model.mouse import Mouse
from mirror.model.screen import Screen

keys = Keys()
mouse = Mouse()
screen = Screen()

client = pymongo.MongoClient('mongodb+srv://')
db = client.Mirror
collection = db.training


class Train:
    def __init__(self):
        self.keyboard_visits = None
        self.mouse_right_visits = None
        self.mouse_left_visits = None
        self.screen_visits = None
        self.model = None

        # Predictions
        self.keyboard_predictions = []
        self.mouse_right_predictions = []
        self.mouse_left_predictions = []
        self.screen_predictions = []

        self.log = logging.getLogger("mirror.training.train.Train")
        logging.basicConfig(level=logging.DEBUG, format="Train: %(message)s, %(levelname)s")

    def train(self, size, action, sample_data: pd.DataFrame = None):
        """
        Trains the model with random data or sample data

        :param size: size of the data
        :param action: action to train
        :param sample_data: sample data to train with
        """

        df = pd.DataFrame()

        if action == "keyboard":
            if sample_data:
                self.keyboard_visits = [sample_data["Key"][i] for i in range(len(sample_data["Key"]))]
                keys.use_data(training_data=sample_data)
            else:
                df["Time"] = np.random.randint(0, 5, size)
                df["Key"] = np.random.choice(
                    ["enter", "space", "shift", "ctrl", "alt", "tab",
                     "backspace", "esc", *list(string.ascii_lowercase)], size)
                self.keyboard_visits = [df["Key"][i] for i in range(len(df["Key"]))]
                keys.use_data(training_data=df)

        elif action == "mouse-left":
            x_y_list = [(rand.randint(0, 1920), rand.randint(0, 1080)) for _ in range(size)]

            if sample_data:
                self.mouse_left_visits = [sample_data["Coordinates"][i] for i in range(len(sample_data["Coordinates"]))]
                mouse.use_left_data(training_data=sample_data)
            else:
                df["Time"] = np.random.randint(0, 5, size)
                df["Action"] = np.random.choice(["left"], size)
                df["Coordinates"] = x_y_list
                df["Status"] = np.random.choice(["pending"], size)
                self.mouse_left_visits = [df["Coordinates"][i] for i in range(len(df["Coordinates"]))]
                mouse.use_left_data(training_data=df)

        elif action == "mouse-right":
            x_y_list = [(rand.randint(0, 1920), rand.randint(0, 1080)) for _ in range(size)]

            if sample_data:
                self.mouse_right_visits = [sample_data["Coordinates"][i] for i in range(len(sample_data["Coordinates"]))]
                mouse.use_right_data(training_data=sample_data)
            else:
                df["Time"] = np.random.randint(0, 5, size)
                df["Action"] = np.random.choice(["right"], size)
                df["Coordinates"] = x_y_list
                df["Status"] = np.random.choice(["pending"], size)
                self.mouse_right_visits = [df["Coordinates"][i] for i in range(len(df["Coordinates"]))]
                mouse.use_right_data(training_data=df)

        elif action == "screen":
            x_y_list = [(rand.randint(0, 1920), rand.randint(0, 1080)) for _ in range(size)]

            if sample_data:
                self.screen_visits = [sample_data["Coordinates"][i] for i in range(len(sample_data["Coordinates"]))]
                screen.use_data(training_data=sample_data)
            else:
                df["Time"] = np.random.randint(0, 5, size)
                df["Coordinates"] = x_y_list
                self.screen_visits = [df["Coordinates"][i] for i in range(len(df["Coordinates"]))]
                screen.use_data(training_data=df)

    def predictions(self, df: pd.DataFrame, action):
        """
        Compares data to the visited actions

        :param df: data to compare
        :param action: action to compare
        :return: prediction
        """

        if action == "keyboard":
            [self.keyboard_predictions.append((df["Time"][i], df["Key"][i]))
             for i in range(len(df["Key"])) if df["Key"][i] in self.keyboard_visits]

            if self.keyboard_predictions:
                self.log.info("What the keyboard predictions would look like: {}".format(self.keyboard_predictions))
                keys.use_data(training_data=df)
                return self.keyboard_predictions

        elif action == "mouse-left":
            [self.mouse_left_predictions.append((df["Time"][i], df["Coordinates"][i]))
             for i in range(len(df["Coordinates"])) if df["Coordinates"][i] in self.mouse_left_visits]

            if self.mouse_left_predictions:
                self.log.info("What the mouse left predictions would look like: {}".format(self.mouse_left_predictions))
                mouse.use_left_data(training_data=df)
                return self.mouse_left_predictions


        elif action == "mouse-right":
            [self.mouse_right_predictions.append((df["Time"][i], df["Coordinates"][i]))
             for i in range(len(df["Coordinates"])) if df["Coordinates"][i] in self.mouse_right_visits]

            if self.mouse_right_predictions:
                self.log.info(
                    "What the mouse right predictions would look like: {}".format(self.mouse_right_predictions))
                mouse.use_right_data(training_data=df)
                return self.mouse_right_predictions

        elif action == "screen":
            [self.screen_predictions.append((df["Time"][i], df["Coordinates"][i]))
             for i in range(len(df["Coordinates"])) if df["Coordinates"][i] in self.screen_visits]

            if self.screen_predictions:
                self.log.info("What the screen predictions would look like: {}".format(self.screen_predictions))
                screen.use_data(training_data=df)
                return self.screen_predictions

    def save_model(self, model_list, action):
        """
        Saves the model to the database
        :param model_list: model list to save
        :param action: action to save
        """
        model = pd.DataFrame(model_list).to_dict()

        if action == "keyboard":
            collection.insert_one({"id": uuid.uuid4(), "keyboard": model})

        elif action == "mouse-left":
            collection.insert_one({"id": uuid.uuid4(), "mouse-left": model})

        elif action == "mouse-right":
            collection.insert_one({"id": uuid.uuid4(), "mouse-right": model})

        elif action == "screen":
            collection.insert_one({"id": uuid.uuid4(), "screen": model})

    def load_model(self, model_id, action):
        """
        Loads the model from the database
        :param model_id: model id to load
        :param action: action to load
        :return: model
        """
        if action == "keyboard":
            try:
                self.model = collection.find_one({"id": model_id})["keyboard"]
            finally:
                return collection.find_one({"id": model_id})["keyboard"]

        elif action == "mouse-left":
            try:
                self.model = collection.find_one({"id": model_id})["mouse-left"]
            finally:
                return collection.find_one({"id": model_id})["mouse-left"]

        elif action == "mouse-right":
            try:
                self.model = collection.find_one({"id": model_id})["mouse-right"]
            finally:
                return collection.find_one({"id": model_id})["mouse-right"]

        elif action == "screen":
            try:
                self.model = collection.find_one({"id": model_id})["screen"]
            finally:
                return collection.find_one({"id": model_id})["screen"]


e = ["eee", *list(string.ascii_lowercase)]
print(e)
