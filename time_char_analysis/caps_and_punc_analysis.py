import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import mktime

#%% Read Tweets

big_tweets = pd.read_csv('./zip.csv.00', nrows=10**7)
big_tweets_processed = pd.read_csv('./big_tweets_processed')

#%% Preprocess tweets

big_tweets.fillna(value=0)
big_tweets = big_tweets[big_tweets['zipcode'] != 0]
big_tweets_selected = big_tweets[big_tweets['zipcode'] >= 99500]
big_tweets_selected = big_tweets_selected[big_tweets_selected['zipcode'] < 99999]

#%% Funcs
def count_caps(tweets_df):
    tweets_df["caps"] = pd.Series(index=tweets_df.index)
    for index, tweet in tweets_df.iterrows():
        tweets_df["caps"][index] = sum(1 for c in tweet["text"] if c.isupper())
    return tweets_df

def count_char(tweets_df, char):
    tweets_df[char] = pd.Series(index=tweets_df.index)
    for index, tweet in tweets_df.iterrows():
        tweets_df[char][index] = sum(1 for c in tweet["text"] if c == char)
    return tweets_df

#%% Tests

big_tweets_selected = count_char(big_tweets_selected, "!")