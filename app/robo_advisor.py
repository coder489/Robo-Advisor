import csv
import json
import os
from dotenv import load_dotenv

import datetime
import time

import requests


### Accept User Symbol Input ###

#while True: 
symbol = input("Please input a company's ticker symbol to collect its recent stock price data:")
#    if symbol.isalpha():   #https://stackoverflow.com/questions/36432954/python-validation-to-ensure-input-only-contains-characters-a-z       
#        break
#    if len(symbol) > int(4): #figure out
#        break
#    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")        
#    exit()

#while True: 
#    symbol = input("Please input a company's ticker symbol to collect its recent stock price data:")
#    if symbol.isalpha():   #https://stackoverflow.com/questions/36432954/python-validation-to-ensure-input-only-contains-characters-a-z       
#        break
#    if len(symbol) > 4: #figure out
#        break
#    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")        
#    exit()


### Get API Key, and get information from URL ###

load_dotenv()

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default = "OOPS")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"


response = requests.get(request_url)
#print(type(response)) #> response
#print(response.status_code) #> 200
#print(type(response.text)) #> str

parsed_response = json.loads(response.text)

#print(parsed_response)


### Request At Date and Time ###

t = time.localtime() #Code from https://www.programiz.com/python-programming/datetime/current-datetime
current_time = time.strftime("%I:%M %p", t) # code from https://www.programiz.com/python-programming/datetime/current-datetime
                                           #Time format was edited by me to make it more readable to the user


### Latest Day ###

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
# print(type(parsed_response)) #> dict


### Latest Closing Price ###

def to_usd(my_price):
    return f"${my_price:,.2f}" #https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0] #assumes that the date on top is the latest date, but consider sorting to ensure

latest_close = tsd[latest_day]["4. close"]


### Recent High and Low ###

prices = []

for date in dates:
    price = tsd[date]["2. high"]
    price = tsd[date]["3. low"]
    prices.append(float(price))

recent_high = max(prices)
recent_low = min(prices)


### Reccomendation ###

if float(latest_close) <  float(.90) * float(recent_high):
    reccomendation = "Don't Buy"
else:
    reccomendation = "Buy"

### Write Data to CSV ###

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames = csv_headers)
    writer.writeheader() 
    for date in dates:
        daily_prices = tsd[date]        
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })
    


### Information Outputs ###

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}") 
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {str(datetime.date.today())} {current_time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION {reccomendation}") # to do: provide reccomendation
print("RECOMMENDATION REASON: The current price is less than 90% the recent highest price")
print("-------------------------")
print(f"Writing Data to CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
