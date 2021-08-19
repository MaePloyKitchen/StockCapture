import requests
import time

ticker_symbols = [
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
]
api_key = "YOUR KEY HERE"


def get_stock_price(ticker_symbol, api_key):
    url = f"https://api.twelvedata.com/price?symbol={ticker_symbol}&apikey={api_key}"
    response = requests.get(url).json()
    price = response["price"]
    return price


def get_stock_quote(ticker_symbol, api_key):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={api_key}"
    response = requests.get(url).json()
    return response


def handle_requests(ticker_symbols):
    # Returns a dictionary of stock information
    result = dict()
    for symbol in ticker_symbols:
        # Call from TwelveData to get stock information
        price = get_stock_price(symbol, api_key)
        quote = get_stock_quote(symbol, api_key)
        time.sleep(15)
        result[symbol] = {"current_price": price, "quote": quote}
    return result


if __name__ == "__main__":
    data = handle_requests(ticker_symbols)
    print(data)
