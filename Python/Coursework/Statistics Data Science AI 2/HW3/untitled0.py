# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 10:45:37 2022

@author: danma
"""

#Importing required modules
 
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
import numpy as np
 
#Load Data
data = load_digits().data
pca = PCA(2)
 
#Transform the data
df = pca.fit_transform(data)
 
df.shape

### (1797, 2)

#Import required module
from sklearn.cluster import KMeans
 
#Initialize the class object
kmeans = KMeans(n_clusters= 10)
 
#predict the labels of clusters.
label = kmeans.fit_predict(df)
 
print(label)

### [0 3 7 ... 7 4 9]

#Getting unique labels
 
u_labels = np.unique(label)
 
#plotting the results:
import matplotlib.pyplot as plt
 
for i in u_labels:
    plt.scatter(df[label == i , 0] , df[label == i , 1] , label = i)
plt.legend()
plt.show()

