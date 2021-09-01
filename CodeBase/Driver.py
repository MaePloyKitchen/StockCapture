import StockLCDDisplay
import TwelveDataAPI
from time import strftime
import time
import os
import json
import concurrent.futures
import queue
import threading
import FileGenerator

SETTINGS = dict()
PATH = os.path.dirname(os.path.realpath(__file__))
os.chdir(PATH)

# Setting up necessary constants for the Program. Information used to form constants found from piconfig file

with open("piconfig.json") as json_data_file:
    SETTINGS = json.load(json_data_file)

# Related to API CALLS

TICKER_SYMBOLS = SETTINGS["ticker_symbols"]
API_KEY = SETTINGS["api_key"]

TOTAL_RUN_TIME = (
    (SETTINGS["duration"]["hours"] * 3600)
    + (SETTINGS["duration"]["minutes"] * 60)
    + (SETTINGS["duration"]["seconds"])
)
TOTAL_DELAY_BETWEEN_CALLS = (
    (SETTINGS["frequency"]["hours"] * 3600)
    + (SETTINGS["frequency"]["minutes"] * 60)
    + (SETTINGS["frequency"]["seconds"])
)

# Related to Display

MAX_ITERATIONS = TOTAL_RUN_TIME // TOTAL_DELAY_BETWEEN_CALLS


class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=5)

    def get_message(self):
        value = self.get_nowait()
        return value

    def set_message(self, value):
        self.put(value)


def display_thread(lcd_pipeline, event):
    data = dict()
    # Wait for data to be pulled from the API
    while lcd_pipeline.empty():
        StockLCDDisplay.display_startup()

    while not event.is_set() or not lcd_pipeline.empty():
        if not lcd_pipeline.empty():
            data = lcd_pipeline.get_message()
        api_data = data["api_data"]
        for symbol in api_data:
            StockLCDDisplay.display_stock(
                symbol,
                api_data[symbol]["current_price"],
                api_data[symbol]["quote"]["change"],
            )
            time.sleep(5)
        StockLCDDisplay.display_iteration(
            data["timestamp"], data["iteration"], MAX_ITERATIONS
        )
        time.sleep(5)


def api_thread(lcd_pipeline, csv_pipeline, event):
    iterations = 0
    while not event.is_set():
        package = dict()
        package["api_data"] = TwelveDataAPI.handle_requests(TICKER_SYMBOLS, API_KEY)
        package["iteration"] = iterations + 1
        package["timestamp"] = strftime("%I:%M")
        iterations = package["iteration"]

        lcd_pipeline.set_message(package)
        csv_pipeline.set_message(package)

        # Sleep for given delay
        time.sleep(TOTAL_DELAY_BETWEEN_CALLS)


def write_thread(csv_pipeline, event):
    data = dict()
    while not event.is_set() or not csv_pipeline.empty():
        if not csv_pipeline.empty():
            data = csv_pipeline.get_message()
        else:
            continue
        FileGenerator.add_to_file(data, PATH)


def while_inactive():
    StockLCDDisplay.display_inactive()


def while_active():
    lcd_pipeline = Pipeline()
    csv_pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(api_thread, lcd_pipeline, csv_pipeline, event)
        executor.submit(display_thread, lcd_pipeline, event)
        executor.submit(write_thread, csv_pipeline, event)
        time.sleep(TOTAL_RUN_TIME)
        event.set()


if __name__ == "__main__":
    while True:
        if (time.localtime().tm_hour < 9) or (time.localtime().tm_hour > 16):
            while_inactive()
        else:
            while_active()
            break
