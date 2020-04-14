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

def test_line():
    result = line("-")
    assert result == "--------------------------------------------------"


CI_ENV = os.environ.get("CI") == "true"

@pytest.mark.skipif(CI_ENV==True, reason="to avoid issuing HTTP requests on the CI server") # skips this test on CI
def test_get_response():
    symbol = "tsla"
    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default = "OOPS")
    parsed_response = get_response(symbol, API_KEY) # issues an HTTP request (see function definition below)

    assert isinstance(parsed_response, dict)
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol
#Source: Adapted from https://github.com/prof-rossetti/intro-to-python/blob/master/notes/devtools/travis-ci.md


def test_writing_csv():
    csv_filepath = os.path.join(os.path.dirname(__file__), "example_data", "sample_prices_daily.csv")

    mock_tsd = {
        '2020-04-14': {'1. open': '698.9700', '2. high': '741.8800', '3. low': '692.4300', '4. close': '709.8900', '5. volume': '29912574'}, 
        '2020-04-13': {'1. open': '590.1600', '2. high': '652.0000', '3. low': '580.5300', '4. close': '650.9500', '5. volume': '21645267'}, 
        '2020-04-09': {'1. open': '562.0900', '2. high': '575.1818', '3. low': '557.1100', '4. close': '573.0000', '5. volume': '13650000'}, 
        '2020-04-08': {'1. open': '554.2000', '2. high': '557.2081', '3. low': '533.3300', '4. close': '548.8400', '5. volume': '12656024'}, 
        '2020-04-07': {'1. open': '545.0000', '2. high': '565.0000', '3. low': '532.3400', '4. close': '545.4500', '5. volume': '17919784'}, 
        '2020-04-06': {'1. open': '511.2000', '2. high': '521.0000', '3. low': '497.9600', '4. close': '516.2400', '5. volume': '14901836'}
    }
    mock_dates = ['2020-04-14', '2020-04-13', '2020-04-09', '2020-04-08', '2020-04-07', '2020-04-06']

    result = writing_csv(csv_filepath, mock_dates, mock_tsd)

    assert result == True
    assert os.path.isfile(csv_filepath) == True




