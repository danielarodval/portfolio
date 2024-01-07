# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 18:48:45 2022

@author: danma
"""

import pandas as pd 
import statsmodels.formula.api as smf
houses = pd.read_csv('C:/Users/danma/Downloads/House_Prices_PRED.csv')
houses = houses.iloc[: , 1:]
houses.head()

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(houses['SalePrice'], houses['P_SalePrice'])
print(mse)

import numpy as np

sse = np.sum((houses['SalePrice'] - houses['P_SalePrice'])**2)
print(sse/1459)