# Robo-Advisor

Link to Project Description
https://github.com/prof-rossetti/intro-to-python/blob/master/projects/robo-advisor/README.md

## Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

```sh
pip install -r requirements.txt
```

From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

```sh
python app/robo_advisor.py
```

## Functionality Requirements

Visit https://www.alphavantage.co/support/#api-key to obtain an API Key
Create a new file in this repo called .env

Place the following in your .env file

```sh
ALPHAVANTAGE_API_KEY = "_____________"
```

