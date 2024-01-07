import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('C:/Users/danma/Downloads/Wine_Quality_Data.csv')

df = df.drop('color',axis=1)

from sklearn.preprocessing import StandardScaler
scaler =  StandardScaler()
scaled_df = scaler.fit_transform(df)
print(scaled_df)

from sklearn.decomposition import PCA
pca = PCA()
pca_df = pca.fit_transform(scaled_df)
print(pca_df)