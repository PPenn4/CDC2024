import requests;
import pandas as pd
import json

url = "http://tour-pedia.org/api/getPlaces?"
city = input("Which city would you like to visit? \n  Choose one from the followng (Amsterdam, Barcelona, Berlin, Dubai, London, Paris, Rome, Tuscany)\n")
url = url + "location=" + city.capitalize()
cat = input("Select a category: accomodation, restaurant, poi, attraction\n")
url = url + "&category=" + cat.lower()
print(url);

response = requests.get(url);
content = response.json();
short = []

for place in content:
    review_url = place.get("reviews")
    if review_url is not None and place.get("numReviews") >= 10:
        short.append(place)
    
print(len(short))






# def max(collection: list[dict]) -> int:
#     maxx = 0
#     for item in collection:
#         if item.get("numReviews") >= maxx:
#             maxx = item.get("numReviews")

#     return maxx

# def min(collection: list[dict]) -> int:
#     minn = collection[0].get("numReviews")
#     for item in collection:
#         if item.get("numReviews") <= minn:
#             minn = item.get("numReviews")

#     return minn

# print(max(short))