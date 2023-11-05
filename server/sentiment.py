from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_vader(sentence):
    sid_obj = SentimentIntensityAnalyzer()

    sentiment_dict = sid_obj.polarity_scores(sentence)
    negative = sentiment_dict['neg']
    neutral = sentiment_dict['neu']
    positive = sentiment_dict['pos']
    compound = sentiment_dict['compound']

    if sentiment_dict['compound'] >= 0.05 :
        overall_sentiment = 1
    elif sentiment_dict['compound'] <= - 0.05 :
        overall_sentiment = -1
    else :
        overall_sentiment = 0
  
    return negative, neutral, positive, compound, overall_sentiment

def get_sentiment(text):
    negative, neutral, positive, compound, overall_sentiment = sentiment_vader(text)
    return overall_sentiment