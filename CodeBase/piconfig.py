import json
import os

print("Welcome to Stock Capture Configuration Settings")
api_key = input("Insert your Twelve Data API Key here: ")

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)


data = {
    "api_key": api_key,
    "ticker_symbols": [
        "MSFT",
        "AAPL",
        "DIS",
        "FB",
        "BABA",
        "LOW",
        "AMZN",
        "GOOG",
        "SSNLF",
        "TWTR",
    ],
    "iterations": 24,
    "path": path,
    "duration": 7,
    "frequency": 15,
}

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

with open("piconfig.json", "w") as outfile:
    json.dump(data, outfile)

print(f"Configuration file created in directory: {path}")
print("File can be editted further to fit your needs")
