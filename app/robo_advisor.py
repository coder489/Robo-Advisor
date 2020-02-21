# app/robo_advisor.py

##### IMPORTS #####
import requests
import json
import os
from dotenv import load_dotenv
import datetime
import time


##### CODE #####

load_dotenv()

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default = "OOPS")

symbol = "TSLA"

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
print("URL:", request_url)

response = requests.get(request_url)
#print(type(response)) #> response
#print(response.status_code) #> 200
#print(type(response.text)) #> str

parsed_response = json.loads(response.text)


### Request At ###

t = time.localtime() #Code from https://www.programiz.com/python-programming/datetime/current-datetime
current_time = time.strftime("%I:%M %p", t) # code from https://www.programiz.com/python-programming/datetime/current-datetime
                                           #Time format was edited by me to make it more readable to the user


### Latest Day ###

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
# print(type(parsed_response)) #> dict


### Information Outputs ###

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {str(datetime.date.today())} {current_time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")



















print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")