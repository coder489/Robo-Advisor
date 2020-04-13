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

from app.robo_advisor import to_usd, url_gathering, recommendation_reason

def test_to_usd():
    result = to_usd(82.9)
    assert result == "$82.90"

def test_url_gathering():
    result = url_gathering("tsla", "TEST_API")
    assert result == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=tsla&apikey=TEST_API"


def test_recommendation_reason():
    result = recommendation_reason(float(10), float(5))
    assert result == "Don't buy, because the current price is greater than 90% of the recent highest price, so you should wait to buy the stock until the price decreases."
