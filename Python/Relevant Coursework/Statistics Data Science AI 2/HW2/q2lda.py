# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%% import libraries
import numpy as np;
import pandas as pa;

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier


#%% Step 1- imports data into dataframe
col_names=['fLength', 'fWidth', 'fSize', 'fConc', 'fConc1', 'fAsym', 'fM3Long', 'fM3Trans', 'fAlpha', 'fDist', 'class']
df = pa.read_table('C:/Users/Daniel Rodriguez/Downloads/Machine Learning AI/HW2/hw2/magic04.data', sep=',', header=None, names=col_names)
df.head()
#%% Step 2 - splits data into x and y
x = df.filter(regex='f')
y = df.filter(regex='class')

#splits into training and test data
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=.2, random_state=0)

#%% Step 3 - scale and center columns
scalar = StandardScaler()
scalar.fit(x_train)

x_train = scalar.transform(x_train)
x_test = scalar.transform(x_test)

#%% Step 4 - Classify data sets
#Logistic Regression
    #import libraries
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

#create dataframe with y training data, categorical

#repace categorical data characters with 1 and 0, 1 to separate from 0
y_train = y_train.replace('g',1, regex=True)
y_train = y_train.replace('h',0, regex=True)

#%% test 1

#y_train = y_train.to_numpy()
#y_train = y_train.ravel()
#load data into logistcic regression model
x_train, y_train = load_iris(return_X_y=True)

#%% test 2
clf = LogisticRegression()
clf.fit(x_train, y_train)

#%% test 3
clf.predict(x_test)

clf.predict_proba(x_test)

#print("Logistic Regression Score = ", clf.score(df_x, temp_y))

from sklearn.metrics import classification_report

#print(classification_report(df_x, temp_y, ))

#%% MachineLearningMastery Article


y_train = y_train.to_numpy()
y_train = y_train.ravel()

print(x_train.shape,y_train.shape)

from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score

cv = RepeatedStratifiedKFold(n_splits=8, n_repeats=3, random_state=1)

scores = cross_val_score(lda, x_train, y_train, scoring='accuracy', cv=cv, n_jobs=-1)

print('Mean Accuracy: %.3f (%.3f)' %(mean(scores), std(scores)))
