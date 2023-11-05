import json
import api

DATA_DIR = "data/"

def get_dcf_data(ticker, period):
    try:
        with open(DATA_DIR + f"{ticker}_{period}.json") as f:
            data = json.load(f)
            return data
    except:
        api.get_data(ticker, period)

        with open(DATA_DIR + f"{ticker}_{period}.json") as f:
            data = json.load(f)
            return data
    
# pretty print json
def ppj(data):
    print(json.dumps(data, indent=4))

def get_cap(symbol):
    try:
        with open(DATA_DIR + f"{symbol}_cap.json") as f:
            data = json.load(f)
            return data
    except:
        api.get_market_cap(symbol)

        with open(DATA_DIR + f"{symbol}_cap.json") as f:
            data = json.load(f)
            return data

def get_income(symbol):
    try: 
        with open(DATA_DIR + f"{symbol}_income.json") as f:
            data = json.load(f)
            return data
    except:
        api.get_income_statement(symbol)

        with open(DATA_DIR + f"{symbol}_income.json") as f:
            data = json.load(f)
            return data

def calculate_dcf(data):
    market_cap = get_cap(data["symbol"])

    for cap in market_cap:
        if cap["date"][0:7] == data["date"][0:7]:
            market_cap = cap['marketCap']
            break

    enterprise_value = market_cap + data["longTermDebt"] + data["shortTermDebt"]
    equity_value = enterprise_value - data["netDebt"]
    
    income_statement = get_income(data["symbol"])

    for statement in income_statement:
        if statement["date"][0:4] == data["date"][0:4]:
            income_statement = statement
            break

    try:
        was = income_statement[0]["weightedaveragenumberofdilutedsharesoutstanding"]
    except:
        was = income_statement["weightedaveragenumberofdilutedsharesoutstanding"]

    dfc = equity_value / was

    print(dfc)

# print every dcf based on the last 5 years
def get_dcf(symbol):
    data = get_dcf_data(symbol, "annual")

    for i in range(5):
        calculate_dcf(data[i])

get_dcf("AAPL")




