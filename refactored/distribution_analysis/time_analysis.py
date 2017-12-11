import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar, time, re, datetime
from time import mktime
import pickle

#%% Read Tweets
big_tweets = pd.read_csv('./tweets_ny_dist.csv')

#%% Preprocess tweets

big_tweets.fillna(value=0)
big_tweets = big_tweets[big_tweets['zipcode'] != 0]

#%% Unix time function

def add_unix_col(str_time):
    if str_time == None:
        return 0
    tweet_time = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    u_time = calendar.timegm(time.struct_time(tweet_time))
    return u_time

big_tweets["time"] = big_tweets.apply(lambda row: add_unix_col(row["created_at"]), axis=1)
big_tweets.to_csv('tweets_ny_dist.csv')

#%% big tweets unix time
big_tweets = add_unix_col(big_tweets)

#%% Display hist

plt.hist(big_tweets["time"], bins=1000 )
plt.yscale('log', nonposy='clip')
plt.xlabel("unix time")
plt.ylabel("frequency")
plt.title("Time distribution")

#%% Returns 24 bins with number of tweets in each timeframe

def get_hourly_rates(tweets, start_time):
    hours = np.empty((0,))
    for hour in range(0, 23):
        tweets_in_range = tweets[tweets["time"] >= start_time + hour * 60 * 60]
        tweets_in_range = tweets_in_range[tweets_in_range["time"] < start_time + ((hour+1) * 60 * 60)]
        hours = np.concatenate((hours, [tweets_in_range.shape[0]]), axis=0)
    return hours

#%% new york hourly tweet rates
hours_nyc = pd.DataFrame([])
for zipcode in range(6001, 11980):
    zip_range = big_tweets[big_tweets["zipcode"] == zipcode]
    hours_nyc[zipcode] = get_hourly_rates(zip_range, 1351550000)
    hours_nyc[zipcode] = hours_nyc[zipcode] / sum(hours_nyc[zipcode])
    if np.isnan(hours_nyc.loc[0, zipcode]):
        hours_nyc = hours_nyc.drop(zipcode, axis=1)

#%% 

for col in range(6001, 11980):
    if col in hours_nyc.columns:
       plt.plot(hours_nyc.ix[:, col])
       plt.hold(True)
plt.xlabel('hour')
plt.ylabel('frequency')
plt.title('distributions by zipcode')
plt.show()
