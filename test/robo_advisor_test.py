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

load_dotenv()

from app.robo_advisor import to_usd, recommendation_reason, get_response

def test_to_usd():
    result = to_usd(82.9)
    assert result == "$82.90"

#def test_url_gathering():
#    result = url_gathering("tsla", "TEST_API")
#    assert result == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=tsla&apikey=TEST_API"
#

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
#Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/devtools/travis-ci.md

