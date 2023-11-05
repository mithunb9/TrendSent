from newsapi import NewsApiClient
import sentiment

DATA_DIR = "data/"
# pls dont steal my api key
newsapi = NewsApiClient(api_key='e40f35b99c484ff694cd9a2d37951bee')

import json

def check_news(company):
    try:
        with open(DATA_DIR + f'{company.lower()}.json') as json_file:
            data = json.load(json_file)
            print("News found")
            return True
    except:
        print("No news found")
        return False
    
def get_news(company):
    if (not check_news(company)):
        articles = newsapi.get_everything(q=company,
                                        language='en',
                                        sort_by='relevancy',
                                        )              
                
        with open(DATA_DIR + f'{company.lower()}.json', 'w') as outfile:
            json.dump(articles, outfile)

        return articles
    else:
        print("No news found")
        return None

def get_sentiment(company):
    get_news(company)
    out = []
   
    with open(DATA_DIR + f'{company.lower()}.json') as json_file:
        data = json.load(json_file)

        articles = data['articles']
        for article in articles:
            try:
                out.append(article['title'] + ". " + article['description'] + ". " + article['content'])
            except:
                pass
            
    for article in out:
        out[out.index(article)] = sentiment.get_sentiment(article)

    return out

    
        
   