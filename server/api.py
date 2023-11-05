import requests
import json

import os

from dotenv import load_dotenv
load_dotenv()

DATA_DIR = "data/"

def get_data(ticker, period):
    API_ENDPOINT = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&apikey={os.getenv('API_KEY')}"

    response = requests.get(url=API_ENDPOINT)

    if response.status_code == 200:
        data = response.json()
        save_data(data, ticker, period)
    else:
        print(f"Failed to retrieve {period} data for {ticker}. Status code: {response.status_code}")
        return None

def save_data(data, ticker, period):
    if data:
        with open(DATA_DIR + f"{ticker}_{period}.json", "w") as f:
            json.dump(data, f, indent=4)  

def get_market_cap(ticker):
    API_ENDPOINT = f"https://financialmodelingprep.com/api/v3/historical-market-capitalization/{ticker}?limit=5000&apikey={os.getenv('API_KEY')}"

    response = requests.get(url=API_ENDPOINT)

    if response.status_code == 200:
        data = response.json()
        save_market_cap(data, ticker)
    else:
        print(f"Failed to retrieve market cap data for {ticker}. Status code: {response.status_code}")
        return None
    
def save_market_cap(data, ticker):
    if data:
        with open(DATA_DIR + f"{ticker}_cap.json", "w") as f:
            json.dump(data, f, indent=4)

def get_income_statement(ticker):
    API_ENDPOINT = f"https://financialmodelingprep.com/api/v3/income-statement-as-reported/{ticker}?period=annual&limit=50&apikey={os.getenv('API_KEY')}"

    response = requests.get(url=API_ENDPOINT)

    if response.status_code == 200:
        data = response.json()
        save_income_statement(data, ticker)
    else:
        print(f"Failed to retrieve income statement data for {ticker}. Status code: {response.status_code}")
        return None
    
def save_income_statement(data, ticker):
    if data:
        with open(DATA_DIR + f"{ticker}_income.json", "w") as f:
            json.dump(data, f, indent=4)