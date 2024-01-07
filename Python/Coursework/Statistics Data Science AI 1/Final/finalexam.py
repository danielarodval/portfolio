# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 00:38:57 2022

@author: danma
"""

#%% Step 1 - Load Data
import pandas as pd
file_path = 'C:/Users/danma/Downloads/bank_data.csv'
df = pd.read_table(file_path, sep=",")

del file_path
#create x and y columns
x = df.drop(['y'],axis=1)
y = df['y']

#create categorical columns for x
x = pd.get_dummies(x)

#convert y into binary 1 or 0
from sklearn.preprocessing import OrdinalEncoder
enc = OrdinalEncoder()
y = enc.fit_transform(y.to_frame())
y = pd.DataFrame(y, columns = ["y"])
df = pd.concat([x, y], axis=1)
#turns y into a 1-d array instead of a dataframe column for logistic regression
y = y.to_numpy()
y = y.ravel()
del enc

#splits into training and test data
from sklearn.model_selection import train_test_split as TTS
TS = 0.25 #for tuning
print("Test Size = ", TS, "\n")
train, test = TTS(df, test_size=0.25)
x_train = train.loc[:, df.columns != 'y']
y_train = train['y']
x_test = test.loc[:, df.columns != 'y']
y_test = test['y']

#fit model
from sklearn.linear_model import LogisticRegression

completemodel = LogisticRegression(max_iter=5000).fit(x,y)

from matplotlib import pyplot

# Get Importance
importance = completemodel.coef_[0]

colnames = list(x_train.columns)
# summarize feature importance
for i,v in enumerate(importance):
	print(colnames[i],'Score: %.5f' % (abs((v))))
# plot feature importance
pyplot.bar([x for x in range(len(importance))], abs(importance))
pyplot.show()
del importance, i, v, colnames
#%% Fitting Reduced Model
red_train = train.drop(['age','balance','day','duration','pdays','previous'],axis=1)
red_test =  test.drop(['age','balance','day','duration','pdays','previous'],axis=1)

red_x_train = red_train.loc[:, red_train.columns != 'y']
red_x_test = red_test.loc[:, red_test.columns != 'y']

reducedmodel = LogisticRegression(max_iter=5000).fit(red_x_train,y_train)
completemodel = LogisticRegression(max_iter=5000).fit(x_train,y_train)

from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

#Complete Model Training
comp_train_pred = completemodel.predict(x_train)
# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_train.astype('int32'), comp_train_pred)
pyplot.plot(fpr, tpr, marker='.', label='Complete Train ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

#to create summary table at the end
from tabulate import tabulate

data = {'Complete Train': [roc_auc_score(y_train.astype('int32'), comp_train_pred)]}
table = pd.DataFrame(data)

#Complete Model Testing
comp_test_pred = completemodel.predict(x_test)
# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test.astype('int32'), comp_test_pred)
pyplot.plot(fpr, tpr, marker='.', label='Complete Test ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

data = {'Complete Test': [roc_auc_score(y_test.astype('int32'), comp_test_pred)]}
table['Complete Test'] = pd.DataFrame(data)

#Reduced Model Training
red_train_pred = reducedmodel.predict(red_x_train)
# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_train.astype('int32'), red_train_pred)
pyplot.plot(fpr, tpr, marker='.', label='Reduced Train ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

data = {'Reduced Train': [roc_auc_score(y_train.astype('int32'), red_train_pred)]}
table['Reduced Train'] = pd.DataFrame(data)

#Reduced Model Testing
red_test_pred = reducedmodel.predict(red_x_test)
# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test.astype('int32'), comp_test_pred)
pyplot.plot(fpr, tpr, marker='.', label='Reduced Test ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

data = {'Reduced Test': [roc_auc_score(y_test.astype('int32'), red_test_pred)]}
table['Reduced Test'] = pd.DataFrame(data)

print("\n\nAUC Score Results:\n")

print(tabulate(table, headers='keys',tablefmt='fancy_grid',showindex=["AUC"]))

del comp_test_pred, comp_train_pred, fpr, red_test_pred, red_train_pred, thresholds, tpr, data, table, red_test, red_train, red_x_train, red_x_test, completemodel, reducedmodel
#%% Create LASSO Model
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import validation_curve
import numpy as np
list_alphas = np.logspace(-3,3,20)

train_scores, valid_scores = validation_curve(
    LogisticRegression(penalty='l1', max_iter=5000,solver='liblinear',), x, y, param_name="C", param_range=list_alphas,
    cv=10,
    n_jobs=-1)
lasso = LogisticRegressionCV(penalty='l1', cv=10, n_jobs=-1, max_iter=5000,solver='liblinear', Cs=list_alphas).fit(x,y)
from matplotlib import pyplot as plt
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(valid_scores, axis=1)
test_scores_std = np.std(valid_scores, axis=1)

plt.title("Validation Curve with Logistic Regression")
plt.xlabel(r"$\lambda$^-1")
plt.ylabel("Score")
plt.ylim(0.0, 1.1)
lw = 2
plt.semilogx(
    list_alphas, train_scores_mean, label="Training score", color="darkorange", lw=lw
)
plt.fill_between(
    list_alphas,
    train_scores_mean - train_scores_std,
    train_scores_mean + train_scores_std,
    alpha=0.2,
    color="darkorange",
    lw=lw,
)
plt.semilogx(
    list_alphas, test_scores_mean, label="Cross-validation score", color="navy", lw=lw
)
plt.fill_between(
    list_alphas,
    test_scores_mean - test_scores_std,
    test_scores_mean + test_scores_std,
    alpha=0.2,
    color="navy",
    lw=lw,
)
plt.legend(loc="best")
plt.show()

print("LASSO optimal λ = ",lasso.C_)

from matplotlib import pyplot

# Get Importance
importance = lasso.coef_[0]

colnames = list(x_train.columns)
# summarize feature importance
for i,v in enumerate(importance):
	print(colnames[i],'Score: %.5f' % (abs((v))))
# plot feature importance
pyplot.bar([x for x in range(len(importance))], abs(importance))
pyplot.show()
del importance, i, v, colnames

from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

#Complete Model Training
comp_train_pred = lasso.predict(x_train)
# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_train.astype('int32'), comp_train_pred)
pyplot.plot(fpr, tpr, marker='.', label='LASSO Train ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

#to create summary table at the end
from tabulate import tabulate

data = {'LASSO Train': [roc_auc_score(y_train.astype('int32'), comp_train_pred)]}
table = pd.DataFrame(data)

#Complete Model Testing
comp_test_pred = lasso.predict(x_test)
# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test.astype('int32'), comp_test_pred)
pyplot.plot(fpr, tpr, marker='.', label='LASSO Test ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

data = {'LASSO Test': [roc_auc_score(y_test.astype('int32'), comp_test_pred)]}
table['LASSO Test'] = pd.DataFrame(data)

print("\n\nAUC Score Results:\n")

print(tabulate(table, headers='keys',tablefmt='fancy_grid',showindex=["AUC"]))