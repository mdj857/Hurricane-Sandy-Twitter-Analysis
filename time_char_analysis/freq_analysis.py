# -*- coding: utf-8 -*-
"""
Created on Sat Dec 09 15:55:02 2017

@author: Matthew Edwards
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar, time, re, datetime
from time import mktime
import pickle

#%% Read Tweets and damage information
tweets_ny = pd.read_csv('ny_tweets.csv', encoding='utf-8', engine='c')
damage_data = pd.read_csv('determination.csv')


#%%
# This function takes a list of zipcodes of the locations (including duplicates) and 
# the top 'num_zips' most frequently occuring zipcodes and returns all tweets from those zipcodes 
def get_tweets_from_zipcode(damage_zip, num_zips): 
    top_zips = damage_zip.value_counts().head(num_zips).index
    return tweets_ny[tweets_ny["zipcode"].isin(top_zips)]["text"]

#%% Get damaged buildings count

affected_tweets, destroyed_tweets = [], []
minor_tweets, major_tweets = [], []

affected_zips = damage_data[damage_data["Affected"] == 1]["ZIPCODE"]
minor_zips = damage_data[damage_data["Minor"] == 1]["ZIPCODE"]
major_zips = damage_data[damage_data["Major"] == 1]["ZIPCODE"]
destroyed_zips = damage_data[damage_data["Destroyed"] == 1]["ZIPCODE"]

affected_tweets.extend(get_tweets_from_zipcode(affected_zips, 100))
minor_tweets.extend(get_tweets_from_zipcode(minor_zips, 100))
major_tweets.extend(get_tweets_from_zipcode(major_zips, 100))
destroyed_tweets.extend(get_tweets_from_zipcode(destroyed_zips, 100))

#%% Count per zip
zip_to_dist = {}
for zipcode in range(6001, 11980):
    num_affected = float(len(affected_zips[affected_zips == zipcode]))
    num_minor = float(len(minor_zips[minor_zips == zipcode]))
    num_major = float(len(major_zips[major_zips == zipcode]))
    num_destroyed = float(len(destroyed_zips[destroyed_zips == zipcode]))
    
    num_total = float(num_affected + num_minor + num_major + num_destroyed)
    
    if num_total == 0:
        zip_to_dist[zipcode] = [np.nan, np.nan, np.nan, np.nan]
        continue
    
    num_affected = num_affected / num_total
    num_minor = num_minor / num_total
    num_major = num_major / num_total
    num_destroyed = num_destroyed / num_total
    
    zip_to_dist[zipcode] =  [num_affected, num_minor, num_major, num_destroyed]

#%% Save
with open('zip_to_dist.pkl', 'wb') as handle:
    pickle.dump(zip_to_dist, handle, protocol=pickle.HIGHEST_PROTOCOL)

    
