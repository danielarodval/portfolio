# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np;
import pandas as pa;
import sklearn as sk;

#Step 1- imports data
data = pa.read_table('C:/Users/Daniel Rodriguez/Downloads/Machine Learning AI/HW2/hw2/magic04.data', sep=',', header=None)
print(data)

#Step 1 - creates data frame
df = pa.DataFrame(data)

#Step 2 - randomly selects small portion from data frame
training_data = df.sample(frac=0.8, random_state=25)
testing_data = df.drop(training_data.index)

print(training_data)

#Step 3 - scale and center columns
    #use mean and standard deviation of each column


#Step 4 - Classify data sets
#Linear Regression
sk.linear_model.LinearRegression()