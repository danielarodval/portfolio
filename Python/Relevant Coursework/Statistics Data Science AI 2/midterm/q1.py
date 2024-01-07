# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 20:02:06 2022

@author: danma
"""

#%% Step 1 Imports data into pandas dataframe
import pandas as pa

col_names=['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']
df = pa.read_table('C:/Users/danma/Documents/STA 4365/midterm/adult.data', sep=',', header=None, names=col_names)
print(df.head())

del col_names
#%% Step 2 splits data into x and y

from sklearn.model_selection import train_test_split

x = df.drop(['income'], axis=1)
y = df.iloc[: , -1]
#replace categorical last column data with 1 and 0
y = y.replace('<=50K',0, regex=True)
y = y.replace('>50K',1, regex=True)

#formats x categorical data into integers for scaling
from sklearn.preprocessing import OrdinalEncoder

#converts x into integers
ord_enc = OrdinalEncoder()
x["workclass"] = ord_enc.fit_transform(x[["workclass"]])
x["education"] = ord_enc.fit_transform(x[["education"]])
x["marital-status"] = ord_enc.fit_transform(x[["marital-status"]])
x["occupation"] = ord_enc.fit_transform(x[["occupation"]])
x["relationship"] = ord_enc.fit_transform(x[["relationship"]])
x["race"] = ord_enc.fit_transform(x[["race"]])
x["sex"] = ord_enc.fit_transform(x[["sex"]])
x["native-country"] = ord_enc.fit_transform(x[["native-country"]])

#turns y into a 1-d array instead of a dataframe column
y = y.to_numpy()
y = y.ravel()
y = y.astype('int')

#splits into training and testing data
TS = 0.2
print("Test Size = ", TS, "\n")
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=TS, random_state=42)

del ord_enc, df, x, y

#%% Step 3 scale and center columns

from sklearn.preprocessing import StandardScaler

#scaling for the final tests a.k.a. the TTS tests
scalar = StandardScaler()
scalar.fit(x_train)

x_train = scalar.transform(x_train)
x_test = scalar.transform(x_test)

del scalar

#import plotting and testing
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from matplotlib import pyplot
from sklearn.metrics import RocCurveDisplay

#%% Step 4 Linear Support Vector Machine
print("Linear SVM Results:")
from sklearn.svm import SVC

#%% Step 4.1 Tune Hyperparameters for Linear Support Vector Machine
print("Linear SVM Hyperparameters:")
#list hyperparameters that we want to tune
# defining parameter range
param_grid = {'C': [0.1, 1, 10, 100],
              'gamma': [1, 0.1, 0.01, 0.001, 'scale', 'auto'],
              'kernel': ['linear']}

grid = GridSearchCV(SVC(), param_grid, verbose = 2, n_jobs=-1)

# fitting the model for grid search
best = grid.fit(x_train, y_train)
#print the values of the best hyperparameters
print('Best C:', best.best_estimator_.get_params()['C'])
print('Best gamma:', best.best_estimator_.get_params()['gamma'])
print('Best kernel:', best.best_estimator_.get_params()['kernel'])

del param_grid, grid, best
#%% Step 4.2 Run model with best hyperparameters

#fit the model
lin_svm = SVC(kernel='linear', C=100, gamma=0.01)
lin_svm.fit(x_train, y_train)

#predict probabilities
lin_svm_pred = lin_svm.predict(x_test)

#print accuracy of the model
print("Accuracy: %0.3f" %lin_svm.score(x_test, y_test))

#roc curve
svc_disp = RocCurveDisplay.from_predictions(y_test, lin_svm_pred, name="Linear SVM ROC")
pyplot.show()

#auc score
fpr, tpr, threshold = metrics.roc_curve(y_test, lin_svm_pred)
score = metrics.auc(fpr, tpr)
print("AUC: %0.3f \n" %score)

del lin_svm, lin_svm_pred, svc_disp, fpr, tpr, threshold, score

#%% Step 5 Support Vector Machine with Gaussian Kernel
print("Gaussian SVM Results:")

#%% Step 5.1 Tune Hyperparameters for Gaussian Support Vector Machine
print("Gaussian SVM Hyperparameters:")
#list hyperparameters that we want to tune
# defining parameter range
param_grid = {'C': [0.1, 1, 10, 100, 500],
              'gamma': [1, 0.1, 0.01, 0.001, 'scale', 'auto'],
              'kernel': ['rbf']}

#use gridsearch
grid = GridSearchCV(SVC(), param_grid, verbose = 2, n_jobs=-1)

# fitting the model for grid search
best = grid.fit(x_train, y_train)
#print the values of the best hyperparameters
print('Best C:', best.best_estimator_.get_params()['C'])
print('Best gamma:', best.best_estimator_.get_params()['gamma'])
print('Best kernel:', best.best_estimator_.get_params()['kernel'])

del param_grid, grid, best
#%% 5.2 Run Model with best hyperparameters

#fit the model
gau_svm = SVC(kernel='rbf', C=100, gamma=0.01)
gau_svm.fit(x_train, y_train)

#predict probabilities
gau_svm_pred = gau_svm.predict(x_test)

#print accuracy of the model
print("Accuracy: %0.3f" %gau_svm.score(x_test, y_test))

#roc curve
svc_disp = RocCurveDisplay.from_predictions(y_test, gau_svm_pred, name="Linear SVM ROC")
pyplot.show()

#auc score
fpr, tpr, threshold = metrics.roc_curve(y_test, gau_svm_pred)
score = metrics.auc(fpr, tpr)
print("AUC: %0.3f \n" %score)

del gau_svm, gau_svm_pred, svc_disp, fpr, tpr, threshold, score

#%% Step 6 Random Forest
print("Random Forest Results:")
from sklearn.ensemble import RandomForestClassifier

#%% Step 6.1 Tune Hyperparameters for Random Forest
print("Random Forest Hyperparameters:")
#list hyperparameters that we want to tune
#defining parameter range
param_grid = {'bootstrap': [True],
    'max_depth': [5, 10, 80, 90, 100, 110],
    'max_features': ["sqrt", "log2"],
    'min_samples_leaf': [3, 4, 5],
    'min_samples_split': [8, 10, 12],
    'n_estimators': [5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 100, 200, 300, 1000]}

grid = GridSearchCV(RandomForestClassifier(), param_grid, verbose=3)

# fitting the model for grid search
best = grid.fit(x_train, y_train)
#print the values of the best hyperparameters
print('Best bootstrap:', best.best_estimator_.get_params()['bootstrap'])
print('Best max_depth:', best.best_estimator_.get_params()['max_depth'])
print('Best max_features:', best.best_estimator_.get_params()['max_features'])
print('Best min_samples_leaf:', best.best_estimator_.get_params()['min_samples_leaf'])
print('Best min_samples_split:', best.best_estimator_.get_params()['min_samples_split'])
print('Best n_estimators:', best.best_estimator_.get_params()['n_estimators'])

del param_grid, grid, best
#%% Step 6.2 Run model with best hyperparameters

#fit the model
rf = RandomForestClassifier()
rf.fit(x_train,y_train)

#predict probabilities
rf_y_pred = rf.predict(x_test)

#print accuracy of the model
print("Accuracy: %0.3f" %rf.score(x_test, y_test))

#roc curve
fpr, tpr, thresholds = metrics.roc_curve(y_test, rf_y_pred)
roc_auc = metrics.auc(fpr, tpr)
display = metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name='Random Forest ROC')
display.plot()

pyplot.show()

#auc score
print("AUC: %0.3f \n" %roc_auc)

del rf, rf_y_pred, fpr, tpr, thresholds, roc_auc, display

#%% Step 7 Gradient Boosted Decision Tree
print("Gradient Boosted Decision Tree")
from sklearn.ensemble import GradientBoostingClassifier

#%% Step 7.1 Tune Hyperparameters for Gradient Boosted Decision Tree Regression
print("GradientBoosted Hyperparameters")

#List hyperparameters we want to tune
param_grid = {'learning_rate': [0.01, 0.02, 0.03, 0.04],
              'subsample': [0.9, 0.5, 0.2, 0.1],
              'n_estimators': [100,200,300, 500, 1000, 1500],
              'max_depth': [4,6,8,10]}

#use gridsearch
grid = GridSearchCV(GradientBoostingClassifier(), param_grid, verbose = 2, n_jobs=-1)
# fitting the model for grid search
best = grid.fit(x_train, y_train)
#print the values of the best hyperparameters
print('Best learning_rate:', best.best_estimator_.get_params()['learning_rate'])
print('Best subsample:', best.best_estimator_.get_params()['subsample'])
print('Best n_estimators:', best.best_estimator_.get_params()['n_estimators'])

del param_grid, grid, best

#%% Step 7.2 Run the model with the best hyperparameters
gb = GradientBoostingClassifier(learning_rate=.02, subsample=.2, n_estimators=300, max_depth=8)
#fit the model
gb.fit(x_train, y_train)
#predict probabilities
gb_pred = gb.predict_proba(x_test)
# keep probabilities for the positive outcome only
gb_pred = gb_pred[:, 1]
#print accuracy of the model
print("Accuracy: %0.3f" %gb.score(x_test, y_test))
# calculate roc curve
fpr, tpr, thresholds = metrics.roc_curve(y_test, gb_pred)
pyplot.plot(fpr, tpr, marker='.', label='Gradient Boosted ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = metrics.roc_auc_score(y_test, gb_pred)
print('AUC: %.3f\n' % auc)

del gb, gb_pred, fpr, tpr, thresholds, auc
#%% Run sound when code is done
import winsound
duration = 1000 #milliseconds
freq = 440 #hz
winsound.Beep(freq, duration)

del duration, freq