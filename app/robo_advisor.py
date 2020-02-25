import csv
import json
import os
from dotenv import load_dotenv

import datetime
import time

import requests

import plotly
import plotly.graph_objs as go

### Accept User Symbol Input ###
#### FINISH VALIDATION #####

symbol = input("Please input a company's ticker symbol to collect its recent stock price data:")
if not symbol.isalpha():   #https://stackoverflow.com/questions/36432954/python-validation-to-ensure-input-only-contains-characters-a-z       
    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")        
    exit()
elif len(symbol) > 4: 
    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")    
    exit()    
   

### Get API Key, and get information from URL ###

load_dotenv()

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default = "OOPS")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"


response = requests.get(request_url)
#print(type(response)) #> response
#print(response.status_code) #> 200
#print(type(response.text)) #> str

response_receipt = response.text
#print(parsed_response)
#print(type(parsed_response))

if "Error" in response_receipt:
    print("Sorry, couldn't find any trading data for that stock symbol. Please try again")
    exit()

parsed_response = json.loads(response.text)

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


### Recommendation ###

reccommendation_reason = ""
if float(latest_close) <  float(.90) * float(recent_high):
    recommendation = "Buy"
    recommendation_reason = "The current price is less than 90% the recent highest price, thus the stock is possibly undervalued and you can buy it low then sell it when the price increases again"
else:
    recommendation = "Don't Buy"
    recommendation_reason = "The current price is greater than 90% the recent highest price, so you should wait to buy the stock until the price decreases."



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
print(f"RECOMMENDATION {recommendation}") 
print(f"RECOMMENDATION REASON: {recommendation_reason}")
print("-------------------------")
print(f"Writing Data to CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


### Line Chart ###


layout = go.Layout(                     #https://plot.ly/python/v3/tick-formatting/
    title=("Close Price of " + symbol.upper() + " Stock Over Time"),
    yaxis = go.layout.YAxis(
        tickformat="$",
        title=go.layout.yaxis.Title(      #https://plot.ly/python/v3/figure-labels/
            text=("Close Price of Stock (in dollars)")
        )
    ),
    xaxis = go.layout.XAxis(
        title= go.layout.xaxis.Title(        
            text=("Trading Day")
        )
    )
)



line_data = []

for y in dates:
    sub_dictionary = {"date": y,"close_price": parsed_response["Time Series (Daily)"][y]["4. close"]}
    line_data.append(sub_dictionary)

date_list = [x["date"] for x in line_data]         #Code edited from the in class three charts assignment that was an in class assignment that I worked on with Tim Palmieri
price_list = [y["close_price"] for y in line_data]

plotly.offline.plot({
    "data": [go.Scatter(x = date_list, y = price_list)],
    "layout": layout
}, auto_open=True)



## Attempt 3

#line_data = parsed_response
#
#date_list = [x[0] for x in parsed_response] 
#
#high_price = []
#low_price = []
#close_price = []
#
#for x in parsed_response["Time Series (Daily)"].values():
#    high_price.append(x["2. high"])
#    low_price.append(x["3. low"])
#    close_price.append(x["4. close"])
#
#
#plotly.offline.plot({
#    "data": [go.Scatter(x=date_list, y=high_price)],
###    "data_2": [go.Scatter(x=date_list, y=low_price)],
###    "data_3": [go.Scatter(x=date_list, y=close_price)]
#    "layout": go.Layout(title="hello world")
#}, auto_open=True)


## Attempt 2
#line_data = list(tsd.keys())
#
#date_list = [x[0] for x in line_data]
#
#high_price = [y["2. high"] for y in line_data]
#
#plotly.offline.plot({
#    "data_1": [go.Scatter(x=date_list, y=high_price)],
##    "data_2": [go.Scatter(x=date_list, y=low_price)],
##    "data_3": [go.Scatter(x=date_list, y=close_price)]
#    "layout": go.Layout(title="hello world")
#}, auto_open=True)


## Attempt 1
#dict(("Time Series (Daily)", int(v)) for k, v in parsed_response.items()) #https://stackoverflow.com/questions/9224385/in-dictionary-converting-the-value-from-string-to-integer

#v=[]
#
#dict((k, float(v)) for k, v in tsd.items())
#
#line_data = parsed_response
#
#date_list = [x[0] for x in parsed_response]   #### place in requirements and readme
#
#high_price = [y["2. high"] for y in parsed_response]
#low_price = [y["3. low"] for y in parsed_response]
#close_price = [y["4. close"] for y in parsed_response]
#
#plotly.offline.plot({
#    "data_1": [go.Scatter(x=date_list, y=high_price)],
# #   "data_2": [go.Scatter(x=date_list, y=low_price)],
#  #  "data_3": [go.Scatter(x=date_list, y=close_price)]
#     "layout": go.Layout(title="hello world")
#}, auto_open=True)






