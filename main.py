import requests;
import pandas as pd
import json
# import seaborn as sns

url = "http://tour-pedia.org/api/getPlaces/csv?location=Berlin&category=poi"
url1 = "http://tour-pedia.org/api/getPlaces?location=Berlin&category=poi"

response = requests.get(url);

response1 = requests.get(url1);

content = response1.json();

for data in content:
    print(data.get("lat"))

