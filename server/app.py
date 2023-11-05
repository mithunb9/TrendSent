from flask import Flask, jsonify
from flask_cors import CORS
import news
import api
import json
import model

app = Flask(__name__)
CORS(app)

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

def read_csv_data(company):
    data = []
    try:
        with open(f'data/{company}.csv') as f:
            for line in f.read().splitlines():
                parts = line.split(',')
                if len(parts) == 3:
                    data.append({
                        'date': parts[0].split()[0],
                        'value': float(parts[2])
                    })
    except FileNotFoundError:
        # Handle file not found error
        pass
    return data

def read_dcf_data(company):
    data = []
    try:
        with open(f'data/{company}_dcf.json') as f:
            dcf = json.load(f)
            for entry in dcf:
                data.append({
                    'date': entry['date'],
                    'value': entry['dcf']
                })
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle file not found or JSON parsing error
        pass
    return data

@app.route('/predict/<company>')
def predict(company):
    csv_data = read_csv_data(company)
    dcf_data = read_dcf_data(company)

    # Combine and sort data by date
    combined_data = sorted(csv_data + dcf_data, key=lambda x: x['date'])

    return jsonify(combined_data)
if __name__ == '__main__':
    app.run(debug=True)

