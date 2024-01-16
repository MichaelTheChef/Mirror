import logging
import threading
import pyautogui
from pynput.mouse import Button, Controller, Listener
import time
import pandas as pd

mouse = Controller()


class Mouse:

    def __init__(self, seconds=0):
        self.last_left_click_time = 0.0
        self.last_right_click_time = 0.0
        self.right_clicks = []
        self.left_clicks = []
        self.invalid_click_left_removed = False
        self.invalid_click_right_removed = False

        self.seconds = seconds
        self.recorded_data = []
        self.left_df = None
        self.right_df = None
        self.running = True
        self.listener = None

        # Configure logging
        self.log = logging.getLogger("mirror.model.mouse.Mouse")
        logging.basicConfig(level=logging.INFO, format="%(message)s, Level: %(levelname)s")

        # Start timer
        timer_thread = threading.Thread(target=self.thread_sleep)
        timer_thread.start()

        if self.seconds > 0:
            # Start listening for mouse clicks (without blocking)
            with Listener(on_click=self.monitor_mouse) as listener:
                self.listener = listener
                listener.join()

            time.sleep(seconds)

    def read_data(self):
        self.left_df = pd.DataFrame(self.left_clicks, columns=["Time", "Action", "Coordinates", "Status"])
        self.right_df = pd.DataFrame(self.right_clicks, columns=["Time", "Action", "Coordinates", "Status"])
        return self.left_df.head(), self.right_df.head()

    def use_data(self):
        use_left_thread = threading.Thread(target=self.use_left_data)
        use_right_thread = threading.Thread(target=self.use_right_data)

        use_left_thread.start()
        use_right_thread.start()

    def use_left_data(self, export_data=False, training_data: pd.DataFrame = None):
        i = 0

        if export_data:
            return self.left_df

        if training_data is not None and not training_data.empty:
            while not training_data.empty:
                pyautogui.moveTo(training_data["Coordinates"][i][0], training_data["Coordinates"][i][1])
                mouse.press(Button.left)
                mouse.release(Button.left)
                time.sleep(training_data["Time"][i])
                training_data.drop(i)
                self.log.info(training_data.head(i))

                if i >= len(training_data):
                    break

                i += 1

        while not self.left_df.query("Status == 'pending'").empty:
            pyautogui.moveTo(self.left_df["Coordinates"][i][0], self.left_df["Coordinates"][i][1])
            mouse.press(Button.left)
            mouse.release(Button.left)
            time.sleep(self.left_df["Time"][i])
            self.left_df.loc[i, "Status"] = "used"
            i += 1

    def use_right_data(self, export_data=False, training_data: pd.DataFrame = None):
        i = 0

        if export_data:
            return self.right_df

        if training_data is not None and not training_data.empty:
            while not training_data.empty:
                pyautogui.moveTo(training_data["Coordinates"][i][0], training_data["Coordinates"][i][1])
                mouse.press(Button.right)
                mouse.release(Button.right)
                time.sleep(training_data["Time"][i])
                training_data.drop(i)
                self.log.info(training_data.head(i))

                if i >= len(training_data):
                    break

                i += 1

        while not self.right_df.query("Status == 'pending'").empty:
            pyautogui.moveTo(self.right_df["Coordinates"][i][0], self.right_df["Coordinates"][i][1])
            mouse.press(Button.right)
            mouse.release(Button.right)
            time.sleep(self.right_df["Time"][i])
            self.right_df.loc[i, "Status"] = "used"
            i += 1

    def monitor_mouse(self, x, y, button, _):

        timestamp = time.time()  # Capture timestamp for both clicks

        if len(self.left_clicks) == 1 and not self.invalid_click_left_removed:
            self.left_clicks.pop(0)
            self.invalid_click_left_removed = True

        elif len(self.right_clicks) == 1 and not self.invalid_click_right_removed:
            self.right_clicks.pop(0)
            self.invalid_click_right_removed = True

        if button == Button.left:
            self.left_clicks.append((timestamp - self.last_left_click_time, "left", (x, y), "pending"))
            print("Left click at coordinates:", x, y, "Time since last left click:",
                  timestamp - self.last_left_click_time)
            self.last_left_click_time = timestamp
            print(f"Current List: {self.left_clicks}")

        else:
            self.right_clicks.append((timestamp - self.last_right_click_time, "right", (x, y), "pending"))
            print("Right click at coordinates:", x, y, "Time since last right click:",
                  timestamp - self.last_right_click_time)
            self.last_right_click_time = timestamp
            print(f"Current List: {self.right_clicks}")

    def thread_sleep(self):
        time.sleep(self.seconds)
        self.listener.stop()

        self.log.info("Mouse Recording: Finished timer with recorded data: {}".format(self.recorded_data))
        self.log.info(f"Read data: {self.read_data()}")
        self.use_data()
