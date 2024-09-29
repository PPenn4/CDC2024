import pandas as pd
import seaborn as sns
import requests
import json
import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', None)
# Get user inputs
placeURL = "http://tour-pedia.org/api/getPlaces?"
city = input("Which city would you like to visit? \nChoose one from the following (Amsterdam, Barcelona, Berlin, Dubai, London, Paris, Rome, Tuscany)\n").lower().capitalize()
placeURL = placeURL + "location=" + city
cat = input("Select a category: accommodation, restaurant, poi, attraction\n").lower()
placeURL = placeURL + "&category=" + cat
pd.set_option('display.max_colwidth', None)
# Make the request
response = requests.get(placeURL)
content = response.json()
places = []
for place in content:
    review_url = place.get("reviews")
    if review_url is not None and place.get("numReviews") >= 10:
        places.append(place)
df = pd.DataFrame(places)
df.drop(columns= ['subCategory', 'details', 'originalId', 'lat', 'lng', 'location', 'category'], inplace=True)


avgRates = []
engCount = []
for rev in df['reviews']:
    revData = []
    res = requests.get(rev)
    con = res.json()
    for thing in con:
        revData.append(thing)

    revDF = pd.DataFrame.from_dict(revData)
    revDF.drop(columns=['polarity', 'time', 'wordsCount', 'details', 'text', 'source'], inplace=True)
    for ind in revDF.index:
        if type(revDF['rating'][ind]) == str:
            revDF.drop(ind, inplace=True)
    avgRates.append(revDF['rating'].mean())
    engCount.append(revDF['language'].value_counts().get('en', 0))

df['Average Rating'] = avgRates
df['Number of English Reviews'] = engCount
df = df.sort_values(by=['numReviews'], ascending=False)
top30 = df.head(15).reset_index()

sns.barplot(data = top30, x = 'Number of English Reviews', y = 'name')
plt.show()