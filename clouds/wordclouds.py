import pickle
import numpy 
import pandas as pd 
from matplotlib import pyplot as plt 
from wordcloud import WordCloud

with open('/Users/mattjohnson/Desktop/Lab_Term_Project/clouds/affected_tweets.pkl', 'rb') as f:
	affected_tweets = pickle.load(f)

with open('/Users/mattjohnson/Desktop/Lab_Term_Project/clouds/minor_tweets.pkl', 'rb') as f:
	minor_tweets = pickle.load(f)

with open('/Users/mattjohnson/Desktop/Lab_Term_Project/clouds/major_tweets.pkl', 'rb') as f:
	major_tweets = pickle.load(f)

with open('/Users/mattjohnson/Desktop/Lab_Term_Project/clouds/destroyed_tweets.pkl', 'rb') as f:
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



plot_word_cloud(affected_tweets, 'affected_wordcloud.png')

plot_word_cloud(minor_tweets, 'minor_wordcloud.png' )

plot_word_cloud(major_tweets, 'major_wordcloud.png')

plot_word_cloud(destroyed_tweets, 'destroyed_wordcloud.png')