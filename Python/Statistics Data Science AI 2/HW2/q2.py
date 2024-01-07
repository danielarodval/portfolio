# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 23:04:12 2022

@author: Daniel Rodriguez
"""

#%% Step 1- imports data into dataframe
import pandas as pa;
import timeit;

col_names=['fLength', 'fWidth', 'fSize', 'fConc', 'fConc1', 'fAsym', 'fM3Long', 'fM3Trans', 'fAlpha', 'fDist', 'class']
df = pa.read_table('C:/Users/danma/Documents/STA 4365/HW2/magic04.data', sep=',', header=None, names=col_names)
print(df.head())

#%% Step 2 - splits data into x and y

from sklearn.model_selection import train_test_split as TTS

x = df.filter(regex='f')
y = df.filter(regex='class')
#repace categorical data characters with 1 and 0, 1 to separate from 0
y = y.replace('g',1, regex=True)
y = y.replace('h',0, regex=True)
#turns y into a 1-d array instead of a dataframe column
y = y.to_numpy()
y = y.ravel()
y = y.astype('int')

#splits into training and test data
TS = 0.1 #for tuning
print("Test Size = ", TS, "\n")
x_train, x_test, y_train, y_test = TTS(x,y,test_size=TS, random_state=42)

del df, col_names, TS

#%% Step 3 - scale and center columns

from sklearn.preprocessing import StandardScaler

scalar = StandardScaler()
scalar.fit(x_train)

x_train = scalar.transform(x_train)
x_test = scalar.transform(x_test)

del scalar

#To tune hyperparameters for each model, you can either use cross-validation or hand-tune by examining
#the model performance for reasonable values of the hyper-parameters.
from sklearn.model_selection import GridSearchCV
# Apply your models to the test set. Report the accuracy, visualize an ROC curve, and report the AUC
#for each model. For Logistic Regression, Random Forests, and Gradient Boosted Decision Trees, report
#the most meaningful predictors.
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot
from sklearn.metrics import RocCurveDisplay

#%% Step 4 - Logistic Regression
print("Logistic Regression Results:")
from sklearn.linear_model import LogisticRegression

#%% Step 4.1 Tuning Hyperparameters - Did not provide change in accuracy nor auc
#start = timeit.default_timer()

#list hyperparameters that we want to tune
#multi_class = ['auto', 'ovr', 'multinomial'] #original run
#multi_class = ['multinomial']
#solver = ['newton-cg', 'lbfgs','liblinear', 'saga', 'sag'] #original run
#solver = ['newton-cg']
#convert to dictionary
#log_hyper = dict(solver=solver, multi_class=multi_class)
#Create new reg object
#logreg_2 = LogisticRegression(max_iter=50000)
#use gridsearch
#grid = GridSearchCV(logreg_2, log_hyper, cv=10, scoring='accuracy', verbose=1)
#best_logreg = grid.fit(x, y)

#print('Best multi_class:', best_logreg.best_estimator_.get_params()['multi_class'])
#print('Best solver:', best_logreg.best_estimator_.get_params()['solver'])

#stop = timeit.default_timer()
#print('Time: %.2f' %(stop-start), '\n')

#Did not provide change in accuracy nor auc
#%%
#fit the model
logreg = LogisticRegression()
logreg.fit(x_train, y_train)

# predict probabilities
logreg_pred = logreg.predict_proba(x_test)
# keep probabilities for the positive outcome only
logreg_pred = logreg_pred[:, 1]

#print accuracy of the model
print("Accuracy: %.3f" %logreg.score(x_test, y_test))

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test, logreg_pred)
pyplot.plot(fpr, tpr, marker='.', label='Logistic Regression ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, logreg_pred)
print('AUC: %.3f\n' % auc)

del logreg, logreg_pred, fpr, tpr, thresholds, auc

#%% Step 5 - LDA
print("Linear Discriminant Analysis Results:")
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

#%% Step 5.1 Tune Hyperparameters for LDA

#%%
#fit the model
lda = LinearDiscriminantAnalysis()
lda.fit(x_train, y_train)

#predict probabilities
lda_pred = lda.predict_proba(x_test)
# keep probabilities for the positive outcome only
lda_pred = lda_pred[:, 1]
#print accuracy of the model
print("Accuracy: %.3f" %lda.score(x_test, y_test))

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test, lda_pred)
pyplot.plot(fpr, tpr, marker='.', label='LDA ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, lda_pred)
print('AUC: %.3f\n' % auc)

del lda, lda_pred, fpr, tpr, thresholds, auc
#%% Step 6 - KNN Classifier
print("KNN Classifier Results:")
from sklearn.neighbors import KNeighborsClassifier

#fit the model
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(x_train, y_train)

#predict probabilities
neigh_pred = neigh.predict_proba(x_test)
# keep probabilities for the positive outcome only
neigh_pred = neigh_pred[:, 1]
#print accuracy of the model
print("Accuracy: %.3f" %neigh.score(x_test, y_test))

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test, neigh_pred)
pyplot.plot(fpr, tpr, marker='.', label='KNN ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, neigh_pred)
print('AUC: %.3f\n' % auc)

#Need to choose the number of neighbors k
del neigh, neigh_pred, fpr, tpr, thresholds, auc
#%% Step 7 - Linear SVM
print("Linear SVM Results:")
from sklearn.svm import SVC

#Need to choose the margin penalty C as a hyperparameter

#fit the model
lin_svm = SVC(kernel='linear')
lin_svm.fit(x_train,y_train)

#predict probabilities
lin_svm_y_pred = lin_svm.predict(x_test)

#print accuracy of the model
print("Accuracy: %0.3f" %lin_svm.score(x_test, y_test))

#roc curve
svc_disp = RocCurveDisplay.from_predictions(y_test, lin_svm_y_pred, name="Linear SVM ROC")
pyplot.show()

from sklearn import metrics

#auc score
fpr, tpr, threshold = metrics.roc_curve(y_test, lin_svm_y_pred)
score = metrics.auc(fpr, tpr)
print("AUC: %0.3f \n" %score)

del lin_svm, lin_svm_y_pred, svc_disp, fpr, tpr, threshold

#%% Step 8 - Gaussian SVM
print("Gaussian SVM Results:")
from sklearn.svm import SVC

#Need to choose the margin penalty C and the radius width γ.

#fit the model
gau_svm = SVC(kernel='rbf')
gau_svm.fit(x_train,y_train)

#predict probabilities
gau_svm_y_pred = gau_svm.predict(x_test)

#print accuracy of the model
print("Accuracy: %0.3f" %gau_svm.score(x_test, y_test))

#roc curve
svc_disp = RocCurveDisplay.from_predictions(y_test, gau_svm_y_pred, name="Gaussian SVM ROC")
pyplot.show()

#auc score
fpr, tpr, threshold = metrics.roc_curve(y_test, gau_svm_y_pred)
score = metrics.roc_auc_score(y_test, gau_svm_y_pred)
print("AUC: %0.3f \n" %score)

del gau_svm, gau_svm_y_pred, score, svc_disp, fpr, tpr, threshold

#%% Step 9 - Random Forest
print("Random Forest Results:")
from sklearn.ensemble import RandomForestClassifier

#Need to choose the number of trees.

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

#%% Step 10 - Gradient Boosted Decision Tree
print("Gradient Boosted Results:")
from sklearn.ensemble import GradientBoostingClassifier

# Need to choose the number of trees and learning rate. 
#If you want, you can also experiment with randomly selecting 
#rows and columns when growing each tree.

#fit the model
gb = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
gb.fit(x_train, y_train)

#predict probabilities
gb_pred = gb.predict_proba(x_test)
# keep probabilities for the positive outcome only
gb_pred = gb_pred[:, 1]

#print accuracy of the model
print("Accuracy: %0.3f" %gb.score(x_test, y_test))

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test, gb_pred)
pyplot.plot(fpr, tpr, marker='.', label='Gradient Boosted ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, gb_pred)
print('AUC: %.3f\n' % auc)

del gb, gb_pred, fpr, tpr, thresholds, auc

#%% Run sound when code is done
import winsound
duration = 1000 #milliseconds
freq = 440 #hz
winsound.Beep(freq, duration)

del duration, freq