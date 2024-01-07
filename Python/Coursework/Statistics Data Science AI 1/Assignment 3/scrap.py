#%% Step 1 - import data with custom column names and dropping first column
import pandas as pd;
file_path = 'C:/Users/danma/Downloads/SouthGermanCredit.asc'
colnames=['status', 'duration', 'credit_history', 'purpose', 'amount', 'savings', 'employment_duration', 'installment_rate', 'personal_status_sex', 'other_debtors', 'present_residence', 'property', 'age', 'other_installment_plans', 'housing', 'number_credits', 'job', 'people_liable', 'telephone', 'foreign_worker', 'credit_risk'] 
df = pd.read_table(file_path, sep=" ", names=colnames)
df = df.iloc[1: , :]
df.dropna()

del file_path
#%% Step 2 - splits data into x and y

from sklearn.model_selection import train_test_split as TTS;

x = df.loc[:, df.columns != 'credit_risk']
y = df['credit_risk']
#turns y into a 1-d array instead of a dataframe column
y = y.to_numpy()
y = y.ravel()

#splits into training and test data
TS = 0.1 #for tuning
print("Test Size = ", TS, "\n")
x_train, x_test, y_train, y_test = TTS(x,y,test_size=TS, random_state=42)

#del df, file_path, colnames, x, y #clear data for variable explorer

print("Small Snippets\nX Test:\n",x_test,"Y Test",y_test)
del df, x, y
#%% Step 3 - logistic regression full set
print("Logistic Regression Results:")
from sklearn.linear_model import LogisticRegression;
from matplotlib import pyplot
#using newton-cg to mitigate error with number of samples on default
completemodel = LogisticRegression(solver='newton-cg').fit(x_train, y_train)

# Get Importance
importance = completemodel.coef_[0]
# summarize feature importance
for i,v in enumerate(importance):
	print(colnames[i],'Score: %.5f' % (v))
# plot feature importance
pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()

del i, v, importance

#Step 3 - create reduced model
x_train_reduced = x_train.drop(['duration', 'purpose', 'amount', 'present_residence', 'age'], axis=1)
x_test_reduced = x_test.drop(['duration', 'purpose', 'amount', 'present_residence', 'age'], axis=1)
reducedmodel = LogisticRegression(solver='newton-cg').fit(x_train_reduced, y_train)

#%% Step 4 - plot an ROC curve
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

print("\nComplete Model Accuracy: %.3f" %completemodel.score(x_test, y_test))

# predict probabilities
logreg_pred = completemodel.predict_proba(x_test)
# keep probabilities for the positive outcome only
logreg_pred = logreg_pred[:, 1]

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test.astype('int32'), logreg_pred)
LogReg_C = pyplot.plot(fpr, tpr, marker='.', label='Complete Logistic Regression ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, logreg_pred)
print('Complete AUC: %.3f' % auc)

#to create summary table at the end
from tabulate import tabulate

data = {'LogReg_C': [completemodel.score(x_test, y_test),auc]}
table = pd.DataFrame(data)


del fpr, tpr, auc, thresholds, logreg_pred

print("\nReduced Model Accuracy: %.3f" %reducedmodel.score(x_test_reduced, y_test))
# predict probabilities
logreg_pred = reducedmodel.predict_proba(x_test_reduced)
# keep probabilities for the positive outcome only
logreg_pred = logreg_pred[:, 1]

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test.astype('int32'), logreg_pred)
LogReg_R = pyplot.plot(fpr, tpr, marker='.', label='Reduced Logistic Regression ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, logreg_pred)
print('Reduced AUC: %.3f\n' % auc)

data = {'LogReg_R': [reducedmodel.score(x_test_reduced, y_test),auc]}
table['LogReg_R'] = pd.DataFrame(data)

del fpr, tpr, auc, thresholds, completemodel, reducedmodel, logreg_pred
#%% Step 5 - LDA
print("Linear Discriminant Analysis Results:")
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
#Model Summary
completelda = LinearDiscriminantAnalysis().fit(x_train, y_train)
importance = completelda.coef_[0]
for i,v in enumerate(importance):
	print(colnames[i],'Score: %.5f' % (v))
# plot feature importance
pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()

print("Shows that the coefficients are the same for LDA as in Logistic Regression, meaning we can use the same reduced model.")
del i, v, importance

reducedlda = LinearDiscriminantAnalysis().fit(x_train_reduced, y_train)
#ROC and AUC for complete and reduced
print("\nComplete LDA Model Accuracy: %.3f" %completelda.score(x_test, y_test))

# predict probabilities
logreg_pred = completelda.predict_proba(x_test)
# keep probabilities for the positive outcome only
logreg_pred = logreg_pred[:, 1]

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test.astype('int32'), logreg_pred)
pyplot.plot(fpr, tpr, marker='.', label='Complete LDA ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, logreg_pred)
print('Complete AUC: %.3f' % auc)

data = {'LDA_C': [completelda.score(x_test, y_test),auc]}
table['LDA_C'] = pd.DataFrame(data)

del fpr, tpr, auc, thresholds, logreg_pred

print("\nReduced LDA Model Accuracy: %.3f" %reducedlda.score(x_test_reduced, y_test))
# predict probabilities
logreg_pred = reducedlda.predict_proba(x_test_reduced)
# keep probabilities for the positive outcome only
logreg_pred = logreg_pred[:, 1]

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test.astype('int32'), logreg_pred)
pyplot.plot(fpr, tpr, marker='.', label='Reduced LDA ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, logreg_pred)
print('Reduced AUC: %.3f\n' % auc)

data = {'LDA_R': [reducedlda.score(x_test_reduced, y_test),auc]}
table['LDA_R'] = pd.DataFrame(data)
del fpr, tpr, auc, thresholds, logreg_pred, completelda, reducedlda
#%% Step 6 QDA
print("Quadratic Discriminant Analysis Results:")
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
#Model Summary
completeqda = QuadraticDiscriminantAnalysis().fit(x_train, y_train)
print("Cannot show coef results because QDA does not have the attributing function.")

reducedqda = QuadraticDiscriminantAnalysis().fit(x_train_reduced, y_train)
#ROC and AUC for complete and reduced
print("\nComplete QDA Model Accuracy: %.3f" %completeqda.score(x_test, y_test))

# predict probabilities
logreg_pred = completeqda.predict_proba(x_test)
# keep probabilities for the positive outcome only
logreg_pred = logreg_pred[:, 1]

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test.astype('int32'), logreg_pred)
QDA_C = pyplot.plot(fpr, tpr, marker='.', label='Complete QDA ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, logreg_pred)
print('Complete AUC: %.3f' % auc)
data = {'QDA_C': [completeqda.score(x_test, y_test),auc]}
table['QDA_C'] = pd.DataFrame(data)
del fpr, tpr, auc, thresholds, logreg_pred

print("\nReduced QDA Model Accuracy: %.3f" %reducedqda.score(x_test_reduced, y_test))
# predict probabilities
logreg_pred = reducedqda.predict_proba(x_test_reduced)
# keep probabilities for the positive outcome only
logreg_pred = logreg_pred[:, 1]

# calculate roc curve
fpr, tpr, thresholds = roc_curve(y_test.astype('int32'), logreg_pred)
QDA_R = pyplot.plot(fpr, tpr, marker='.', label='Reduced QDA ROC')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()

# calculate AUC
auc = roc_auc_score(y_test, logreg_pred)
print('Reduced AUC: %.3f\n' % auc)
data = {'QDA_R': [reducedqda.score(x_test_reduced, y_test),auc]}
table['QDA_R'] = pd.DataFrame(data)
del fpr, tpr, auc, thresholds, logreg_pred, completeqda, reducedqda
#%% Step 7 Comparison
print(tabulate(table, headers='keys',tablefmt='fancy_grid',showindex=["Accuracy","AUC"]))
fig = pyplot.figure()
ax = fig.add_subplot(111)
ax.add_line(LogReg_C)
LogReg_C
LogReg_R
QDA_C
QDA_R
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
# show the plot
pyplot.show()