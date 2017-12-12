
# coding: utf-8

# In[218]:

# Matthew Johnson 
# 2 December 2017
import numpy as np 
import pandas as pd 
import seaborn as sns
from matplotlib import pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import pickle 


# In[233]:

tweet_chunks = pd.read_csv('clean_zip.csv', encoding='utf-8', engine='c', chunksize=3000)
damage_data = pd.read_csv('determination_zip.csv')

# In[216]:
# word cloud data structures
affected_tweets, destroyed_tweets = [], []
minor_tweets, major_tweets = [], []

# This function takes a list of zipcodes of the locations (including duplicates) and 
# the top 'num_zips' most frequently occuring zipcodes and returns all tweets from those zipcodes 
def get_tweets_from_zipcode(damage_zip, num_zips): 
    top_zips = damage_zip.value_counts().head(num_zips).index
    return tweet_data[tweet_data["zip_codes"].isin(top_zips)]["text"]

for tweet_data in tweet_chunks:
    

    print "processing chunk. size: ", len(tweet_data)
    affected_zips = damage_data[damage_data["Affected"] == 1]["zip_codes"]
    minor_zips = damage_data[damage_data["Minor"] == 1]["zip_codes"]
    major_zips = damage_data[damage_data["Major"] == 1]["zip_codes"]
    destroyed_zips = damage_data[damage_data["Destroyed"] == 1]["zip_codes"]
    # no_damage_zips = damage_data[damage_data["No Damage"] == 1]["zip_codes"]

    print "commiting..."
    affected_tweets.extend(get_tweets_from_zipcode(affected_zips, 100))
    minor_tweets.extend(get_tweets_from_zipcode(minor_zips, 100))
    major_tweets.extend(get_tweets_from_zipcode(major_zips, 100))
    destroyed_tweets.extend(get_tweets_from_zipcode(destroyed_zips, 100))

    print "finished commit."



pickle.dump(affected_tweets, open("clouds/affected_tweets.pkl", "wb"))
pickle.dump(minor_tweets, open("clouds/minor_tweets.pkl", "wb"))
pickle.dump(major_tweets, open("clouds/major_tweets.pkl", "wb"))
pickle.dump(destroyed_tweets, open("clouds/destroyed_tweets.pkl", "wb"))
# pickle.dump(no_damage_tweets, open("clouds/destroyed_tweets.pkl", "wb"))

print "affected tweets: ", affected_tweets
print "minor tweets: ", minor_tweets
print "major tweets: ", major_tweets
print "destroyed tweets: ", destroyed_tweets

# plots word cloud
# package: https://github.com/amueller/word_cloud
def plot_word_cloud(list_of_tweets):
    wordcloud = WordCloud().generate(''.join(list_of_tweets))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()



plot_word_cloud(affected_tweets)

plot_word_cloud(minor_tweets)

plot_word_cloud(major_tweets)

plot_word_cloud(destroyed_tweets)

