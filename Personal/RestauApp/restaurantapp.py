import requests
import json
import time
import pandas as pd

ethiopian_restaurants = []
params = {}

endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=ethiopian+food&key="

res = requests.get(endpoint_url, params = params)
results = json.loads(res.content)
ethiopian_restaurants.extend(results['results'])
time.sleep(2)
while "next_page_token" in results:
    params['pagetoken'] = results['next_page_token'],
    res = requests.get(endpoint_url, params = params)
    results = json.loads(res.content)
    ethiopian_restaurants.extend(results['results'])
    time.sleep(2)
    
place_name = []
address = []
rating = []

for i in range(len(ethiopian_restaurants)):
    restaurant = ethiopian_restaurants[i]
    
    try:
        place_name.append(restaurant['name'])
    except:
        place_name.append('none')
        
    try:
        address.append(restaurant['formatted_address'])
    except:
        address.append('none')
    
    try:
        rating.append(restaurant['rating'])
    except:
        rating.append('none')
        
df_dict = {'Name':place_name, 'Address':address, 'Rating':rating}
ethiopian_restaurants_df = pd.DataFrame(df_dict)
ethiopian_restaurants_df.to_csv('EthiopianRestaurants.csv', index=False, encoding='utf-8')
print("All Done!!")


