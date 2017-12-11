# merge.py:
# merges the tweets csv and very large lsi_corpus (10GB+)
# creates a new topic frame csv.
# (1.8M, 15) . (1.8M, 200) -> (1.8M, 215)

from gensim import corpora, models, similarities 
import numpy as np
import pandas as pd
import itertools
import os

import logging
logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

def tweets_generator(train_path, corpus_path):
    train = pd.read_csv(train_path, encoding="utf-8")
    lsi_corpus = corpora.MmCorpus(corpus_path)
    for (train_elem, lsi_elem) in itertools.izip(train.iterrows(), lsi_corpus):
        if lsi_elem: # valid topic vector
            topics = pd.Series([elem[1] for elem in lsi_elem])
            topics.rename(lambda k: "topic" + str(k), inplace=True)
            yield pd.concat([train_elem[1], topics])

def chunks(iterable, size):
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))

train_path = "corpus/train.csv"
corpus_path = "corpus/lsi_corpus.mm"
frame_path = "corpus/topic_frame.csv"
tweets_gen = tweets_generator(train_path, corpus_path)
chunk, chunk_size = (0, 5000)
for tweets in chunks(tweets_gen, chunk_size):
    topic_frame = pd.DataFrame([tweet for tweet in tweets if tweet is not None])
    # raw_input("press any key to continue...")
    topic_frame.to_csv(frame_path, encoding="utf-8", header=(not os.path.exists(frame_path)), index=False, mode='a')
    del topic_frame
    chunk += chunk_size
    print "written(%d): " % chunk
