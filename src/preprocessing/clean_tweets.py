# This script calls the preprocessing library on a tweets csv

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 12:39:40 2017

@author: mattjohnson
"""
import numpy as np 
import pandas as pd 
import seaborn as sns
import time
import os
import sys
import preprocessor as p
import pickle

if len(sys.argv) < 2:
    print "usage: clean_tweets.py <input_tweets.pkl> <output_tweets.pk1>"
    exit(1)
    
with open(sys.argv[1], 'rb') as f:
	dirty_tweets = pickle.load(f)

dirty_tweets_str = [tweet.encode('utf-8') for tweet in dirty_tweets]
clean_tweets = [p.clean(tweet) for tweet in dirty_tweets_str]

pickle.dump(clean_tweets, open("../../tweets/" + sys.argv[2], "wb"))

