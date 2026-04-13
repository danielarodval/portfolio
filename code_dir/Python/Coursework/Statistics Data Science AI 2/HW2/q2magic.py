# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np;
import pandas as pa;

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier

#Step 1- imports data
data = pa.read_table('C:/Users/Daniel Rodriguez/Downloads/Machine Learning AI/HW2/hw2/magic04.data', sep=',', header=None)

#Step 1 - creates data frame
df = pa.DataFrame(data)
#drop categorical data
df.drop([10], axis=1, inplace=True)

#Step 2 - randomly selects small portion from data frame
x = df.iloc[:, 0:3].values
y = df.iloc[:, 3].values

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=.2, random_state=0)

#Step 3 - scale and center columns
scalar = StandardScaler()
scalar.fit(x_train)

x_train = scalar.transform(x_train)
x_test = scalar.transform(x_test)


#Step 4 - Classify data sets
#Linear Regression
    #select data
reg_x = x_train
reg_y = y_train
    #train model
reg = LinearRegression().fit(reg_x,reg_y)
    #score model
reg.score(reg_x,reg_y)
print("Linear Regression Score = " , reg.score(reg_x,reg_y))

#LDA - Categorical
lda = LinearDiscriminantAnalysis(n_components=1)
    #select data
#lda_y = np.array2string(y_train)
#lda.fit(x_train, lda_y)
#LinearDiscriminantAnalysis(n_components=None, priors=None, shrinkage=None, solver='svd', store_covariance=False, tol=0.0001)
    #train model
#lda_x = lda.fit_transform(lda_x, lda_y)
    #performing lda
#lda_test = testing_data[:, 0:3]
    #training and making pred
#from sklearn.ensemble import RandomForestClassifier
#lda_classifier = RandomForestClassifier(max_depth=2, random_state=0)
#lda_classifier.fit(lda_x, lda_y)


#KNN Classifier - need to choose the number of neighbors k
neigh = KNeighborsClassifier(n_neighbors=3)
neigh_y = y_train.transpose()
#neigh.fit(x_train, neigh_y)

#Linear SVM - need to choose the margin penalty C as a hyperparameter

#Gaussian SVM - need to choose the margin penalty C and the radius width :symbol:

#Random Forest - need to choose the number of trees

#Gradient Boosted Decision Tree

#%% MachineLearningMastery Article


y_train = y_train.to_numpy()
y_train = y_train.ravel()

print(x_train.shape,y_train.shape)

from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score

cv = RepeatedStratifiedKFold(n_splits=8, n_repeats=3, random_state=1)

scores = cross_val_score(lda, x_train, y_train, scoring='accuracy', cv=cv, n_jobs=-1)

#print('Mean Accuracy: %.3f (%.3f)' %(mean(scores), std(scores)))