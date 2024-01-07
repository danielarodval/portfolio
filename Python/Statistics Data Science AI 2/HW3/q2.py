# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 22:30:02 2022
Search

@author: danma
"""

#%% Genereating a simulated data set with 60 observations

import pandas as pd
import numpy as np

#creates 50 columns
col = [1]*50
#randomly generates 20 normalized rows per column
arrays_1 = [np.random.normal(loc=0, scale=c, size=(20)) for c in col]
#creates dataframe from numpy arrays
df_1 = pd.DataFrame.from_dict(arrays_1)
#transposes to create a 20 observation/row 50 variable/column dataframe
#adds a classifier column to identify what class observation it is from
listtype = ['class_1']*20
dftype = pd.DataFrame(listtype).transpose()
#add to original dataframe
df_1 = pd.concat([df_1,dftype])
#transposes to create a 20 observation 50 variable dataframe
df_1 = df_1.transpose()
print("Head of DataFrame 1:\n",df_1.head(),"\nShape:",df_1.shape)
del arrays_1, listtype, dftype
#repeat 2 times with different meanshifts/loc
arrays_2 = [np.random.normal(loc=0.7, scale=c, size=(20)) for c in col]
df_2 = pd.DataFrame.from_dict(arrays_2)

listtype = ['class_2']*20
dftype = pd.DataFrame(listtype).transpose()
df_2 = pd.concat([df_2,dftype])
df_2 = df_2.transpose()
print("Head of DataFrame 2:\n",df_2.head(),"\nShape:",df_2.shape)
del arrays_2, listtype, dftype
arrays_3 = [np.random.normal(loc=1.4, scale=c, size=(20)) for c in col]
df_3 = pd.DataFrame.from_dict(arrays_3)

listtype = ['class_3']*20
dftype = pd.DataFrame(listtype).transpose()
df_3 = pd.concat([df_3,dftype])
df_3 = df_3.transpose()
print("Head of DataFrame 3:\n",df_3.head(),"\nShape:",df_3.shape)
del arrays_3, listtype, dftype

df = pd.concat([df_1,df_2,df_3]).reset_index(drop=True)
df = df.set_axis([*df.columns[:-1], 'observation'], axis=1, inplace=False)

print("Head of X:\n",df.head(),"\nShape:",df.shape)
del df_1, df_2, df_3, col
#%% Perform PCA on the 60 observations and plot

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

#separating out the features
X = df.iloc[: , :50]

#separating out the target
y = df.loc[:,['observation']].values

pca = PCA(n_components=50)

principalComponents = pca.fit_transform(X)
principalDf = pd.DataFrame(principalComponents)

finalDf = pd.concat([principalDf, df[['observation']]], axis = 1)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

targets = ['class_1', 'class_2', 'class_3']
colors = ['r', 'g', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['observation'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 0]
               , finalDf.loc[indicesToKeep, 1]
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()

del principalComponents, ax, color, colors, fig, indicesToKeep, pca, principalDf, target, targets
#%% Perfrom K-means clustering k=3
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
true_class = np.array(['0']*20 + ['1']*20 + ['2']*20, dtype=int)
cluster = kmeans.labels_
print(cluster,"\n")
tab = pd.crosstab(cluster, true_class, rownames = ['cluster'], colnames = ['true_class']);
print(tab)
del kmeans, true_class, cluster, tab
#%% Perfrom K-means clustering k=2
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
true_class = np.array(['0']*20 + ['1']*20 + ['2']*20, dtype=int)
cluster = kmeans.labels_
print(cluster)
tab = pd.crosstab(cluster, true_class, rownames = ['cluster'], colnames = ['true_class']);
print(tab)
del kmeans, true_class, cluster, tab
#%% Perfrom K-means clustering k=4
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4, random_state=0).fit(X)
true_class = np.array(['0']*20 + ['1']*20 + ['2']*20, dtype=int)
cluster = kmeans.labels_
print(cluster)
tab = pd.crosstab(cluster, true_class, rownames = ['cluster'], colnames = ['true_class']);
print(tab)
del kmeans, true_class, cluster, tab

#%% Perform K-means clustering on principal component score vectors.
from sklearn.cluster import KMeans

princ2 = finalDf.iloc[: , :2]
kmeans = KMeans(n_clusters=3, random_state=0).fit(princ2)
true_class = np.array(['0']*20 + ['1']*20 + ['2']*20, dtype=int)
cluster = kmeans.labels_
print(cluster)
tab = pd.crosstab(cluster, true_class, rownames = ['cluster'], colnames = ['true_class']);
print(tab)
del kmeans, true_class, cluster, tab, princ2

#%%  Perform K-means clustering after scaling each variable
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=0).fit(scale(X))
true_class = np.array(['0']*20 + ['1']*20 + ['2']*20, dtype=int)
cluster = kmeans.labels_
print(cluster,"\n")
tab = pd.crosstab(cluster, true_class, rownames = ['cluster'], colnames = ['true_class']);
print(tab)
del kmeans, true_class, cluster, tab

