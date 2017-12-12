## *What if 140 characters could save lives?* 

Matthew Johnson

Javier Zepeda 

Ronald MacMaster 

Matthew Edwards

## Motivation

The 2017 Atlantic hurricane season was one of the most active hurricane seasons in over a decade. Not since the mid-2000s had the Atlantic churned out hurricanes with such frequency and intensity. Hurricanes Harvey, Irma, and Maria ravaged through large swaths of the southeast United States and Puerto Rico, causing significant spikes in buzz on Twitter in the process. The presence of a vast wealth of textual and geographical information available on Twitter coupled with the spikes in social media buzz during the events provided the basis for a very fundamental question: given a tweet from the areas affected during Hurricane Sandy, is it possible to predict the level of damage for that specific area?


## The Datasets

To answer our question, we turned our attention to one of the most significant meteorological events in recent memory: Hurricane Sandy. 

As it turns out, there was no lack of tweets about Hurricane Sandy. For our project, we analyzed 47 million publicly available tweets with the hashtag “#sandy” or containing some other keyword deemed relevant to the storm and its aftermath [1]. 

For our damage analysis, we used data from FEMA’s post-disaster survey of 300,000 affected buildings in the tri-state area [2]. As part of their survey, FEMA labeled buildings as affected, minor damage, major damage, or destroyed. A summary of our datasets and the damage classification rule is shown below. 

#### The Datasets

| | Tweet Dataset | FEMA Damage Dataset |
| ---- | ------- | ----- |
| Number of Samples | 47 million tweets (11 GB)  | 300k buildings (375 MB)  |
| Description | Tweets collected from 10/15/12 to 11/12/12 containing hashtag "#sandy" or related keywords | Collection of damage reports for buildings after Hurricane Sandy |
| Number of Features | 13 | 20 |
| Important Features | time_created, num_followers, latitude, longitude, text_of_tweet | latitude, longitude, damage_level, damage_type |


#### FEMA Damage Classification

| Damage Level | Description |
| ------------ | ----------- |
| Affected | Generally superficial damage to solid structures (loss of tiles or roof shingles); some mobile homes and light structures damaged or displaced. |
| Minor | Solid structures sustain exterior damage (e.g., missing roofs or roof segments); some mobile homes and light structures are destroyed, many are damaged or displaced. |
| Major | Some solid structures are destroyed; most sustain exterior and interior damage (roofs missing, interior walls exposed); most mobile homes and light structures are destroyed. Extensive structural damage from storm surge. |
| Destroyed | Most solid and all light or mobile home structures destroyed. Structure has been completely destroyed or washed away from storm surge. |

###### Adapted from https://data.femadata.com/MOTF/Hurricane_Sandy/FEMA%20MOTF-Hurricane%20Sandy%20Products%20ReadME%20FINAL.pdf

## Our Design Overview

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/block_diagram.png "Block Diagram")

## Preprocessing

After we found our two datasets, we needed to combine them so that we could perform predictive analysis. The following subsections describe our methods cross-referencing our data; we ultimately wanted each geo-tagged tweet in the USA to have a damage level associated with it.

### Removing tweets
The original dataset contains 47 million tweets. First, we removed tweets which had no location data and tweets which came from outside the United States using the _uszipcode_ Python package. Next, we removed all tweets which came from outside the tri-state area. This yielded around 2 million tweets for our "clean" dataset.

### Zip codes and damage classification
First, we determined the zip code each tweet was from by examining the latitude and longitude of each tweet. Next, examined the FEMA dataset and looked at the types of damaged buildings by zip code. We categorized the damage level of each tweet by the worst damaged building in the zip code that tweet originated from. For example, if a tweet comes from a zip code with 6 affected buildings, 2 buildings labeled with minor damage, and 1 building labeled as destroyed, then that tweet is classified as destroyed (because of the single destroyed building). We chose this method of classification because we believe that it is more prudent to overestimate damage in a disaster scenario.

### Text cleanup
We removed common words like articles and prepositions and words that only appeared once in our dataset. We also set all of the text to lower case. This helped to eliminate some of the textual noise present in our dataset.

## Map Visualization

Before we began creating any models, we tried to get a better understanding of our data. Below is an image of Plotly visualization tool that we created, which shows our tweets on a map. Because of computational constraints, only 20,000 tweets are plotted. Access the interactive Plotly map [here](https://plot.ly/~javiertzepeda/0.embed) (You might have to zoom in a little to get a better look). 

Each tweet marker’s color represents its respective damage classification: pink for affected, yellow for minor, orange for major, and red for destroyed. The radius of the marker represents the number of followers of the tweet’s author, and hovering over a marker shows the tweet text and damage level.

We noticed a high level damage around the coast, with lower levels of damage further inland.  Try discovering for yourself if you notice any relationships among the tweets, location, and damage classification. There’s some rather interesting and *colorful* tweets that we found very entertaining.


![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/map_tool.png "Map Visualizer")

## Word Cloud Visualization

Another powerful tool that we used to analyze our data were word clouds, which we generated with the library [here]( https://github.com/amueller/word_cloud). Each word cloud shows a visual representation of the text data for each damage classification. Words are weighted such that larger words are more frequent in that classification of the data set.

We noticed that the destroyed word cloud had a large “power” text, indicating that those in destroyed areas were most likely without power (and were tweeting about it!). What patterns do you see?

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/word_clouds.png "Word Clouds")

## Time Series Exploration

We thought that there might be predictive information in the distribution of the tweets by zip code. We observed that the dataset had many more tweets during the time when the most affected regions were under Hurricane Sandy. The image below on the left is the distribution of tweets for each zip code between October 29th 2012 at 6pm EST and October 30th 2012 at 6pm EST. The image below on the right is the distribution of tweets between October 15th 2012 and November 15th 2012. 

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/time_series_1.png "Time Series 1")

We tried to predict the distribution of buildings damaged by FEMA using the distribution of tweets by hour as features. We were unsuccessful in making this prediction, as predicting all zeros resulted in a better mean absolute error score except for the "unknown" category. We used the XGBoost Regressor to make our predictions. Below is the results of our regression.

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/regression_pic.png "Time Series 2")

Next, we tried to classify the presence of damaged buildings by zip code using the same frequency information. If a zip code had a building classified in a certain category, we classed that as true in our prediction. Note that we classified the tweets differently here than we do in our analysis of the tweet text. The below plots are the ROC scores for each of the five categories. We used the XGBoost Classifier to make our predictions.

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/time_series_3.png "Time Series 3")

## Tweets as Embedded Vectors

In order to make meaning out of our tweets, we sought the help of the Doc2Vec library, a close relative of the popular Word2Vec API. Essentially, Doc2Vec converts sentences (in our case, tweets) into vectors. In order to do this, our dataset was converted into a matrix _D_, where each row denotes of tokens in the dataset and each column denotes a tweet. Each element _D<sub>ij</sub>_ consists of some value to indicate the presence of token _i_ in sentence _j_ [3]. An example illustration of the Doc2Vec framework is shown below: 

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/doc2vec.png "Doc2vec Illustration")

There are a couple of advantages to the Doc2Vec approach. The first is that the semantic relationships between words are preserved; the euclidean distance between the vectorized words encapsulates the semantics behind the words themselves. Second, including a term-document matrix in the encoding preserves the ordering of sentences themselves. For example, _I walked the dog_ is a drastically different from _The dog walked I_. Including _D_ in a sentence encoding allows for the inclusion of both semantic and ordinal information in a sentence [3]. 

Naturally, there are many ways to encode _D_. Here are three: 

**Bag of words:** This is the simplest encoding. _D<sub>ij</sub>_ simply contains the number of times the word _i_ occurs in document _j_. Naturally, this skews the embedding towards words that appear more frequently. Additionally, this encoding can create very large and sparse vectors for large datasets. Each tweet would be defined as a vector with size equal to the number of unique words in the entire dataset!

**Term-Frequency-Inverse-Document-Frequency (tf-idf):** In essence, tf-idf is identical to the bag-of-words approach but with a key difference. _D<sub>ij</sub>_ still contains the frequency of the word _i_ in document _j_, but normalized over the number of times _i_ appears in the entire set of documents (all of the columns of _D_). However, the vectors are still rather large. When transforming our tweets, they were each represented as a vector of size ~40,000.

**Latent Semantic Indexing (LSI):** Because _D_ might become pretty large when working with large sets of text (like our tweets!), it’d be pretty useful to have a _low-rank_ _approximation_ of _D_. A _low-rank_ _approximation_ is representation of something where you remove non-essential information. This process is used frequently in image compression. Latent Semantic Indexing is exactly a low-rank approximation of the term-document matrix _D_ encoded with tf-idf (detailed above)! As it turns out, this encoding was pretty useful to feed into machine learning models, as it reduced the size of each tweet vector to size 200.

After we've constructed dense vector representations of tweet text, we were able to easily feed these vectors into a machine learning model.

## A first attempt: A simple model with Keras tweet embedding

For our first model, we elected to use a simple tokenizer API native to Keras to embed the tweets as vectors. Essentially, the tokenizer yielded a one-hot-encoded 1.8 million tweet x 1000 token matrix (only including the top 1000 most frequently occuring tokens). This was very similar to the bag of words approach described above. Then, we fed the encoded matrix into a simple sequential neural network with three hidden layers, scaling down the size of the input roughly in half at each stage. Below is a graphic displaying the simple model's architecture. 

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/simple_model.png "Simple Model Architecture")

## A second attempt: A custom deep network with custom tweet embedding

The deep network's input layer receives a 200-dimensional topic vector from a latent semantic index (LSI) embedding described above. The early hidden layers reduce the previous layer size by half until reaching a size of 10. Next, the deep layers learn complex nonlinear relationships between the earlier learned hidden features. There are 20 deep hidden layers, each of size 10. All of the hidden layers use a ReLU activation function. The output layer of the network outputs a classification probability for each of the five categories with a softmax activation function. 

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/model_architecture.png "Model Architecture")

## Empirical Results

So... what does all of this mean? 

Using our simple model with the default Keras tweet embedding, we achieved a 71% validation accuracy which is only slightly better than classifying based on the frequency of classifications in the data (just classifying all tweets as "unknown"). 

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/simple_results.png "Simple BOW Network Results")

Fortunately, our custom embedding and complex network architecture paid off! We were able to reach a validation accuracy of 88%--much better than our previous model. Our deep learning model was able to learn the nonlinear relationships between the LSI-embedded tweets and their respective damage classifications pretty well!

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/empirical_results.png "Deep Topics Network Results")


## Contact Us

Have questions? Comments? Please feel free to contact us or check out our Github repository for this project. 

[https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis)

mjohnson082396 at utexas.edu

javier.t.zepeda at utexas.edu


## References: 
[1] [http://dx.doi.org/10.5061/dryad.15fv2](http://dx.doi.org/10.5061/dryad.15fv2)

[2] [https://data.femadata.com/MOTF/](https://data.femadata.com/MOTF/)

[3] [https://cs.stanford.edu/~quocle/paragraph_vector.pdf](https://cs.stanford.edu/~quocle/paragraph_vector.pdf)

[4] [https://aclweb.org/anthology/W/W16/W16-6201.pdf](https://aclweb.org/anthology/W/W16/W16-6201.pdf)

[5] [http://www.deeplearningbook.org/](http://www.deeplearningbook.org/)
