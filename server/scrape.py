# from newsapi import NewsApiClient

# # Init
# newsapi = NewsApiClient(api_key='e40f35b99c484ff694cd9a2d37951bee')

# all_articles = newsapi.get_everything(q='apple',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       )

# twentytwo_articles = newsapi.get_everything(q='apple',
#                                        language='en',
#                                     sort_by='relevancy',
#                                         from_param='2022-01-01',
#                                         to='2022-01-31',
#                                         )

# print(all_articles)

# # Save to JSON
# import json

# with open('data.json', 'w') as outfile:
#     json.dump(all_articles, outfile)

# with open('data2.json') as json_file:
#     json.dump(twentytwo_articles, json_file)

scrape = "https://www.google.com/search?q=apple+news&tbs=cdr%3A1%2Ccd_min%3A2022%2Ccd_max%3A2022&tbm=nws"
import requests

response = requests.get(scrape, headers={"User-Agent": "Mozilla/5.0"})
print(response.status_code)

from bs4 import BeautifulSoup as bs

soup = bs(response.text, "html.parser")

print(soup.prettify())

# Save to html
with open('data.html', 'w') as outfile:
    outfile.write(response.text)

# scrape all the articles (links, titles, descriptions)
articles = soup.find_all("div", {"class": "dbsr"})
print(articles)

