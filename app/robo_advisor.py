import csv
import json
import os
from dotenv import load_dotenv

import datetime
import time

import requests

import plotly
import plotly.graph_objs as go

load_dotenv()

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Parameters: 
    
        my_price (int or float): a price value that is not formatted like 4000.444444
        
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    """
    return f"${my_price:,.2f}" 

def current_time():
    """
    Used to get the current time, format it, and then return it.
        
    Source: https://www.programiz.com/python-programming/datetime/current-datetime
    """
    t = time.localtime()                
    time_now = time.strftime("%I:%M %p", t) 
    return time_now

def line(symbol):
    """
    Creates a divider out of a specified symbol.
    
    Parameters: 
    
        symbol (str): any symbol that you wish to use repeatedly to form a divider, like "*" or "-"

    """
    return symbol * 50

def get_response(stock_symbol, api):
    """
    Gets prices of stock from a specified url from alphavantage, validates that the company ticker requested exists, and then returns the requested information as json.loads.
    
    Parameters: 
    
        stock_symbol (str): must be 4 characters or less, and only contains letters, like "msft"
    
        api (str): an API key that can be obtained through alphavantage)

    Source: Adapted from https://github.com/prof-rossetti/intro-to-python/blob/master/notes/devtools/travis-ci.md
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={api}"
    response = requests.get(url) # issues an HTTP request
    good_response = response.text
    if "Error" in good_response:
        print("Sorry, couldn't find any trading data for that stock symbol. Please try again")
        exit()
    else:
        return json.loads(response.text)

def recommendation_reason(latest_close, recent_high):
    """
    Prints a recommendation in regards to buying stock based on the most recent high and low stock prices.

    Parameters: 
    
        latest_close (float or int): a price value, like 456.9980 or 456 
    
        recent_high (float or int): a price value, like 45.6868 or 45

    """
    if float(latest_close) < float(0.9) * float(recent_high):
        recommendation = "Buy, because the current price is less than 90% of the recent highest price, thus the stock is possibly undervalued and you can buy it low then sell it when the price increases again"
    else:
        recommendation = "Don't buy, because the current price is greater than 90% of the recent highest price, so you should wait to buy the stock until the price decreases."
    return recommendation

def writing_csv(csv_filepath, all_dates, stock_price_data): 
    """
    Gathers data given, loops through that data, and collects requested information, then writes the information to a csv file at the specified file path.

    Parameters: 
    
        csv_filepath (str): desired filepath for the csv file
    
        all_dates (list): a list of first element of each dictionary in looped through dictionary of dictionaries
    
        stock_price_data (dict): dictionary of dictionaries, each dict has key value pairs unique to a certain date

    Source: Adapted from Prof Rosetti's screen cast of Robo Advisor
    """

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() 
        for date in all_dates:
            daily_prices = stock_price_data[date] 
            writer.writerow({
                "timestamp": date,
                "open": daily_prices["1. open"],
                "high": daily_prices["2. high"],
                "low": daily_prices["3. low"],
                "close": daily_prices["4. close"],
                "volume": daily_prices["5. volume"]
            })
    return True

if __name__ == "__main__":
    
    ### INFORMATION INPUTS AND DATA COLLECTION ###

    # ACCEPT USER SYMBOL INPUT AND VALIDATE IT

    symbol = input("Please input a company's ticker symbol to collect its recent stock price data:")
    if not symbol.isalpha():   #https://stackoverflow.com/questions/36432954/python-validation-to-ensure-input-only-contains-characters-a-z       
        print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")        
        exit()
    elif len(symbol) > 4: 
        print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")    
        exit()    
   

    # COLLECTING INFO REQUESTED BY USER AND VERIFYING IT EXISTS

    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default = "OOPS")

    parsed_response = get_response(symbol, API_KEY)

   
    # COLLECT THE LATEST DAY AND LATEST CLOSING PRICE
    
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    tsd = parsed_response["Time Series (Daily)"]

    dates = list(tsd.keys())

    latest_day = dates[0] 

    latest_close = tsd[latest_day]["4. close"]


    # COLLECT THE RECENT HIGH AND LOW

    prices = []

    for date in dates:
        price = tsd[date]["2. high"]
        price = tsd[date]["3. low"]
        prices.append(float(price))

    recent_high = max(prices)
    recent_low = min(prices)

    ### INFORMATION OUTPUTS ###

    # WRITE DATA TO CSV FILE

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

    writing_csv(csv_file_path, dates, tsd)
   
    ## INFORMATION GIVEN IMMEDIATELY TO USER

    print(line("-"))
    print(f"SELECTED SYMBOL: {symbol.upper()}") 
    print(line("-"))
    print("REQUESTING STOCK MARKET DATA...")
    print(f"REQUEST AT: {str(datetime.date.today())} {current_time()}")
    print(line("-"))
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print(line("-"))
    print(f"RECOMMENDATION: {recommendation_reason(float(latest_close), float(recent_high))}") 
    print(line("-"))
    print("Writing Data to CSV...")
    print(f"You may now access the CSV via this file path: {csv_file_path}")
    print(line("-"))
    print("A visualization of the stock close prices over time can be seen in your browser.")
    print(line("-"))
    print("HAPPY INVESTING!")
    print(line("-"))

    ## VISUALIZATION OUTPUT

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









