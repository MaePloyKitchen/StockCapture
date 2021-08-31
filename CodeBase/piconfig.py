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
    "duration": {
        "hours": 0,
        "minutes":30,
        "seconds":0
    },
    "frequency": {
        "hours":0,
        "minutes":15,
        "seconds":0
    } 
}

with open("piconfig.json", "w") as outfile:
    json.dump(data, outfile)

print(f"Configuration file created in directory: {path}")
print("File can be editted further to fit your needs")

#path += "\\Data"
#os.mkdir("Data")
