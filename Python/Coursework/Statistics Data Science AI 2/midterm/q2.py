# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 15:51:49 2022

@author: danma
"""

#%% Step 1 Imports data into pandas dataframe
import pandas as pa

df = pa.read_table('C:/Users/danma/Documents/STA 4365/midterm/parkinsons.data', sep=',')
print(df.head())

#%% Step 2 splits data into x and y

x = df.drop(['status', 'name'], axis=1)
y = df.iloc[:, 17]

#turns y into a 1-d array instead of a dataframe column
y = y.to_numpy()
y = y.ravel()
y = y.astype('int')

#%% Step 3 Prepare data by standardizing each feature to have mean 0 and variance 1

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

x[list(x.columns)] = scaler.fit_transform(x[list(x.columns)])

print(x.head())

#%% Step 4 K-Means Model on Unsupervised Features and Plots

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from  sklearn.metrics import silhouette_samples
import matplotlib.cm as cm
import numpy as np

# List to store cluster and intra cluster distance

clusters = []
inertia_vals = []
all_scores = []

# Since creating one cluster is similar to observing the data as a whole, multiple values of K are utilized to come up with the optimum cluster value
#Note: Cluster number and intra cluster distance is appended for plotting the elbow curve
for k in range(2, 16, 1):
    
    # Create a subplot with 1 row and 2 columns
    fig, (ax1) = plt.subplots(1,1)
    
    fig.set_size_inches(10, 7)
    
    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(x) + (k + 1) * 10])
    
    # train clustering with the specified K
    model = KMeans(n_clusters=k, random_state=10, algorithm="auto")
    model.fit(x)
    # append model to cluster list
    clusters.append(model)
    inertia_vals.append(model.inertia_)
    cluster_labels = model.fit_predict(x)
    #print("---------------------------------------")
    #print(clusters[k-2])
    #print("Silhouette score:",silhouette_score(x, clusters[k-2].predict(x)))
    all_scores.append(silhouette_score(x, clusters[k-2].predict(x)))
    
    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(x, clusters[k-2].predict(x))
    
    y_lower = 10
    for i in range(k):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / k)
        ax1.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7
        )
        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples
     
    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_score(x, clusters[k-2].predict(x)), color="red", linestyle="--")
 
    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

del inertia_vals, model, ax1, cluster_labels, color, fig, i, ith_cluster_silhouette_values, k
del sample_silhouette_values, size_cluster_i, y_lower, y_upper

#%% Step 5 What is the optimal number of clusters for this dataset for each model?
best_cluster = clusters[all_scores.index(max(all_scores))]
print("The Optimal Number of Clusters is ", best_cluster.n_clusters)

#%%  Learn a final K-means model using the optimal number of clusters.

model = KMeans(n_clusters=best_cluster.n_clusters, random_state=10, algorithm="auto")
model.fit_predict(x)

# Calculate Silhoutte Score
score = silhouette_score(x, model.labels_, metric='euclidean')

# Print the score
print('Silhouetter Score: %.3f' % score)

from yellowbrick.cluster import SilhouetteVisualizer

fig, ax = plt.subplots(1,1, figsize=(15,8))

visualizer = SilhouetteVisualizer(model, colors='yellowbrick', ax=ax)
visualizer.fit(x)

