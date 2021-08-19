import json

print("Welcome to Stock Capture Configuration Settings")
api_key = input("Insert your API Key here: ")
email = input("Insert your email id here: ")

data = {
    "api_key": api_key,
    "email": email,
}

with open("piconfig.json", "w") as outfile:
    json.dump(data, outfile)
