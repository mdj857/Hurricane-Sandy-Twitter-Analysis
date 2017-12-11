# -*- coding: utf-8 -*-
"""
looking at determination.csv 

"""

import numpy as np 
import pandas as pd 
import seaborn as sns
from geopy.geocoders import Nominatim
from pygeocoder import Geocoder

data = pd.read_csv('datasets/determination.csv')

print data.columns
#%%
# This function cycles through all tweets and identifies which come from the United States
# as well as adding a column for location of the tweet
def get_zip_codes(df):
    locations = []
    geolocator = Nominatim()
    for i in range(len(df['ID])):
        point = str(df.iloc[i]['LATITUDE']) + ', ' + str(df.iloc[i]['LONGITUDE'])
        
        try:
            location = geolocator.reverse(point)
        except Exception as e: 
            print ('WiFi connection perhaps lost !! Trying one more time...')
            try:
                location = geolocator.reverse(point)
            except:
                try:
                    location = geolocator.reverse(point)
                except:
                    print ('WiFi connection really lost !! Bailing out..')
                    print(Exception)

        
        location_address = location.address.encode('utf-8')
        locations.append(location_address)
        
    df['locations'] = locations
#%%
requests.get(link, headers = {'User-agent': 'your bot 0.1'})
point = str(data.iloc[1]['LATITUDE']) + ', ' + str(data.iloc[1]['LONGITUDE'])
geolocator = Nominatim()
location = geolocator.reverse(point)
location_address = location.address.encode('utf-8')
#result = Geocoder.geocode(location_address)
print location_address
equests.get(link, headers = {'User-agent': 'your bot 0.1'})

#filter_to_USA(data)