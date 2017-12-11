import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar, time, re, datetime
from time import mktime
import pickle
import random

#%% Read Tweets and damage information
tweets_ny = pd.read_csv('ny_tweets.csv', )
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

#%% Append distributions
def add_dist(zipcode, num):
    if zipcode > 11979 or zipcode < 6001:
        return 0
    dist = zip_to_dist[zipcode][num]
    return dist

def add_none(flag):
    return flag
    
tweets_ny["affected"] = tweets_ny.apply(lambda row: add_dist(row['zipcode'], 0), axis=1)
tweets_ny["minor"] = tweets_ny.apply(lambda row: add_dist(row['zipcode'], 1), axis=1)
tweets_ny["major"] = tweets_ny.apply(lambda row: add_dist(row['zipcode'], 2), axis=1)
tweets_ny["destroyed"] = tweets_ny.apply(lambda row: add_dist(row['zipcode'], 3), axis=1)
tweets_ny = tweets_ny.fillna(0)
tweets_ny["unknown"] = tweets_ny.apply(lambda row: add_none(1-(row['affected'] + row['minor'] + row['major'] + row['destroyed'])), axis=1)

#%%
tweets_ny.to_csv('tweets_ny_dist.csv')

    
