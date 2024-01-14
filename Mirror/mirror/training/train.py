import logging

import numpy as np
import pandas as pd

class Train:
    def __init__(self):
        self.training_data = None
        self.log = logging.getLogger("mirror.training.train.Train")
        logging.basicConfig(level=logging.DEBUG, format="Train: %(message)s, %(levelname)s")

    def train(self, action: str):
        mouse_df = pd.DataFrame()

    def test(self):
        pass

    def save_model(self):
        pass

    def load_model(self):
        pass