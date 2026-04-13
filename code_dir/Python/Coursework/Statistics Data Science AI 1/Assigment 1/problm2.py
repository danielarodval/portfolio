# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 21:54:40 2022

@author: danma
"""

#%%
#Load Dataset
import pandas as pa;
import numpy as np;
import seaborn as sns;
file_path = 'C:/Users/danma/Downloads/STA 4364/Assignment 2/AirQuality.csv'
df = pa.read_csv(file_path,parse_dates= {"datetime" : ["year","month","day","hour"]},date_parser=lambda x: pa.datetime.strptime(x, '%Y %m %d %H'),keep_date_col=True)
#omit rows with NA entries
df = df.dropna()
df.head()
#Plot histogram of PM2.5, take log transformation, remove 0 entries
#remove 0 entries
df = df.loc[df['pm2.5'] != 0]
#log transformation
df['pm2.5'] = df['pm2.5'].apply(np.log)
#plot histogram
sns.histplot(data=df['pm2.5'])
#%%Exploratory analysis polution over time, months or days with greater pollution environmental factors
import matplotlib.pyplot as plt
plt.style.use('seaborn') # pretty matplotlib plots
plt.rc('font', size=14)
plt.rc('figure', titlesize=18)
plt.rc('axes', labelsize=15)
plt.rc('axes', titlesize=18)

fig, axs = plt.subplots(nrows=2,ncols=2,figsize=(20, 20),dpi=500)
sns.boxplot(x='year', y='pm2.5', data=df,ax=axs[0,0])
sns.boxplot(x='month', y='pm2.5', data=df,ax=axs[0,1])
sns.boxplot(x='day', y='pm2.5', data=df,ax=axs[1,0])
sns.boxplot(x='hour', y='pm2.5', data=df,ax=axs[1,1])

plotEx_1 = plt.figure(figsize=(50,25),dpi=500)
plotEx_1.axes[0] = sns.pairplot(df, vars=['pm2.5','DEWP', 'TEMP', 'PRES', 'cbwd', 'Iws', 'Is', 'Ir'], palette='Paired', kind='scatter')

#%% Transform
df.drop(['datetime'], axis=1, inplace=True)
df['sin_time_month'] = np.sin(2*np.pi*df['month'].astype(int)/12)
df['cos_time_month'] = np.cos(2*np.pi*df['month'].astype(int)/12)
df.drop(['month'], axis=1, inplace=True)
df['sin_time_day'] = np.sin(2*np.pi*df['day'].astype(int)/30)
df['cos_time_day'] = np.cos(2*np.pi*df['day'].astype(int)/30)
df.drop(['day'], axis=1, inplace=True)
df['sin_time_hour'] = np.sin(2*np.pi*df['hour'].astype(int)/24)
df['cos_time_hour'] = np.cos(2*np.pi*df['hour'].astype(int)/24)
df.drop(['hour'], axis=1, inplace=True)