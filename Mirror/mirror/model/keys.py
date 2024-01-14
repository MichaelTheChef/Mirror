import logging
from typing import Optional

import keyboard
import asyncio
import time

import pandas as pd


class Keys:

    def __init__(self, seconds: int):
        self.seconds = seconds
        self.recorded_data = []
        self.df = None
        self.start_time = None

        self.log = logging.getLogger("mirror.model.keys.Key")
        logging.basicConfig(level=logging.INFO, format="%(message)s, Level: %(levelname)s")

        # Start listening for key presses
        keyboard.on_press(self.monitor_keyboard)
        asyncio.run(self.async_sleep(seconds))
        keyboard.wait()

    def read_data(self, amount: int):
        self.df = pd.DataFrame(self.recorded_data, columns=["Time", "Key"])
        return self.df.head(amount if amount < len(self.df) else len(self.df))

    def use_data(self, training_data: Optional[pd.DataFrame] = False):
        i = 0

        if training_data:
            while not training_data.empty:
                keyboard.press(training_data["Key"][i])
                time.sleep(training_data["Time"][i])
                keyboard.release(training_data["Key"][i])
                training_data.drop(i)
                self.log.info(training_data.head(i))

                if i >= len(training_data):
                    break
                else:
                    i += 1

        while not self.df.empty:

            keyboard.press(self.df["Key"][i])
            time.sleep(self.df["Time"][i])
            keyboard.release(self.df["Key"][i])
            self.df.drop(i)
            self.log.info(self.df.head(i))
            i += 1


    def monitor_keyboard(self, event):
        self.log.info("Key pressed: {}".format(event.name))

        # Start timer for the first key press
        if self.start_time is None:
            self.start_time = time.time()
            self.recorded_data.append((0, event.name))

        # End timer and add tuple for subsequent key presses
        else:
            time_elapsed = time.time() - self.start_time
            self.recorded_data.append((time_elapsed, event.name))
            self.start_time = time.time()

        print(self.recorded_data)


    async def async_sleep(self, seconds: int):
        if seconds > 0:
            await asyncio.sleep(seconds)
            keyboard.unhook_all()
            self.log.info("Keyboard Recording: Finished timer with recorded data: {}".format(self.recorded_data))
            self.log.info(f"Read data: {self.read_data(900)}")
            self.use_data()
        else:
            self.log.info("Keyboard Recording: Finished timer with recorded data: {}".format(self.recorded_data))
            self.log.info(f"Read data: {self.read_data(900)}")
            self.use_data()


Keys(5)





