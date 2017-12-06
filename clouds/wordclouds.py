import pickle
import numpy 
import pandas as pd 
from matplotlib import pyplot as plt 
from wordcloud import WordCloud

with open('/Users/mattjohnson/Desktop/Term_Project/tweets/affected_tweets_clean.pkl', 'rb') as f:
	affected_tweets = pickle.load(f)

with open('/Users/mattjohnson/Desktop/Term_Project/tweets/minor_tweets_clean.pkl', 'rb') as f:
	minor_tweets = pickle.load(f)

with open('/Users/mattjohnson/Desktop/Term_Project/tweets/major_tweets_clean.pkl', 'rb') as f:
	major_tweets = pickle.load(f)

with open('/Users/mattjohnson/Desktop/Term_Project/tweets/destroyed_tweets_clean.pkl', 'rb') as f:
	destroyed_tweets = pickle.load(f)

# plots word cloud
# package: https://github.com/amueller/word_cloud
def plot_word_cloud(list_of_tweets, file_name):
    wordcloud = WordCloud().generate(''.join(list_of_tweets))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(file_name)
    plt.show()



plot_word_cloud(affected_tweets, '/Users/mattjohnson/Desktop/Term_Project/affected_wordcloud.png')

plot_word_cloud(minor_tweets, '/Users/mattjohnson/Desktop/Term_Project/minor_wordcloud.png' )

plot_word_cloud(major_tweets, '/Users/mattjohnson/Desktop/Term_Project/major_wordcloud.png')

plot_word_cloud(destroyed_tweets, '/Users/mattjohnson/Desktop/Term_Project/destroyed_wordcloud.png')