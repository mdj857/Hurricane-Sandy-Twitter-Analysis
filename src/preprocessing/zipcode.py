
# coding: utf-8

# In[85]:

# Matt Johnson
# 1 December 2017


# In[1]:

import numpy as np 
import pandas as pd 
import seaborn as sns
import time
import os
import sys
from uszipcode import ZipcodeSearchEngine


# In[90]:

if len(sys.argv) < 3:
    print "usage: zipcode.py <input.csv> <output.csv>"
    exit(1)

chunks = pd.read_csv(sys.argv[1], encoding='utf-8', chunksize=60000)
results_csv = sys.argv[2] 
zc = ZipcodeSearchEngine()


# In[88]:

# This function cycles through all tweets and identifies which come from the United States, i.e if 
# the latitude and longitude are within 10 miles of an actual zipcode 
# as well as adding a column for location of the tweet

def get_zip_codes(df, zc):
    zip_codes = []
    for index, row in df.iterrows():
        try:
            res = zc.by_coordinate(row['lat_final'], row['lng_final'], radius=10)
        except Exception as e:
            zip_codes.append(str(0))
            continue
        if not res: 
            zip_codes.append(str(0))
        else: 
            place = res[0]
            zipcode = place["Zipcode"].encode('utf-8')
            zip_codes.append(zipcode)
            
    df['zip_codes'] = zip_codes
    df.zip_codes = df.zip_codes.str.zfill(5)
    return df

for chunk in chunks:
    print chunk.head(1)
    get_zip_codes(chunk, zc).to_csv(results_csv, 
        header=(not os.path.exists(results_csv)), index=False, encoding='utf-8', mode='a')

# In[91]:

# This function cycles through all damage reports and identifies which come from the United States, i.e if 
# the latitude and longitude are within 10 miles of an actual zipcode 
# as well as adding a column for location of the tweet

# def get_zip_codes_damage(df):
#     zip_codes = []
#     lats = df['LATITUDE']
#     longs= df['LONGITUDE']
#     zc = ZipcodeSearchEngine()
#     for i in range(len(df['ID'])):
#         res = zc.by_coordinate(lats[i], longs[i], radius=10)
#         if not res: 
#             zip_codes.append(0)
#         else: 
#             place = res[0]
#             zipcode = place["Zipcode"].encode('utf-8')
#             zip_codes.append(zipcode)
#     df['zip_codes'] = zip_codes
#     df.zip_codes = df.zip_codes.apply('="{}"'.format) # keep leading 0's
#     return df


# # In[92]:

# damage_data_with_zip_codes = get_zip_codes_damage(damage_data)


# # In[93]:

# damage_data_with_zip_codes.to_csv('determination_with_zip_codes.csv')

