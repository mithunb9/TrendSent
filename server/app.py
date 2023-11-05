from flask import Flask
import news

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
