#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 23:50:06 2017

@author: mattjohnson
"""

import pandas as pd 
import numpy as np 
tweets = pd.read_csv('train_short.csv')
import keras 
import keras.preprocessing.text as kpt
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')
#%%

print tweets.head

tweets = pd.concat([tweets, pd.get_dummies(tweets['damage'])], ignore_index = False, axis=1 )
#%%

tweets.drop(['damage'], axis =1, inplace=True)


X = tweets['text']
Y = tweets.iloc[:, len(tweets.columns)-5:len(tweets.columns)]


#%%
# will only work with top 1000 words in our tweets 
max_words = 1000

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(X)

dictionary = tokenizer.word_index
#%% 

def convert_text_to_idx_array(text):
    return [dictionary[word] for word in kpt.text_to_word_sequence(text)]

all_word_idx = []

for tweet in X:
    word_idxs = convert_text_to_idx_array(tweet)
    all_word_idx.append(word_idxs)
    
#%%

# now we have a list of all tweets converted to index arrays
all_word_idx = np.asarray(all_word_idx)
#%%
#create a one-hot matrix out of indexed tweets
X = tokenizer.sequences_to_matrix(all_word_idx)
print X.shape
print Y.shape
model = Sequential()
model.add(Dense(512, input_shape=(1000,), activation='relu'))
model.add(Dropout(.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(16, activation='relu'))
model.add(Dropout(.5))
for _ in range(20):
    model.add(Dense(5, activation='relu')) 
    model.add(Dropout(5))

model.add(Dense(5, activation='softmax'))

#%%

model.compile(loss='categorical_crossentropy', 
              optimizer = 'adam', 
              metrics = ['accuracy'])

#%%

history = model.fit(X, Y, batch_size =32, epochs=3, verbose=1, validation_split=.1, shuffle=True)

fig = plt.figure()

plt.subplot(211)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.tight_layout()
#plt.show()

# summarize history for loss
plt.subplot(212)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.tight_layout()
plt.savefig('plot_history.jpeg')
plt.close(fig)


