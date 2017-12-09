import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar, time, re, datetime
from time import mktime

#%% Read Tweets

big_tweets = pd.read_csv('./ny_tweets.csv', chunksize = 100)

#%%
def add_unix_col(tweets_df):
    tweets_df["time"] = pd.Series(index=tweets_df.index)
    for index, tweet in tweets_df.iterrows():
        str_time = tweet['created_at']
        if str_time == None:
            tweets_df["time"][index] = np.NaN
            continue
        tweet_time = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        u_time = calendar.timegm(time.struct_time(tweet_time))
        tweets_df["time"][index] = u_time - 60*60*-5
    return tweets_df


#%%
chunk_count = 1
for chunk in big_tweets:
           
    # Preprocess tweets
    chunk.fillna(value=0)
    chunk = chunk[chunk['zipcode'] != 0]
    chunk_processed = add_unix_col(chunk)
    chunk_processed.to_csv('./ny_tweets_times/big_tweets_processed_' + str(chunk_count))
    chunk_count = chunk_count + 1


#%% Display hist

plt.hist(big_tweets_processed["time"], bins=100 )
plt.yscale('log', nonposy='clip')
plt.xlabel("unix time")
plt.ylabel("frequency")
plt.title("big_tweets_processed time distribution")

#%% Returns 24 bins with number of tweets in each timeframe

def get_hourly_rates(tweets, start_time):
    hours = np.empty((0,))
    for hour in range(0, 23):
        tweets_in_range = tweets[tweets["time"] >= start_time + hour * 60 * 60]
        tweets_in_range = tweets_in_range[tweets_in_range["time"] < start_time + ((hour+1) * 60 * 60)]
        hours = np.concatenate((hours, [tweets_in_range.shape[0]]), axis=0)
    return hours

#%% Find Rates

# before sandy rates
timezone = -5 # EST
hourly_average = np.ndarray(shape=(23,))
for day in range(15, 28):
    start_time = datetime.datetime(2012, 10, day, 0 - timezone)
    hour_rates = get_hourly_rates(big_tweets_processed.copy(), mktime(start_time.timetuple()))
    hourly_average = hourly_average + hour_rates
hourly_average = hourly_average / (28-15)
    
    
    
#%%
big_tweets_processed_prior = big_tweets_processed[big_tweets_processed["time"] < 1351468800]
big_tweets_processed_mean = big_tweets_processed["time"].mean()
big_tweets_processed_prior_mean = big_tweets_processed_prior["time"].mean()

#%%

#big_tweets_processed.to_csv('big_tweets_processed')
