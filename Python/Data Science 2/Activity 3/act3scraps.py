# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 17:47:49 2022

@author: danma
"""

#%%
import pandas as pd;

microsoft = pd.read_csv('C:/Users/danma/Downloads/Microsoft_Results.csv')
microsoft = microsoft.dropna()

microsoft.head()
#%%
microsoft['HasDetections'] = microsoft['HasDetections'].astype(float)

y = microsoft['HasDetections']
y_pred_proba = microsoft['P_HasDetections']

#true positive
#false positive
#true negative
#false negative
#sensitivity
#specificity
#accuracy
#precision
from sklearn.metrics import average_precision_score;
print(average_precision_score(y, y_pred_proba))

#%%
from sklearn.metrics import roc_auc_score;
# Calculating AUC and GINI of Model
auc = roc_auc_score(y, y_pred_proba)
gini = 2*(auc-0.5)

print('AUC: %.2f' % auc)
print('GINI: %.2f' % gini)

#%%
import matplotlib.pyplot as plt;
from sklearn.metrics import roc_curve;
import numpy as np;
fpr, tpr, thresholds = roc_curve(y, y_pred_proba)

tpr10 = np.quantile(tpr, q = np.arange(0.095, 1, 0.095))
fpr10 = np.quantile(fpr, q = np.arange(0.095, 1, 0.095))
#shows 10 points
print(len(tpr10))

plt.figure(figsize=(12, 8), dpi=200)
plt.plot(fpr10, tpr10, label = 'roc',marker='.')
plt.legend(fontsize=16)
plt.title("10 Percentile")
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# show the legend
plt.legend()
# show the plot
plt.show()

#%%
tpr5 = np.quantile(tpr, q = np.arange(0.048, 1, 0.048))
fpr5 = np.quantile(fpr, q = np.arange(0.048, 1, 0.048))
#shows 10 points
print(len(tpr5))

plt.figure(figsize=(12, 8), dpi=200)
plt.plot(fpr5, tpr5, label = 'roc',marker='.')
plt.legend(fontsize=16)
plt.title("5 Percentile")
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# show the legend
plt.legend()
# show the plot
plt.show()
#%% produce a lift chart of the model at decile level (i.e., every ten percent one point).

#divide each entry in decile by .55 cutoff 
tpr10lift = tpr10 / .55
#get cummalative true positive rate
tpr10cumlift = np.cumsum(tpr10lift)

plt.figure(figsize=(12, 8), dpi=200)
plt.plot(fpr10, tpr10lift, label = 'Lift',marker='.')
plt.plot(fpr10, tpr10cumlift, label = 'Cummalative Lift',marker='.')
plt.legend(fontsize=16)
plt.title("Lift Chart")
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# show the legend
plt.legend()
# show the plot
plt.show()

#%%

skplt.metrics.plot_lift_curve(
    fpr10, tpr10, figsize=(12, 8), title_fontsize=20, text_fontsize=18
)
plt.show()