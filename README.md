# Robo-Advisor

Summary: Issues requests to the AlphaVantage Stock Market API in order to provide automated stock or cryptocurrency trading reccomendations.

## Instalation

Create a new repository and enter its respository name, such as robo-advisor

After creating the remote repo, use GitHub Desktop software or the command-line to download or "clone" it onto your computer. Choose a familiar download location like the Desktop.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

```sh
cd ~/Desktop/robo-advisor
```

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

Then, from within the virtual environment, demonstrate your ability to run the Python script from the command-line:

```sh
python app/robo_advisor.py
```

## Functionality Requirements

Visit https://www.alphavantage.co/support/#api-key to obtain an API Key
Create a new file in this repo called ".env"

After obtaining your API key, place the following in your .env file (with your actual API key specified)

```sh
ALPHAVANTAGE_API_KEY = "_____________"
```

## Usage

To run the script:

```sh
python robo_advisor.pyy
```
