import logging
import threading

import pyautogui
from typing import Optional
import time

import pandas as pd


class Screen:

    def __init__(self, seconds: int):
        self.seconds = seconds
        self.recorded_data = []
        self.df = None
        self.start_time = None
        self.running = True

        self.log = logging.getLogger("mirror.model.screen.Screen")
        logging.basicConfig(level=logging.INFO, format="%(message)s, Level: %(levelname)s")

        timer_thread = threading.Thread(target=self.async_sleep, args=(seconds,))
        timer_thread.start()
        self.monitor_screen()



    def read_data(self, amount: int):
        self.df = pd.DataFrame(self.recorded_data, columns=["Time", "Coordinates"])
        return self.df.head(amount if amount < len(self.df) else len(self.df))

    def use_data(self, training_data: Optional[pd.DataFrame] = False):
        i = 0

        if training_data:
            while not training_data.empty:
                pyautogui.moveTo(training_data["Coordinates"][i])
                time.sleep(training_data["Time"][i])
                training_data.drop(i)
                self.log.info(training_data.head(i))

                if i >= len(training_data):
                    break
                else:
                    i += 1

        while not self.df.empty:
            pyautogui.moveTo(self.df["Coordinates"][i])
            time.sleep(self.df["Time"][i])
            self.df.drop(i)
            self.log.info(self.df.head(i))
            i += 1


    def monitor_screen(self):
        current_position = pyautogui.position()
        current_time = time.time()

        while self.running:
            if current_position == pyautogui.position():
                pass
            else:
                x, y = pyautogui.position()

                self.recorded_data.append((time.time() - current_time, (x, y)))
                current_time = time.time()
                current_position = pyautogui.position()
                self.log.info(self.recorded_data)
                self.log.info("Mouse moved to: {}".format(pyautogui.position()))



    def async_sleep(self, seconds: int):

        if seconds > 0:
            time.sleep(seconds)
            self.running = False
            self.log.info("Screen Recording: Finished timer with recorded data: {}".format(self.recorded_data))
            self.log.info(f"Read data: {self.read_data(900)}")
            self.use_data()

        else:
            self.log.info("Screen Recording: Finished timer with recorded data: {}".format(self.recorded_data))
            self.log.info(f"Read data: {self.read_data(900)}")
            self.use_data()







