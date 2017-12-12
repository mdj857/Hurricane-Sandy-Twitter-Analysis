#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 14:56:56 2017

@author: mattjohnson
"""

import pickle
import numpy 
import pandas as pd 
from matplotlib import pyplot as plt 
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora, models, similarities 
from collections import defaultdict

with open('/Users/mattjohnson/Desktop/Term_Project/tweets/affected_tweets_clean.pkl', 'rb') as f:
	affected_tweets = pickle.load(f)

with open('/Users/mattjohnson/Desktop/Term_Project/tweets/minor_tweets_clean.pkl', 'rb') as f:
	minor_tweets = pickle.load(f)

with open('/Users/mattjohnson/Desktop/Term_Project/tweets/major_tweets_clean.pkl', 'rb') as f:
	major_tweets = pickle.load(f)

with open('/Users/mattjohnson/Desktop/Term_Project/tweets/destroyed_tweets_clean.pkl', 'rb') as f:
	destroyed_tweets = pickle.load(f)

affected_tweets = [tweet.encode('utf-8') for tweet in affected_tweets]
#%%
# http://rohankshir.github.io/2015/10/30/analyzing-twitter-part-2/
#vectorizer = TfidfVectorizer()
#vectorizer.fit_transform(affected_tweets_str)
#idf = vectorizer.idf_
#term_score = zip(vectorizer.get_feature_names(), idf)
#term_score = sorted(term_score, key = lambda tup:(-tup[1], tup[0]))
#print term_score[500]

#%%

# referenced https://radimrehurek.com/gensim/tut1.html
# removing common words, tokenizing 
stoplist = set('for a of the and to in are eediting. i rt : my is this'.split())
texts = [[word for word in tweet.lower().split() if word not in stoplist]
            for tweet in affected_tweets]

# remove words that appear only once
from collections import defaultdict 
frequency = defaultdict(int)
for text in texts:
     for token in text:
         frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
          for text in texts]

# print 
#%%

# bag-of-words approach with frequency as the embedded feature 
dictionary = corpora.Dictionary(texts)

# creating corpus
corpus = [dictionary.doc2bow(text) for text in texts]

# train tfidf model on the corpus
# https://en.wikipedia.org/wiki/Tf%E2%80%93idf
tfidf = models.TfidfModel(corpus)

#apply transformation to tfidf vector space 
corpus_tfidf = tfidf[corpus]

# Latent Semantic Indexing 
# convert to latent space in R^2
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=3)
corpus_lsi = lsi[corpus_tfidf]
#%%
lsi.print_topics(3)
'''
yields: 
    [(0, u'0.366*"power" + 0.221*"no" + 0.200*"on" + 0.199*"still" + 0.198*"have" + 0.186*"hurricane" + 0.161*"you" + 0.151*"out" + 0.147*"gas" + 0.137*"got"'), 
    (1, u'-0.410*"insurance" + -0.382*"fema" + -0.324*"damage." + -0.300*"call." + -0.295*"ready" + -0.238*"-825-1038" + -0.179*"on" + -0.164*"hand." + -0.161*"contact.com" + -0.156*"crew"')]

We can see that when we project the tweets into R^2 space, the most 
important characteristics of the first element of the vector stems
from whether or not the tweet mentions power. 

Curiously, the second element gets the vast majority of its collective 
'information' from whether or not the tweet contains mentions of 
'damage', 'insurance', or 'FEMA' 

''' 
#%%
#index the corpus
gas_tweet = "Out of gas"
gas_tweet_vec = dictionary.doc2bow(gas_tweet.lower().split())
gas_tweet_vec = lsi[gas_tweet_vec]
index = similarities.MatrixSimilarity(corpus_lsi)

similarities = index[gas_tweet_vec] # list of tuples in form of (docnumber, sim_score) 
similarities = sorted(enumerate(similarities), key = lambda item: -item[1])
print type(index)