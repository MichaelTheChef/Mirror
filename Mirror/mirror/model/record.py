import logging
import os
import threading

import pandas as pd
from typing import Optional
import uuid
import pymongo

from mirror.model.keys import Keys
from mirror.model.mouse import Mouse
from mirror.model.screen import Screen

client = pymongo.MongoClient('mongodb+srv://')
db = client.Mirror
collection = db.records


class Record:

    def __init__(self, seconds: int, training_data: Optional[pd.DataFrame] = None):
        self.log = logging.getLogger("mirror.model.record.Record")
        logging.basicConfig(level=logging.DEBUG, format="Record: %(message)s, %(levelname)s")

        self.seconds = seconds
        self.training_data = training_data
        self.recorded_data = pd.DataFrame()

    def record(self, keyboard: bool, mouse: bool, screen: bool):
        keyboard_thread = threading.Thread(target=Keys, args=(self.seconds,))
        mouse_thread = threading.Thread(target=Mouse, args=(self.seconds,))
        screen_thread = threading.Thread(target=Screen, args=(self.seconds,))

        if keyboard:
            keyboard_thread.start()

        if mouse:
            mouse_thread.start()

        if screen:
            screen_thread.start()

    def save_data(self, df: pd.DataFrame, to_csv=False) -> str:
        file_id = str(uuid.uuid4())

        if to_csv:
            df.to_csv(f"{file_id}.csv")
        else:
            data_to_save = {"id": file_id, "data": df.to_dict()}
            collection.insert_one(data_to_save)

        return file_id

    def use_data(self, action: str):
        if action == "keyboard":
            keyboard_thread = threading.Thread(target=Keys.use_data, args=(self.training_data,))
            keyboard_thread.start()

        elif action == "mouse-left":
            mouse_thread = threading.Thread(target=Mouse.use_left_data, args=(self.training_data,))
            mouse_thread.start()

        elif action == "mouse-right":
            mouse_thread = threading.Thread(target=Mouse.use_right_data, args=(self.training_data,))
            mouse_thread.start()

        elif action == "screen":
            screen_thread = threading.Thread(target=Screen.use_data, args=(self.training_data,))
            screen_thread.start()

    def read_data(self, data: Optional[pd.DataFrame], path: Optional[str], file_id: Optional[str]):
        if path and file_id:
            try:
                self.training_data = pd.read_csv(os.path.join(path, file_id)) # Include the file id and extension
            finally:
                self.log.info("Data: {}".format(self.training_data.head()))

            self.training_data = pd.DataFrame(data)
        else:
            self.training_data = pd.DataFrame(data)



