#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities 
import numpy as np
import pandas as pd
import keras
from keras.models import Sequential 
from keras.layers import Dense, Dropout, Activation, Flatten, LSTM
import itertools

import logging
logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

def batch_generator(train_path, size=60000, compression=None):
    train_chunks = pd.read_csv(train_path, encoding="utf-8", chunksize=size, compression=compression)
    for chunk in train_chunks:
        # drop certains columns
        columns = ["damage", "text", "lat_final", "lng_final", "created_at", "time_min", "topsy_doc_sentiment"]
        chunk = chunk.drop(columns, axis=1)
        chunk_y = pd.DataFrame()
        chunk_y["affected"] = chunk["affected"]
        chunk_y["minor"] = chunk["minor"]
        chunk_y["major"] = chunk["major"]
        chunk_y["destroyed"] = chunk["destroyed"]
        chunk_y["unknown"] = chunk["unknown"]
        yield (chunk, chunk_y)

def chunks(iterable, size):
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))


# batch generation
batch_size = 512
#batch_gen = batch_generator("corpus/topic_frame.csv.gz", size=batch_size, compression="gzip")
batch_gen = batch_generator("corpus/1train_topic_with_onehot_label.csv.gz", size=batch_size, compression="gzip")

# compile keras model
model = Sequential()
model.add(Dense(200, input_shape=(213,), activation='relu'))
model.add(Dropout(.5))
model.add(Dense(100, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(5, activation='softmax'))

model.compile(loss='binary_crossentropy', 
              optimizer = 'adam', 
              metrics = ['accuracy'])

model.fit_generator(batch_gen, steps_per_epoch=300, epochs=10, verbose=1, shuffle=True)
