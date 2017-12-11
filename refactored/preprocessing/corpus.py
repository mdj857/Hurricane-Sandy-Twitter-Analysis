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
from optparse import OptionParser

import logging
logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

## Generate the text pickle
# referenced https://radimrehurek.com/gensim/tut1.html
# removing common words, tokenizing 
corpus_dir = "short/"
tweets = pd.read_csv(corpus_dir + "train.csv", encoding="utf-8")
stoplist = set('a an and are as at be by for from has he i in is it its of on that the to u was were will with rt eediting my this'.split())
stopchars = "();"
# print tweets.iloc[0, :]["text"].encode("utf-8").translate(None, stopchars).lower().split()
texts = [[word for word in tweet.encode("utf-8").translate(None, stopchars).lower().split() if word not in stoplist]
            for tweet in tweets['text']]

# remove words that appear only once
from collections import defaultdict 
frequency = defaultdict(int)
for text in texts:
     for token in text:
         frequency[token] += 1

pickle.dump(texts, open(corpus_dir + "texts.pkl", "wb"))

## Generate the dictionary
# bag-of-words approach with frequency as the embedded feature 
texts = pickle.load(open(corpus_dir + "texts.pkl", "rb"))
dictionary = corpora.Dictionary(texts)
dictionary.filter_extremes(no_below=20)
dictionary.save(corpus_dir + "tweets.dict")

## Generate Basic training corpus
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize(corpus_dir + "corpus.mm", corpus)  # store to disk
 
## TFIDF Transform
# https://en.wikipedia.org/wiki/Tf%E2%80%93idf
dictionary = corpora.Dictionary.load(corpus_dir + "tweets.dict")
corpus = corpora.MmCorpus(corpus_dir + "corpus.mm")
tfidf = models.TfidfModel(corpus)
tfidf.save(corpus_dir + "tfidf.model")
tfidf_corpus = tfidf[corpus]
corpora.MmCorpus.serialize(corpus_dir + "tfidf_corpus.mm", tfidf_corpus)  # store to disk

## Latent Semantic Indexing Transform
# convert to latent space in R^200
dictionary = corpora.Dictionary.load(corpus_dir + "tweets.dict")
tfidf_corpus = corpora.MmCorpus(corpus_dir + "tfidf_corpus.mm")
lsi = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=200)
lsi.save(corpus_dir + "lsi.model")
lsi_corpus = lsi[tfidf_corpus]
corpora.MmCorpus.serialize(corpus_dir + "lsi_corpus.mm", lsi_corpus)  # store to disk
