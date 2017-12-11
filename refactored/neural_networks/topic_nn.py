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
        columns = [
            "created_at", "lat_final", "lng_final", "retweeted_status_id", "text", 
            "time_min", "topsy_doc_sentiment", "topsy_doc_sentiment_abs", "topsy_doc_sentiment_rel",
            "tweet_id", "user_followers_count", "user_friends_count", "user_id", "zipcode", "damage"
        ]
        damages = ["unknown", "affected", "minor", "major", "destroyed"]
        yield (chunk.drop(columns, axis=1), pd.get_dummies(chunk["damage"]).T.reindex(damages).T.fillna(0))

def chunks(iterable, size):
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))


# batch generation
batch_size = 512
# batch_gen = batch_generator("corpus/1train_topic_with_onehot_label.csv.gz", size=batch_size, compression="gzip")
train_gen = batch_generator("corpus/topic_clean.csv.gz", size=batch_size, compression="gzip")
test_gen = batch_generator("test_corpus/topic_clean.csv.gz", size=batch_size, compression="gzip")

# for chunk in batch_gen:
#     print chunk
#     raw_input("press any key to continue...")

# compile keras model
model = Sequential()
model.add(Dense(200, input_shape=(200,), activation='relu'))
model.add(Dropout(.5))
model.add(Dense(100, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(50, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(5, activation='softmax'))

model.compile(loss='binary_crossentropy', 
              optimizer = 'adam', 
              metrics = ['accuracy'])

history = model.fit_generator(train_gen, steps_per_epoch=500, epochs=2, verbose=1, shuffle=True)
model.save("models/topic_nn.h5")
print model.metrics_names
print model.evaluate_generator(test_gen, steps=300)

import matplotlib.pyplot as plt
plt.plot(history.history['acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('plots/topic_history.jpg')
plt.close()

