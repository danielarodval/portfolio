#%% Import and Scale Data
import pandas as pa;

file_path = 'C:/Users/danma/Desktop/Personal Documents/UCF/STA 4365/final/gene_data.csv'
df = pa.read_csv(file_path, header=None)
#transpose
df = df.transpose()

from sklearn.preprocessing import StandardScaler
#standardize
scalar = StandardScaler()
scalar.fit(df)

df = scalar.transform(df)

print("DataFrame Output:\n",df)

#%% K-means
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=2, random_state=0).fit(df)
clst = kmeans.labels_

print("clusters:",clst)

import numpy as np
true_class = np.array(['1']*20 + ['0']*20, dtype=int)

tab = pa.crosstab(clst, true_class, rownames = ['cluster'], colnames = ['true_class']);
print("\n",tab)

#%% Plotting with TSNE

from sklearn.decomposition import PCA

pca = PCA(n_components=40)

principalComponents = pca.fit_transform(df)
principalDf = pa.DataFrame(principalComponents)

from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, learning_rate='auto', init='pca')
tsne_proj = tsne.fit_transform(principalDf)

embeddingsdf = pa.DataFrame()
embeddingsdf['x'] = tsne_proj[:,0]
embeddingsdf['y'] = tsne_proj[:,1]
embeddingsdf.head()

###PLOT FIGURES FOR TSNE

import seaborn as sns
from matplotlib import pyplot as plt

labels_scale = clst

plt.figure(figsize = (10,10))
sns.scatterplot(x=tsne_proj[:,0], y=tsne_proj[:,1], 
                hue=labels_scale, 
                palette='Set1',
                s=100, alpha=0.2).set_title('KMeans Clusters (2) Labels on 2d t-SNE embeddings', fontsize=15)
plt.legend()
plt.ylabel('PC2')
plt.xlabel('PC1')
plt.show()

###PLOT FIGURES FOR KMEANS
pca = PCA(2)
df2 = pca.fit_transform(df)

kmeans = KMeans(n_clusters=2, random_state=0)
label = kmeans.fit_predict(df2)

labels_scale = clst

plt.figure(figsize = (10,10))
sns.scatterplot(x=df2[:,0], y=df2[:,1], 
                hue=labels_scale, 
                palette='Set1',
                s=100, alpha=0.2).set_title('KMeans Clusters (2) Labels on KMeans Clustering', fontsize=15)
plt.legend()
plt.ylabel('PC2')
plt.xlabel('PC1')
plt.show()