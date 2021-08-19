import StockLCDDisplay
import TwelveDataAPI
from time import strftime
import time
import concurrent.futures

ticker_symbols = ['MSFT','AAPL','DIS','FB','BABA','LOW','AMZN','GOOG','SSNLF','TWTR']
#720 Requests per day

data = dict()
is_running = True
iterations = 0

def waiting():
    while True:
        if (time.localtime().tm_hour < 9) or (time.localtime().tm_hour > 16):
            StockLCDDisplay.display_inactive()
        else:
            main()

def display_thread():
    global is_running
    #Wait for data to be pulled from the API
    while iterations == 0:
        StockLCDDisplay.display_startup()
    while is_running:
        local_data = data
        local_iterations = iterations
        for symbol in local_data:
            StockLCDDisplay.display_stock(symbol,local_data[symbol]['current_price'],local_data[symbol]['quote']['change'])
            time.sleep(5)
        StockLCDDisplay.display_iteration(strftime('%I:%M'),local_iterations)
        time.sleep(5)
        
        if local_iterations == 24:
            is_running = False
        
        
        
    

def api_thread():
    global data
    global iterations
    
    #Run for the first time
    data = TwelveDataAPI.handle_requests(ticker_symbols)
    iterations = 1
    time.sleep(900)
    while is_running:
        data = TwelveDataAPI.handle_requests(ticker_symbols)
        iterations += 1
        #Sleep for 15 Minutes
        time.sleep(900)

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(api_thread)
        executor.submit(display_thread)
    
if __name__ == '__main__':
    waiting()