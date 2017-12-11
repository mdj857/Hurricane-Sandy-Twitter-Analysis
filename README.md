## *What if 140 characters could save lives?* 

## Motivation

The 2017 Atlantic hurricane season was one of the most active hurricane seasons in over a decade. Not since the mid-2000s had the Atlantic churned out hurricanes with such frequency and intensity. Hurricanes Harvey, Irma, and Maria ravaged through large swaths of the southeast United States and Puerto Rico, causing significant spikes in buzz on Twitter in the process. The presence of a vast wealth of textual and geographical information available on Twitter coupled with the spikes in social media buzz during the events provided the basis for a very fundamental question: given a tweet from the areas affected during Hurricane Sandy, is it possible to predict the level of damage for that specific area?


## The Datasets

To answer our question, we turned our attention to one of the most significant meteorological events in recent memory: Hurricane Sandy. 

As it turns out, there was no lack of Twitter about Hurricane Sandy. For our project, we analyzed 37 million publicly available tweets with the hashtag “#sandy” or containing some other keyword deemed relevant to the storm and its aftermath [1]. 

For our damage analysis, we used data from FEMA’s post-disaster survey of 300,000 affected buildings in the tri-state area [2]. As part of their survey, FEMA labeled buildings as affected, minor damage, major damage, or destroyed. A summary of our datasets and the damage classification rule is shown below. 

#### The Datasets

| | Tweet Dataset | FEMA Damage Dataset |
| ---- | ------- | ----- |
| Number of Samples | 47 million tweets (11 GB)  | 300k buildings (48 MB)  |
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

## Visualization

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/map_tool.png "Map Visualizer")

## Word Clouds

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/word_clouds.png "Word Clouds")

## Time Series Exploration

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/time_series_1.png "Time Series 1")
![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/time_series_2.png "Time Series 2")
![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/time_series_3.png "Time Series 3")

## Tweets as Embedded Vectors

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/doc2vec.png "Doc2vec Illustration")

## Model Architecture

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/model_architecture.png "Model Architecture")

## Empirical Results

![alt text](https://github.com/mdj857/Hurricane-Sandy-Twitter-Analysis/raw/master/images/empirical_results.png "Empirical Results")


# References: 
[1] http://dx.doi.org/10.5061/dryad.15fv2

[2] https://data.femadata.com/MOTF/

[3] https://aclweb.org/anthology/W/W16/W16-6201.pdf

[4] http://www.deeplearningbook.org/
