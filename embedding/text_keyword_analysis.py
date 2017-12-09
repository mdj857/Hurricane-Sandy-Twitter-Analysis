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

#tweets = pd.read_csv('/Users/mattjohnson/Desktop/Term_Project/tweets.csv')

tweets = pd.read_csv('/Users/mattjohnson/Desktop/Term_Project/ny_tweets_short.csv')
#with open('/Users/mattjohnson/Desktop/Term_Project/tweets/affected_tweets_clean.pkl', 'rb') as f:
     #tweets = pickle.load(f)
#%%

# referenced https://radimrehurek.com/gensim/tut1.html
# removing common words, tokenizing 
stoplist = set('for a of the and to in are eediting. i rt : my is this'.split())
texts = [[word for word in tweet.lower().split() if word not in stoplist]
            for tweet in tweets['text']]

# remove words that appear only once
from collections import defaultdict 
frequency = defaultdict(int)
for text in texts:
     for token in text:
         frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
          for text in texts]
#%%

# bag-of-words approach with frequency as the embedded feature 
dictionary = corpora.Dictionary(texts)
dictionary.save("short_tweets.dict")

# creating corpus
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('short_corpus.mm', corpus)  # store to disk, for l
    
# train tfidf model on the corpus
# https://en.wikipedia.org/wiki/Tf%E2%80%93idf
tfidf = models.TfidfModel(corpus)

#apply transformation to tfidf vector space 
tfidf_corpus = tfidf[corpus]
corpora.MmCorpus.serialize('tfidf_short_corpus.mm', tfidf_corpus)  # store to disk, for l
    

    
# Latent Semantic Indexing 
# convert to latent space in R^2
lsi = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=300)
lsi_corpus = lsi[tfidf_corpus]
corpora.MmCorpus.serialize('lsi_short_corpus.mm', lsi_corpus)  # store to disk, for l

