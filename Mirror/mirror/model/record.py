import logging
import os

import pandas as pd
import uuid
import pymongo

client = pymongo.MongoClient('mongodb+srv://')
db = client.Mirror
collection = db.records


class Record:

    def __init__(self, seconds=0, training_data: pd.DataFrame = None):
        self.log = logging.getLogger("mirror.model.record.Record")
        logging.basicConfig(level=logging.DEBUG, format="Record: %(message)s, %(levelname)s")

        self.seconds = seconds
        self.training_data = training_data
        self.recorded_data = pd.DataFrame()

    def save_data(self, df: pd.DataFrame, to_csv=False) -> str:
        file_id = str(uuid.uuid4())

        if to_csv:
            df.to_csv(f"{file_id}.csv")
        else:
            data_to_save = {"id": file_id, "data": df.to_dict()}
            collection.insert_one(data_to_save)

        return file_id

    def read_data(self, data: pd.DataFrame = None, path=None, file_id=None):
        if path and file_id:
            try:
                # Include the file id and extension
                self.training_data = pd.read_csv(os.path.join(path, file_id))
            finally:
                self.log.info("Data: {}".format(self.training_data.head()))

            self.training_data = pd.DataFrame(data)
        elif data:
            self.training_data = pd.DataFrame(data)

        else:
            self.log.error("No data was found to read")
