import requests
import json

def get_finance_data(ticker): 
    # pls dont steal my api key
    FINANCE_ENDPOINT = f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{ticker}?apikey=1JeACD0Znul5cesWO0KiZthh2suTGKEo"

    response = requests.get(url=FINANCE_ENDPOINT)

    if response.status_code == 200:
        data = response.json()

        return data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

        return None

def check_finance_data(ticker):
    try:
        with open(f'{ticker.lower()}_finance.json') as json_file:
            data = json.load(json_file)
            print("Finance data found")
            return True
    except:
        print("No finance data found")
        return False

def get_dcf(ticker):
    if (not check_finance_data(ticker)):
        data = get_finance_data(ticker)

        with open(f'{ticker.lower()}_finance.json', 'w') as outfile:
            json.dump(data, outfile)

        return data
    else:
        print("No finance data found")
        return None

print(get_dcf("GS"))