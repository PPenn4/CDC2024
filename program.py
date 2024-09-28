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
short: list[dict] = []

for place in content:
    review_url = place.get("reviews")
    if review_url is not None and place.get("numReviews") >= 10:
        short.append(place)
    
print(len(short))

def findMinRating(collection: list) -> int:
    """Finds the place with the minimum avg rating and return the ID of that place"""
    id: int = collection[0][0]
    minRating: float = collection[0][2]
    for item in collection:
        if item[2] <= minRating:
            minRating = item[2]
            id = item[0]
    return id

places: list = []

i = 0

for s in short:
    if i == 5:
        break
    r = requests.get(s.get("reviews"))
    reviews = r.json()
    review: list[str] = []
    for rev in reviews:
        review.append(rev.get("text"))
    places.append([s.get("id"), s.get("name"), s.get("polarity"),review])
    i += 1;

print(places)





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