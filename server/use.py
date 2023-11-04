import json

with open('data.json') as json_file:
    data = json.load(json_file)

print(len(data['articles']))

# count articles per year
years = {}

for article in data['articles']:
    year = article['publishedAt'][:4]
    if year in years:
        years[year] += 1
    else:
        years[year] = 1

print(years)


