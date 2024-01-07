#%% Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
import centroid_initialization as cent_init

#%matplotlib inline

#%% Creating some data

from sklearn.datasets import make_blobs

n_samples = 250
n_features = 2
n_clusters = 4
random_state = 42
max_iter = 100

X, y = make_blobs(n_samples=n_samples, 
                  n_features=n_features, 
                  centers=n_clusters, 
                  random_state=random_state)

fig=plt.figure(figsize=(8,8), dpi=80, facecolor='w', edgecolor='k')
plt.scatter(X[:, 0], X[:, 1]);

#%% k-means++ Initialization

plus_centroids = cent_init.plus_plus(X, n_clusters)
print(plus_centroids)

#%% Random Initialization

random_centroids = cent_init.random(X, n_clusters)
print(random_centroids)

#%% Naive Sharding Initialization

naive_centroids = cent_init.naive_sharding(X, n_clusters)
print(naive_centroids)