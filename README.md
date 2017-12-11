## *What if 140 characters could save lives?* 

## Motivation

The 2017 Atlantic hurricane season was one of the most active hurricane seasons in over a decade. Not since the mid-2000s had the Atlantic churned out hurricanes with such frequency and intensity. Hurricanes Harvey, Irma, and Maria ravaged through large swaths of the southeast United States and Puerto Rico, causing significant spikes in buzz on Twitter in the process. The presence of a vast wealth of textual and geographical information available on Twitter coupled with the spikes in social media buzz during the events provided the basis for a very fundamental question: given a tweet from the areas affected during Hurricane Sandy, is it possible to predict the level of damage for that specific area?


## The Datasets

To answer our question, we turned our attention to one of the most significant meteorological events in recent memory: Hurricane Sandy. 

As it turns out, there was no lack of Twitter about Hurricane Sandy. For our project, we analyzed 47 million publicly available tweets with the hashtag “#sandy” or containing some other keyword deemed relevant to the storm and its aftermath [1]. 

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

## Preprocessing

First, we determined the zip code each tweet was from by examining the latitude and longitude of each tweet. Next, examined the FEMA dataset and looked at the types of damaged buildings by zip code. We categorized the damage level of each tweet by the worst damaged building in the zip code that tweet originated from. For example, if a tweet comes from a zip code with 6 affected buildings, 2 minorly damaged building, and 1 destroyed building, that tweet is classified as destroyed because of the single destroyed building. We chose this method of classification because we believe that it is more prudent to overestimate damage in a disaster scenario.

## Our Design Overview

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/block_diagram.png "Block Diagram")

## Visualization

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/map_tool.png "Map Visualizer")

## Word Clouds

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/word_clouds.png "Word Clouds")

## Time Series Exploration

We thought that there might be predictive information in the distribution of the tweets by zip code. We observed that the dataset had many more tweets during the time when the most affected regions were under Hurricane Sandy. The image below on the right is the distribution of tweets between October 15th 2012 and November 15th 2012. The below image on the left is the distribution of tweets for each zip code between October 29th 2012 at 6pm EST and October 30th 2012 at 6pm EST. 

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/time_series_1.png "Time Series 1")

We tried to predict the distribution of buildings damaged by FEMA using the distribution of tweets by hour as features. We were unsuccessful in making this prediction, as predicting all zeros resulted in a better mean absolute error score. 

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/time_series_2.png "Time Series 2")

Next, we tried to classify the presence of damaged buildings by zip code using the same frequency information. If a zip code had a building classified in a certain category, we classed that as true in our prediction. The below plots are the ROC scores for each of the five categories

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/time_series_3.png "Time Series 3")

## Tweets as Embedded Vectors

In order to make meaning out of our tweets, we sought the help of the Doc2Vec library, as close relative of the popular Word2Vec API. Essentially, Doc2Vec converts sentences (in our case, tweets) into vectors. In order to do this, our dataset was converted into a matrix _D_, where each row denotes of tokens in the dataset and each column denotes a tweet. Each element _D<sub>ij</sub>_ consists of some value to indicate the presence of token _i_ in sentence _j_ [3]. An example illustration of the Doc2Vec framework is shown below: 

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/doc2vec.png "Doc2vec Illustration")

There are a couple of advantages to the Doc2Vec approach. The first is that the semantic relationships between words are preserved; the euclidean distance between the vectorized words encapsulates the semantics behind the words themselves. Second, including a term-document matrix in the encoding preserves the ordering of sentences themselves. For example, _I walked the dog_ is a drastically different from _The dog walked I_. Including _D_ in a sentence encoding allows for the inclusion of both semantic and ordinal in a sentence [3]. 

Naturally, there are many ways to encode _D_. Here are three: 

## Model Architecture

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/model_architecture.png "Model Architecture")

The network's input layer receives a 200-dimensional topic vector from a latent semantic index (LSI) embedding.  
The early hidden layers reduce the previous layer size by half until reaching a size of 10.  
Next, the deep layers learn complex nonlinear relationships between the earlier learned hidden features.  
There are 20 deep hidden layers, each of size 10. All of the hidden layers use a ReLU activation function.  
The output layer of the network outputs a classification probability for each of the five categories with a softmax activation function.  

## Empirical Results

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/empirical_results.png "Deep Topics Network Results")

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/simple_results.png "Simple BOW Network Results")


# References: 
[1] http://dx.doi.org/10.5061/dryad.15fv2

[2] https://data.femadata.com/MOTF/

[3] https://cs.stanford.edu/~quocle/paragraph_vector.pdf

[4] https://aclweb.org/anthology/W/W16/W16-6201.pdf

[5] http://www.deeplearningbook.org/
