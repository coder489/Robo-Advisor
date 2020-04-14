import csv
import json
import os
from dotenv import load_dotenv

import datetime
import time

import requests

import plotly
import plotly.graph_objs as go
import pytest
import json

load_dotenv()

from app.robo_advisor import to_usd, recommendation_reason, get_response, writing_csv, line

def test_to_usd():
    result = to_usd(82.9)
    assert result == "$82.90"

def test_recommendation_reason():
    result = recommendation_reason(float(10), float(5))
    assert result == "Don't buy, because the current price is greater than 90% of the recent highest price, so you should wait to buy the stock until the price decreases."

CI_ENV = os.environ.get("CI") == "true"

@pytest.mark.skipif(CI_ENV==True, reason="to avoid issuing HTTP requests on the CI server") # skips this test on CI
def test_get_response():
    symbol = "tsla"
    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default = "OOPS")
    parsed_response = get_response(symbol, API_KEY) # issues an HTTP request (see function definition below)

    assert isinstance(parsed_response, dict)
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol
#Source: Adapted from https://github.com/prof-rossetti/intro-to-python/blob/master/notes/devtools/travis-ci.md

def test_line():
    result = line("-")
    assert result == "--------------------------------------------------"

def test_writing_csv():
    csv_filepath = os.path.join(os.path.dirname(__file__), "example_data", "sample_prices_daily.csv")

    if os.path.isfile(csv_filepath):
        os.remove(csv_filepath)

    result = writing_csv(csv_filepath)

    assert result == True
    assert os.path.isfile(csv_filepath) == True
    




#with open('data.txt') as json_file:
#    data = json.load(json_file)
#    for p in data['people']: #use os to get the filepath for the json file and make that a variable, replace data.txt with the json file path
#        print('Name: ' + p['name'])
#        print('Website: ' + p['website'])
#        print('From: ' + p['from'])
#        print('')
#
#sample_data_filepath = "test/example_data/prices_daily.json"
#with open(gradebook_filepath, "r") as json_file:
#    file_contents = json_file.read()
#gradebook = json.loads(file_contents)
#print(type(gradebook)) #> <class 'dict'>
#print(gradebook)