import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
from sklearn.cross_validation import train_test_split
import xgboost as xgb

#%% GET DATA

with open('zip_to_dist.pkl', 'rb') as handle:
    zip_to_dist = pickle.load(handle)
    
with open('hours_ny.pkl', 'rb') as handle:
    hours_dist = pickle.load(handle)

hours_dist = hours_dist.transpose()
hours_dist_list = hours_dist.index.values

#%% Clean data
hours_dist_y = pd.DataFrame()
for zipcode in hours_dist_list:
    data = pd.DataFrame(zip_to_dist[zipcode]).transpose()
    if np.isnan(data[0]).bool():
        data = data.fillna(0)
        data[4] = 1
    else:
        data[4] = 0
    hours_dist_y = hours_dist_y.append(data)
hours_dist_y.index = hours_dist.index


#%% Regression

def abs_cv(model, x, y):
    abs_val = cross_val_score(model, x, y, scoring="neg_mean_absolute_error", cv = 5)
    return(abs_val)


xgb_reg = xgb.XGBRegressor()
zeros = np.zeros((317,))

categories = ["affected", "minor", "major", "destroyed", "unknown"]
abs_cross = [0] * 5
for category in range(0, 5):
    print categories[category]
    abs_cross[category] = -abs_cv(xgb_reg, hours_dist, hours_dist_y[category]).mean()
    print abs_cross[category]

hours_dist_train, hours_dist_test, hours_dist_y_train, hours_dist_y_test= train_test_split(hours_dist, hours_dist_y)

abs_val = [0] * 5
for category in range(0, 5):
    print categories[category]
    xgb_reg.fit(hours_dist_train, hours_dist_y_train[category])
    preds = xgb_reg.predict(hours_dist_test)
    abs_val[category] = mean_absolute_error(hours_dist_y_test[category], preds)
    print abs_val[category]

#%% Plot Regression
ind = [0,1,2,3,4]
plt.bar(ind, abs_cross)
plt.title('Mean absolute error (cross validation)')
plt.xticks(ind, ('affected', 'minor', 'major', 'destroyed', 'unknown'))
plt.show()

plt.bar(ind, abs_val)
plt.title('Mean absolute error (test/train split)')
plt.xticks(ind, ('affected', 'minor', 'major', 'destroyed', 'unknown'))
plt.show()

#%% classifying

def classify(val):
    return val != 0

hours_dist_class = pd.DataFrame(index=hours_dist_y.index)
hours_dist_class["affected"] = hours_dist_y.apply(lambda row: classify(row[0]), axis=1)
hours_dist_class["minor"] = hours_dist_y.apply(lambda row: classify(row[1]), axis=1)
hours_dist_class["major"] = hours_dist_y.apply(lambda row: classify(row[2]), axis=1)
hours_dist_class["destroyed"] = hours_dist_y.apply(lambda row: classify(row[3]), axis=1)
hours_dist_class["unknown"] = hours_dist_y.apply(lambda row: classify(row[4]), axis=1)

def roc_cv(model, x, y):
    roc = cross_val_score(model, x, y, scoring="roc_auc", cv = 5)
    return(roc)

hours_dist_train, hours_dist_test, hours_dist_y_train, hours_dist_y_test = train_test_split(hours_dist, hours_dist_class)

xgb_class = xgb.XGBClassifier()

categories = ["affected", "minor", "major", "destroyed", "unknown"]
roc_cross = [0] * 5
for category in range(0, 5):
    print categories[category]
    roc_cross[category] = roc_cv(xgb_class, hours_dist_train, hours_dist_y_train[categories[category]]).mean()
    print roc_cross[category]

roc_val = [0] * 5
for category in range(0, 5):
    print categories[category]
    xgb_class.fit(hours_dist_train, hours_dist_y_train[categories[category]])
    preds = xgb_class.predict_proba(hours_dist_test)[:, 1:]
    roc_val[category] = roc_auc_score(hours_dist_y_test[categories[category]], preds)
    print roc_val[category]

#%% Plot classifying stuff

ind = [0,1,2,3,4]
plt.bar(ind, roc_cross)
plt.title('ROC (cross validation)')
plt.xticks(ind, ('affected', 'minor', 'major', 'destroyed', 'unknown'))
plt.show()

plt.bar(ind, roc_val)
plt.title('ROC (test/train split)')
plt.xticks(ind, ('affected', 'minor', 'major', 'destroyed', 'unknown'))
plt.show()

