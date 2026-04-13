# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 22:30:02 2022
Search

@author: danma
"""

#%% Import data into dataframe and split
import pandas as pa;

file_path = 'C:/Users/danma/Personal Documents/School/Archive/11 Spring 2022/STA 4365/HW3/fashion-mnist_train.csv'
df = pa.read_csv(file_path) 

#creates small dataframe 
sm_df = df.sample(frac = .08333, random_state = 50)
labels = sm_df.filter(regex='label')
pixels = sm_df.filter(regex='pixel')

print(sm_df.head())
print(labels.head())
print(pixels.head())

#del file_path, df, sm_df

#%% learn kmeans model using the kmeans++ initialization methods k=10
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

kmeans = KMeans(n_clusters=10, random_state=0).fit(pixels)
clst = kmeans.labels_
print('labels:\n',clst)
shape = kmeans.cluster_centers_.shape
print('shape:\n',shape)

fig, ax = plt.subplots(2, 5, figsize=(28, 12))
centers = kmeans.cluster_centers_.reshape(10, 28, 28)
for axi, center in zip(ax.flat, centers):
    axi.set(xticks=[], yticks=[])
    axi.imshow(center, interpolation='nearest', cmap=plt.cm.binary)

del fig, ax, centers, center, axi, shape, clst
#%% use PCA before learning t-SNE model and creating two plots
from sklearn.decomposition import PCA

pca = PCA(n_components=50)

principalComponents = pca.fit_transform(pixels)
principalDf = pa.DataFrame(principalComponents)

from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, learning_rate='auto', init='pca')
tsne_proj = tsne.fit_transform(principalDf)

# Create DF
embeddingsdf = pa.DataFrame()
# Add game names
embeddingsdf['label'] = labels
# Add x coordinate
embeddingsdf['x'] = tsne_proj[:,0]
# Add y coordinate
embeddingsdf['y'] = tsne_proj[:,1]
# Check
embeddingsdf.head()

#%% Plotting
import seaborn as sns
plt.figure(figsize = (10,10))
sns.scatterplot(x=embeddingsdf.x, y=embeddingsdf.y,
                palette='Set1',
                s=100, alpha=0.2).set_title('2D t-SNE embedding of the observed data', fontsize=15)
plt.legend()
plt.ylabel('PC2')
plt.xlabel('PC1')
plt.show()

###PLOT FIGURES FOR TSNE

import seaborn as sns

labels_scale = kmeans.labels_

plt.figure(figsize = (10,10))
sns.scatterplot(x=tsne_proj[:,0], y=tsne_proj[:,1], 
                hue=labels_scale, 
                palette='Set1',
                s=100, alpha=0.2).set_title('KMeans Clusters (10) Labels on 2d t-SNE embeddings', fontsize=15)
plt.legend()
plt.ylabel('PC2')
plt.xlabel('PC1')
plt.show()

###PLOT FIGURES FOR KMEANS
pca = PCA(2)

df = pca.fit_transform(pixels)

plt.figure(figsize = (10,10))
sns.scatterplot(x=df[:,0], y=df[:,1], 
                hue=labels_scale, 
                palette='Set1',
                s=100, alpha=0.2).set_title('KMeans Clusters (10) Labels on KMeans Clustering', fontsize=15)
plt.legend()
plt.ylabel('PC2')
plt.xlabel('PC1')
plt.show()

