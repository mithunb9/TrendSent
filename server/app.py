from flask import Flask, jsonify
from flask_cors import CORS
import news
import api
import json
import model

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return "Hello, world!"

print("Initialized server sucessfully")
@app.route('/sentiment/<company>')
def sentiment(company):
    return api.get_sent_analysis(company)

@app.route('/companies')
def companies():
    return api.get_companies()

@app.route('/predict/<company>')
def predict(company):
    out = []

    with open(f'data/{company}.csv') as f:
        data = f.read().splitlines()
        
        date_data = [d.split(',')[0] for d in data]

        date_data = [d.split('-')[0] + '-' + d.split('-')[1] for d in date_data]
        
        data.pop(1)

        for i in range(len(data)):
            data[i] = data[i].split(',')
            data[i][0] = date_data[i]

        data = data[1:]

        for d in data:
            out.append({
                'date': d[0],
                'value': d[2],
            })
    
    combined = []   
    with open(f'data/{company}_dcf.json') as f:
        dcf = json.load(f)

        for d in dcf:
            combined.append({
                'date': d['date'],
                'value': d['dcf'],
            })

        combined.reverse()

    combined.extend(out)

    return jsonify(combined)

if __name__ == '__main__':
    app.run(debug=True)

