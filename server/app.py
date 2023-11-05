from flask import Flask, jsonify
from flask_cors import CORS
import news
import api
import model

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return "hi"

print("Initialized server sucessfully")
@app.route('/sentiment/<company>')
def sentiment(company):
    sentiment = news.get_sentiment(company)
    
    # remove all neutral sentiments
    sentiment = [s for s in sentiment if s != 0]

    out = {}
    out['sentiment'] = sentiment
    out['average'] = sum(sentiment) / len(sentiment)
    out['negative'] = len([s for s in sentiment if s == -1])
    out['positive'] = len([s for s in sentiment if s == 1])
    out['percent'] = out['positive'] / (out['positive'] + out['negative'])
    out['company'] = company

    return out

@app.route('/companies')
def companies():
    return api.get_companies()

@app.route('/predict/<company>')
def predict(company):
    with open(f'data/{company}.csv') as f:
        data = f.read().splitlines()

        # parse date (remove time)
        data = [d.split(',')[0] for d in data]

        print(data)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

