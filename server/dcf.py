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

    return { "date": data["date"], "dcf": dfc }

# print every dcf based on the last 5 years
def get_dcf(symbol):
    out = []
    data = get_dcf_data(symbol, "annual")

    for i in range(15):
        out.append(calculate_dcf(data[i]))

    return out

# print("AAPL")
# ppj(get_dcf("AAPL"))

# print("GS")
# ppj(get_dcf("GS"))

# print("MSFT")
# ppj(get_dcf("MSFT"))

# print("O")
# ppj(get_dcf("O"))

# print("COKE")
# ppj(get_dcf("COKE"))

# print("JPM")
# print(get_dcf("JPM"))

# print("WFC")
# print(get_dcf("WFC"))

# print("BAC")
# print(get_dcf("BAC"))

# print("C")
# print(get_dcf("C"))

# print("SCHW")
# print(get_dcf("SCHW"))

# print("MS")
# print(get_dcf("MS"))

# print("NFLX")
# print(get_dcf("NFLX"))

# print("NVDA")
# print(get_dcf("NVDA"))

# print("AMZN")
# print(get_dcf("AMZN"))

# print("MCD")
# print(get_dcf("MCD"))

# print("QCOM")
# print(get_dcf("QCOM"))

# print("INTC")
# print(get_dcf("INTC"))

# print("EOG")
# print(get_dcf("EOG"))

# print("CBRE")
# print(get_dcf("CBRE"))
