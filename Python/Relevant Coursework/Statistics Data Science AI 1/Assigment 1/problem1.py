# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 21:26:40 2022

@author: danma
"""
import numpy as np
X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
# y = 1 * x_0 + 2 * x_1 + 3
y = np.dot(X, np.array([1, 2])) + 3


#%%% Problem 1
import pandas as pd;
file_path = 'C:/Users/danma/Downloads/STA 4364/Assigment 1/Auto.csv'
df = pd.read_csv(file_path)
df.dropna()
df = df[df['horsepower'] != '?']
df['horsepower'] = df['horsepower'].astype(int)
df.head()

#%%
from tabulate import tabulate
table = [['mpg', 'displacement', 'horsepower', 'weight', 'acceleration'], [str(df['mpg'].min()), str(df['displacement'].min()), str(df['horsepower'].min()), str(df['weight'].min()), str(df['acceleration'].min())], [str(df['mpg'].max()), str(df['displacement'].max()), str(df['horsepower'].max()), str(df['weight'].max()),str(df['acceleration'].max())]]
print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

#%%

import seaborn as sns
sns.pairplot(df, vars=['displacement', 'weight', 'horsepower', 'acceleration', 'mpg'], hue='cylinders')

#%%

import pandas as pd;
file_path = 'C:/Users/danma/Downloads/STA 4364/Assigment 1/CodParasite.txt'
df = pd.read_table(file_path)
df.dropna()

import seaborn as sns
import numpy as np
df['Intensity'] = df['Intensity'].apply(np.log1p)
sns.boxplot(y=df['Intensity'],x=df['Area'])
sns.boxplot(y=df['Intensity'],x=df['Sex'])
sns.boxplot(y=df['Intensity'],x=df['Stage'])
sns.boxplot(y=df['Intensity'],x=df['Year'])
#%%
import pandas as pd;
file_path = 'C:/Users/danma/Downloads/STA 4364/Assigment 1/Owls.txt'
df = pd.read_table(file_path)
df.dropna()

#plotting
import matplotlib.pyplot as plt
import seaborn as sns

fig, axs = plt.subplots(nrows=1,ncols=1,figsize=(5,5),dpi=100)
sns.scatterplot(y=df['SiblingNegotiation'],x=df['NegPerChick'],palette="Set2")

df['SiblingNegotiation'] = df['SiblingNegotiation'].apply(np.log1p)

fig, axs = plt.subplots(nrows=1,ncols=1,figsize=(5,5),dpi=100)
sns.scatterplot(y=df['SiblingNegotiation'],x=df['ArrivalTime'],palette="Set2")