# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 21:07:56 2022

@author: danma
"""

#%% Step 1 - Load Data & Prep Data
import pandas as pd;

x = pd.read_table('C:/Users/danma/Downloads/gene_data.csv', sep=",",)
y = pd.read_table('C:/Users/danma/Downloads/gene_labels.csv', sep=",",)

#possibly remove sample name column
x = x.iloc[: , 1:]
y = y.iloc[: , 1:]
 
from sklearn.preprocessing import OrdinalEncoder
enc = OrdinalEncoder()
y = enc.fit_transform(y)
y = pd.DataFrame(y, columns = ["Class"])

print(x.head())
print(y.head())
#%% Step 2 - Remove Variance < 0.001
from sklearn.feature_selection import VarianceThreshold

selector = VarianceThreshold(threshold = 0.001)
selector.fit(x)

concol = [column for column in x.columns 
          if column not in x.columns[selector.get_support()]]

print("Columns with Variance < 0.001")
for features in concol:
    print(features)
    
x_reduced = x.drop(concol,axis=1)

del concol, selector, features
#%% Step 3 - Standardize the Data
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x_reduced)

x_scaled = pd.DataFrame(x_scaled, columns = x_reduced.columns)#return to dataframe with column names

del x_reduced, scaler, x
#%% Step 4 - Split Data
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y)
print(x_train.dtypes)
del y
#%% Step 4.5 Testing Logistic Regression and RidgeClassification to ensure that they yield the same results, which they did meaning that Ridge as a package alone works for L2 Regularization while running quicker than both.
#from sklearn.linear_model import LogisticRegressionCV

#clf = LogisticRegressionCV(cv=10, random_state=0, Cs=list_alphas, penalty="l2", solver="saga", n_jobs=-1, multi_class="multinomial", max_iter=5000).fit(x_train, y_train.values.ravel())
#print(clf.Cs)

#y_ridge_pred = clf.predict(x_test)  
#from sklearn.linear_model import RidgeClassifierCV
#list_alphas = [1e-15, 1e-10, 1e-8, 1e-5, 1e-4, 1e-3,1e-2, 1e-1, 1, 5, 10, 20]
#clf = RidgeClassifierCV(cv=10, alphas=list_alphas).fit(x_train, y_train.values.ravel())
#print("Ridge optimal λ = ",clf.alpha_)

#y_ridge_pred = clf.predict(x_test)

#from sklearn.metrics import confusion_matrix
#using ravel to create single array and round to create classifier prediction for confusion matrix
#print(confusion_matrix(y_test.values.ravel(),y_ridge_pred.round(0)))
#matrix shows exact match

#%% Step 5 - Ridge Regression, 10 Fold, Optimal Lambda, Confusion Matrix Accuracy
from sklearn.linear_model import RidgeCV
import numpy as np
#list_alphas = np.logspace(-15, 1.35, 400) ran large range but defaulted at the 1e-15 after a 5 min run
list_alphas = [1e-15, 1e-10, 1e-8, 1e-5, 1e-4, 1e-3,1e-2, 1e-1, 1, 5, 10, 20]
clf = RidgeCV(cv=10, alphas=list_alphas).fit(x_train, y_train.values.ravel())
print("Ridge optimal λ = ",clf.alpha_)

y_ridge_pred = clf.predict(x_test)

from sklearn.metrics import confusion_matrix
#using ravel to create single array and round to create classifier prediction for confusion matrix
cm = confusion_matrix(y_test.values.ravel(),y_ridge_pred.round(0))
print(cm)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay.from_predictions(y_test.values.ravel(),y_ridge_pred.round(0))
disp.ax_.set_title("Ridge Confusion Matrix")

#%% Step 6 - LASSO Regression, 10 Fold, Optimal Lambda, Confusion Matrix Accuracy
from sklearn.linear_model import LassoCV
list_alphas = np.logspace(-15, 1.35, 400)
reg = LassoCV(cv=10, alphas=list_alphas, n_jobs=-1, positive=True).fit(x_train, y_train.values.ravel())
print("LASSO optimal λ = ",reg.alpha_)

y_lasso_pred = reg.predict(x_test)

cm = confusion_matrix(y_test.values.ravel(),y_lasso_pred.round(0))
print(cm)
#matrix shows incorrect guesses and a wider range
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay.from_predictions(y_test.values.ravel(),y_lasso_pred.round(0))
disp.ax_.set_title("LASSO Confusion Matrix")
#%% Step 7 - 20 Most Relevant Predictors from LASSO
#%% Step 7.1 - Fitting Logistic Regression to get Coef for all Tumors
from sklearn.linear_model import LogisticRegression
#fitting Logistic Regression for All Coefficients
lasso = LogisticRegression(C=(1/reg.alpha_), penalty="l1", solver="saga", n_jobs=-1, max_iter=5000)
lasso.fit(x_train, y_train.values.ravel())

y_pred = lasso.predict(x_test)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay.from_predictions(y_test.values.ravel(),y_pred)
disp.ax_.set_title("Logistic(L1) Confusion Matrix")

#%% Step 7.2 - Pull Coefficient Matrix from Logistic Regression
imp = lasso.coef_
imp = imp.transpose()
#%% Step 7.3 - Coefficients from LASSO model
import numpy as np
importance = pd.DataFrame({'gene': reg.feature_names_in_, 'coef': reg.coef_}, columns=['gene', 'coef'])
importancesorted = importance.sort_values(by=['coef'], ascending=False)
top20 = importancesorted.head(20)
print("Top 20 Most Relevant Genes from LASSO:\n")
from tabulate import tabulate
print(tabulate(top20, headers='keys', tablefmt='fancy_grid', showindex=False))
#%% Step 8 - Relation of Genes to Tumors
#%% Step 8.1 - Top20(LASSO) from LogReg
cat = enc.categories_[0]
importance[enc.categories_[0]] = imp
importancesorted = importance.sort_values(by=['coef'], ascending=False)
top20 = importancesorted.head(20)
print("Top 20 Most Relevant Genes from LASSO with Coefficients from LogReg(L1):\n")
from tabulate import tabulate
print(tabulate(top20, headers='keys', tablefmt='fancy_grid', showindex=False))
#%% Step 8.2 - Relation
#swap negatives for low, positives for high, zeros for none
values = top20.iloc[: , -5:]
values[values < 0] = -1
values[values > 0] = 1

mapping = {1:'high prob', -1:'low prob', 0:'no relation'}
values = values.astype(int).replace({'BRCA': mapping, 'COAD': mapping, 'KIRC': mapping, 'LUAD': mapping, 'PRAD': mapping})
#drop coef column, and print new dataframe with labels rather than numerical coef
values.insert (0, 'gene', top20['gene'])

from tabulate import tabulate
print(tabulate(values, headers='keys', tablefmt='fancy_grid', showindex=False))