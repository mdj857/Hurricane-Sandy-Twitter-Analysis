# corpus_gen.py
# generates the corpus files from csv input.
# feed this models already trained and stored in corpus_dir.

import pickle
import pandas as pd 
from matplotlib import pyplot as plt 
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora, models, similarities 
from collections import defaultdict

import logging
logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

import sys
if len(sys.argv) < 3:
    print "usage: %s <test.csv> <corpus_dir>"
    exit(-1)

## Generate the text pickle
# IMPORTANT: corroborate this transform with corpus.py
# removing common words, tokenizing 
corpus_dir = sys.argv[2] + "/"
tweets = pd.read_csv(sys.argv[1], encoding="utf-8")
stoplist = set('a an and are as at be by for from has he i in is it its of on that the to u was were will with rt eediting my this'.split())
stopchars = "();"
# print tweets.iloc[0, :]["text"].encode("utf-8").translate(None, stopchars).lower().split()
texts = [[word for word in tweet.encode("utf-8").translate(None, stopchars).lower().split() if word not in stoplist]
            for tweet in tweets['text']]

# load models and prepare corpus.
dictionary = corpora.Dictionary.load(corpus_dir + "tweets.dict")
tfidf = models.TfidfModel.load(corpus_dir + "tfidf.model")
lsi = models.LsiModel.load(corpus_dir + "lsi.model")
corpus = [dictionary.doc2bow(text) for text in texts]

# transform and save
tfidf_corpus = tfidf[corpus]
lsi_corpus = lsi[tfidf_corpus]
corpora.MmCorpus.serialize(corpus_dir + "tfidf_corpus.mm", tfidf_corpus)
corpora.MmCorpus.serialize(corpus_dir + "lsi_corpus.mm", lsi_corpus)  # store to disk
