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

from app.robo_advisor import to_usd

def test_to_usd():
    result = to_usd(82.9)
    assert result == "$82.90"

def test_url_gathering():
    result = url_gathering(tsla, TEST_API)
    assert result == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=tsla&apikey=TEST_APT"


#def test_recommendation_reason