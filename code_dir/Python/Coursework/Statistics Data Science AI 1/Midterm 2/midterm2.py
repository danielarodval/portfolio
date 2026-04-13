#%% Step 1 - Load and Clean Data
import pandas as pd;
#temp names to better work with OLS logistic regression ouput
colnames=['row','response', 'a', 'b', 'c', 'd', 'e', 'f', 'g','h', 'i'] 
file_path = 'C:/Users/danma/Downloads/midterm_data_2.csv'
df = pd.read_table(file_path, sep=",",names=colnames)
df = df.iloc[1: , :]
df = df.loc[:, df.columns != 'row']
del file_path

#get median from columns after dropping NA
nan_values = df[df.isna().any(axis=1)]
print("\nFinding NaN values that have to be replaced in the dataframe")
print(nan_values)
print("\nAfter printing we can see that feat.b and feat.d are only rows with nan values. So we take the median of the dropped NA dataframe and fill those nan with medians.")
df_no_NA = df.dropna()
#go back on original and load NAs with Median Value
values = {"b": df_no_NA["b"].median(), "d": df_no_NA["d"].median()}
df = df.fillna(value=values)
#reassign values
df[['d','response']] = df[['d','response']].astype(int)
df[['a','b','e','f','h','i']] = df[['a','b','e','f','h','i']].astype(float)
del df_no_NA, nan_values, values
#%% Step 2 - Format feat.c and feat.g as Categorical
from sklearn.preprocessing import OneHotEncoder;
oe = OneHotEncoder()
#encode C
encoded_C = oe.fit_transform(df[["c"]])
encoded_C = pd.DataFrame(encoded_C.toarray(),columns=["c_a","c_b","c_c","c_d"])
df = df.join(encoded_C,how='left')
#encode G
encoded_G = oe.fit_transform(df[["g"]])
encoded_G = pd.DataFrame(encoded_G.toarray(),columns=["g_x","g_y","g_z"])
df = df.join(encoded_G,how='left')
#drop original categorical columns
df = df.loc[:, df.columns != "c"]
df = df.loc[:, df.columns != "g"]
#drops na values
df = df.dropna()
print("\nFinal Data Frame (after encoding categorical columns):\n",df.head())
del encoded_C, encoded_G, oe
#%% Step 3 - Split Data
#split into  and Y
x = df.loc[:, df.columns != 'response']
y = df['response']
#turns y into a 1-d array instead of a dataframe column for logistic regression
y = y.to_numpy()
y = y.ravel()
#split into train test split
from sklearn.model_selection import train_test_split as TTS;
TS = 0.25 #for tuning
print("\nTest Size = ", TS, "\n")
train, test = TTS(df, test_size=0.25)
x_train = train.loc[:, df.columns != 'response']
y_train = train['response']
x_test = test.loc[:, df.columns != 'response']
y_test = test['response']
#%% Step 4 - Create Full and Reduced Model
print("Complete Logistic Regression Feature Importance:")
from sklearn.linear_model import LogisticRegression;
from matplotlib import pyplot
#using newton-cg to mitigate error with number of samples on default
completemodel = LogisticRegression(max_iter=5000).fit(x_train, y_train)

from sklearn.feature_selection import RFE
rfe = RFE(completemodel, n_features_to_select=7)
rfe.fit(x, y)
print("\nFeature Importance Ranking\n\n")
print(rfe.support_)

# Get Importance
importance = completemodel.coef_[0]

colnames = list(x_train.columns)
# summarize feature importance
for i,v in enumerate(importance):
	print(colnames[i],'Score: %.5f' % (abs((v))))
# plot feature importance
pyplot.bar([x for x in range(len(importance))], abs(importance))
pyplot.show()

del i, v, importance, colnames, rfe
#%% Step 5 - Create Linear Model and Show Summary Screen
import statsmodels.api as sm;

completemodel = sm.Logit(y_train,x_train).fit()
print(completemodel.summary())
#%% Step 6 - Create a Reduced Model
import statsmodels.formula.api as smf

reducedmodel = smf.logit('response ~ d + e + f + i', data=train).fit()
print(reducedmodel.summary())
#%% Step 7 - Create ROC Curve 
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
red_train_pred = reducedmodel.predict(x_train)
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
red_test_pred = reducedmodel.predict(x_test)
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

del comp_test_pred, comp_train_pred, fpr, red_test_pred, red_train_pred, thresholds, tpr, data, table

#%% Step 8 - Threshold Comparison
from sklearn.metrics import accuracy_score
# Predicted probability
y_predict_prob = reducedmodel.predict(x_test)
print("Define threshold 0.5")
y_predict_class = [1 if prob > 0.5 else 0 for prob in y_predict_prob]
print("Accuracy:", round(accuracy_score(y_test, y_predict_class), 3))

from sklearn.metrics import confusion_matrix
CM = confusion_matrix(y_test, y_predict_class)
FN = CM[1][0]
print("False Negative Rate",FN)

print("\nDefine threshold 0.65")
y_predict_class = [1 if prob > 0.65 else 0 for prob in y_predict_prob]
print("Accuracy:", round(accuracy_score(y_test, y_predict_class), 3))
CM = confusion_matrix(y_test, y_predict_class)
FN = CM[1][0]
print("False Negative Rate",FN)

#%% Step 9 - feat.d Manipulation

print("feat.d set to 0 results:")
d_set_0 = x_test.assign(d=0)
y_predict_prob0 = reducedmodel.predict(d_set_0)
print("Prediction Probability Average:",round(y_predict_prob0.mean(),4))

print("\nfeat.d set to 1 results:")
d_set_1 = x_test.assign(d=1)
y_predict_prob1 = reducedmodel.predict(d_set_1)
print("Prediction Probability Average:",round(y_predict_prob1.mean(),4))

print("\nDifference Between Probabilities ",round((y_predict_prob1.mean() - y_predict_prob0.mean()),4))