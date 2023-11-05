import pandas as pd 

df = pd.read_csv('twitter_dataset.csv')
df = df.iloc[:,0]

def search_sentiment(company):
    company = company.lower()
    company = company.replace(" ", "")

    tweets = df[df.str.contains(company)]

    return tweets

print(len(search_sentiment("apple")))
