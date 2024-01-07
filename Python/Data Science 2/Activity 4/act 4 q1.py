# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 00:08:58 2022

@author: danma
"""

#%% 1.	Read the data into your software system
import pandas as pd;
file_path = 'C:/Users/danma/Downloads/ACT_04_Data.csv'
colnames=['Y','X1','X2','X12','X1SQ', 'X2SQ'] 
df = pd.read_csv(file_path, names=colnames)
df = df.iloc[1: , :]
df = df.astype('int32')
df.dropna()

print(df.head)

del file_path, colnames
#%% 2.	Produce a scatter plot of Y and X1.
import seaborn as sns;
sns.set_style("darkgrid")
sns.scatterplot(data=df, x="X1", y="Y")

#%% 3.	Produce a scatter plot of Y and X2.
sns.scatterplot(data=df, x="X2", y="Y")

#%% 4.	Build a regression model with two predictors X1 and X2. (Model I)
from sklearn.linear_model import LinearRegression
model1 = LinearRegression().fit(df[['X1','X2']],df['Y'])

#%% 5.	Build another regression model with three predictors X1, X2, and X12. (Model II)
model2 = LinearRegression().fit(df[['X1','X2', 'X12']],df['Y'])

#%% 6.	Build the third regression model with all five predictors. (Model III)
model3 = LinearRegression().fit(df.loc[:, df.columns != 'Y'],df['Y'])

#%% 7.	Build the last regression model with four predictors X1, X2, X12, and X1SQ (Model IV)
model4 = LinearRegression().fit(df[['X1','X2', 'X12', 'X1SQ']],df['Y'])

#%% Results
r_sq1 = model1.score(df[['X1','X2']],df['Y'])
r_sq2 = model2.score(df[['X1','X2', 'X12']],df['Y'])
r_sq3 = model3.score(df.loc[:, df.columns != 'Y'],df['Y'])
r_sq4 = model4.score(df[['X1','X2', 'X12', 'X1SQ']],df['Y'])

from sklearn.metrics import mean_squared_error;
mse1 = mean_squared_error(df['Y'], model1.predict(df[['X1','X2']]))
mse2 = mean_squared_error(df['Y'], model2.predict(df[['X1','X2', 'X12']]))
mse3 = mean_squared_error(df['Y'], model3.predict(df.loc[:, df.columns != 'Y']))
mse4 = mean_squared_error(df['Y'], model4.predict(df[['X1','X2', 'X12', 'X1SQ']]))

#to create summary table at the end
from tabulate import tabulate

data = {'model1': [r_sq1,mse1]}
table = pd.DataFrame(data)

data = {'model2': [r_sq2,mse2]}
table['model2'] = pd.DataFrame(data)

data = {'model3': [r_sq3,mse3]}
table['model3'] = pd.DataFrame(data)

data = {'model4': [r_sq4,mse4]}
table['model4'] = pd.DataFrame(data)

print(tabulate(table, headers='keys',tablefmt='fancy_grid',showindex=["R-Squared","MSE"]))