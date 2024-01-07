#%% Import and Split Data
import pandas as pa;

file_path = 'C:/Users/danma/Desktop/Personal Documents/UCF/STA 4365/final/Weekly.csv'
df = pa.read_csv(file_path)

print("DataFrame Output:\n",df)

x = df.drop(['Direction'], axis=1)
y = df.iloc[: , -1]
#replace categorical last column data with 1 and 0
y = y.replace('Down',0, regex=True)
y = y.replace('Up',1, regex=True)

print("\nX Column Output:\n",x)

print("\nY Column Output:\n",y)
#%% Further Split and Scale Data
from sklearn.model_selection import train_test_split as TTS

x_train, x_test, y_train, y_test = TTS(x,y,test_size=.2, random_state=0)

from sklearn.preprocessing import StandardScaler

scalar = StandardScaler()
scalar.fit(x_train)

x_train = scalar.transform(x_train)
x_test = scalar.transform(x_test)

print("Scaled Training Data:\n",x_train)
#%% Naive Bayes
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
gnb.fit(x_train,y_train)

gnb_pred = gnb.predict(x_test)
gnb_prob = gnb.predict_proba(x_test)

#%% Naives Bayes Results
from sklearn.metrics import accuracy_score
gnb_score = accuracy_score(y_test, gnb_pred)
print("Accuracy: %.03f" %gnb_score)

from sklearn.metrics import RocCurveDisplay
from matplotlib import pyplot

gnb_disp = RocCurveDisplay.from_predictions(y_test, gnb_prob[:,1], name="Naive Bayes ROC")
pyplot.show()

#%% Support Vector Machine with Linear
from sklearn.svm import SVC

# Tuning
from sklearn.model_selection import GridSearchCV

svm_param_grid = {'C': [0.1, 1, 10, 100, 1000],
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001]}

svm_grid = GridSearchCV(SVC(kernel='linear', probability=True), svm_param_grid, refit = True, verbose = 3, n_jobs=-1)
best_svm = svm_grid.fit(x_train, y_train)

svm_C = best_svm.best_estimator_.get_params()['C']
svm_gamma = best_svm.best_estimator_.get_params()['gamma']

print("Support Vector Machine with Linear Hyperparameters:\n")
print("C:", svm_C)
print("gamma:", svm_gamma)

#final fit
svm = SVC(kernel='linear', probability=True, C=svm_C, gamma=svm_gamma)

svm.fit(x_train,y_train)

svm_pred = svm.predict(x_test)
svm_prob = svm.predict_proba(x_test)

#%% Support Vector Machine with Linear Kernel Results
from sklearn.metrics import accuracy_score
svm_score = accuracy_score(y_test, svm_pred)
print("Accuracy: %.03f" %svm_score)

from sklearn.metrics import RocCurveDisplay
from matplotlib import pyplot

svm_disp = RocCurveDisplay.from_predictions(y_test, svm_prob[:,1], name= "Support Vector Machine with Linear Kernel")
pyplot.show()

#%% Random Forest
from sklearn.ensemble import RandomForestClassifier

# Tuning
from sklearn.model_selection import GridSearchCV

rf_param_grid = {'n_estimators': [5,10,50,100,200,400,600,800,1000,1200,1400,1600,1800],
              'max_depth': [10,20,30,40,50,60,70,80,90,100,None],
              'max_features': ['log2', 'auto', 'sqrt'],
              'min_samples_split': [2,5,7],
              'min_samples_leaf': [1,2,4]}
 
rf_grid = GridSearchCV(RandomForestClassifier(), rf_param_grid, refit=True, verbose=3, n_jobs=-1)
best_rf = rf_grid.fit(x_train, y_train)

rf_n_estimators = best_rf.best_estimator_.get_params()['n_estimators']
rf_max_depth = best_rf.best_estimator_.get_params()['max_depth']
rf_max_features = best_rf.best_estimator_.get_params()['max_features']
rf_min_samples_split = best_rf.best_estimator_.get_params()['min_samples_split']
rf_min_samples_leaf = best_rf.best_estimator_.get_params()['min_samples_leaf']

print("Random Forest Hyperparameters:\n")
print("n_estimators:", rf_n_estimators)
print("max_depth:", rf_max_depth)
print("max_features:", rf_max_features)
print("min_samples_split:", rf_min_samples_split)
print("min_samples_leaf:", rf_min_samples_leaf)

#final fit
rf = RandomForestClassifier(n_estimators=rf_n_estimators, max_depth=rf_max_depth, max_features=rf_max_features, min_samples_split=rf_min_samples_split, min_samples_leaf=rf_min_samples_leaf)
rf.fit(x_train,y_train)

rf_pred = rf.predict(x_test)
rf_prob = rf.predict_proba(x_test)

#%% Random Forest Results
from sklearn.metrics import accuracy_score
rf_score = accuracy_score(y_test, rf_pred)
print("Accuracy: %.03f" %rf_score)

from sklearn.metrics import RocCurveDisplay
from matplotlib import pyplot

rf_disp = RocCurveDisplay.from_predictions(y_test, rf_prob[:,1], name= "Random Forest")
pyplot.show()

#%% Gradient Boosted Decision Tree
from sklearn.ensemble import GradientBoostingClassifier

#tuning
from sklearn.model_selection import GridSearchCV

gb_param_grid = {'learning_rate': [0.01, 0.02, 0.03, 0.04],
              'subsample': [0.9, 0.5, 0.2, 0.1],
              'n_estimators': [100,200,300,500,750,1000,1500],
              'max_depth': [4,6,8,10]}

gb_grid = GridSearchCV(GradientBoostingClassifier(), gb_param_grid, refit=True, verbose=3, n_jobs=-1)
best_gb = gb_grid.fit(x_train, y_train)

gb_learning_rate = best_gb.best_estimator_.get_params()['learning_rate']
gb_subsample = best_gb.best_estimator_.get_params()['subsample']
gb_n_estimators = best_gb.best_estimator_.get_params()['n_estimators']
gb_max_depth = best_gb.best_estimator_.get_params()['max_depth']

print("Gradient Boosted Decision Tree Hyperparameters:\n")
print("learning_rate:", gb_learning_rate)
print("subsample:", gb_subsample)
print("n_estimators:", gb_n_estimators)
print("max_depth:", gb_max_depth)

#final fit
gb = GradientBoostingClassifier(learning_rate=gb_learning_rate, subsample=gb_subsample, n_estimators=gb_n_estimators, max_depth=gb_max_depth)
gb.fit(x_train, y_train)

gb_pred = gb.predict(x_test)
gb_prob = gb.predict_proba(x_test)

#%% Gradient Boosted Decision Tree Results
from sklearn.metrics import accuracy_score
gb_score = accuracy_score(y_test, gb_pred)
print("Accuracy: %.03f" %gb_score)

from sklearn.metrics import RocCurveDisplay
from matplotlib import pyplot

gb_disp = RocCurveDisplay.from_predictions(y_test, gb_prob[:,1], name="Gradient Boosted Decision Tree")
pyplot.show()