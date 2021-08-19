import json

print("Welcome to Stock Capture Configuration Settings")
api_key = input("Insert your Twelve Data API Key here: ")
email = input("Insert your email id here: ")

data = {
    "api_key": api_key,
    "email": email,
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
}

with open("piconfig.json", "w") as outfile:
    json.dump(data, outfile)
