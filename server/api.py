import requests
import json

def get_data(ticker, period):
    API_KEY = "1JeACD0Znul5cesWO0KiZthh2suTGKEo"  
    API_ENDPOINT = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&apikey={API_KEY}"
    
    response = requests.get(url=API_ENDPOINT)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve {period} data for {ticker}. Status code: {response.status_code}")
        return None

def save_data(data, ticker, period):
    if data:
        with open(f"{ticker}_{period}.json", "w") as f:
            json.dump(data, f, indent=4)  

tickers = ["AAPL", "TSLA", "GS"]
periods = ["annual", "quarter"]

for ticker in tickers:
    for period in periods:
        data = get_data(ticker, period)
        if data:
            save_data(data, ticker, period)
