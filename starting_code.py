import requests;
import pandas as pd
import json



url1 = "http://tour-pedia.org/api/getPlaces?location=Berlin&category=restaurant"

review_url = "http://tour-pedia.org/api/getReviews?location=Berlin&language=en&category=restaurant"

review_response = requests.get(review_url)

# response = requests.get(url);

response1 = requests.get(url1);

reviews = review_response.json()

content = response1.json();

print(reviews[0].keys())
print(len(reviews))

print(content[0].keys())
print(content[0].get("reviews"))
