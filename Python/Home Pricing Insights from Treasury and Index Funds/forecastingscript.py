'''
Daniel Rodriguez, Kzzy Centeno, Mir Khan, Sriharsha Aitharaju
'''

#%% Import Packages
import pandas as pd
import numpy as np
from os import listdir
from os.path import join
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from math import sqrt
from prettytable import PrettyTable
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.inspection import permutation_importance
#%% Data Allocation

global path 
path = "C:/Users/danma/Downloads/STA 4724/Project Data"
files = [f for f in listdir(path) if f.endswith(".csv")]

def filter_last_date(group):
    return group[group.index == group.index.max()]

#convert datetime and set index
def index_format(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

def is_numeric_column(col):
    try:
        pd.to_numeric(col.str.replace(',',''), errors='raise')
        return True
    except:
        return False

def process_file(file_name):
    df = pd.read_csv(join(path,file_name))
    
    #check for morningstar
    if "morningstar" in file_name:
        #create an acronym based on the file_name
        acronym = ''.join(np.transpose(np.array(file_name.split(".")[0].split("_")).astype('<U1')))
        
        #format data
        df = df.iloc[: , 1:]
        
        for col in df.columns:
            if is_numeric_column(df[col]):
                df[col] = df[col].str.replace(',','').astype(float)
        
        #replace the column names
        df.columns = [f"{col}_{acronym}" if col != 'Date' else col for col in df.columns]
        
        df = index_format(df)
        
    elif "summary" in file_name:
        #formatting SOMA time data
        df.rename(columns={'As Of Date': 'Date'}, inplace=True)
        
        df = index_format(df)
        
        #index column adjustments
        df = df.groupby([df.index.year, df.index.month]).apply(filter_last_date)
        df.index = df.index.droplevel(0)
        df.index = df.index.droplevel(0)
    elif "sale" in file_name:
        #formatting Zillow data
        df = df.drop(columns = ['SizeRank', 'StateName'])
        df = df.iloc[0]
        df = df.iloc[1:]
        df.name = "Median Sale Price"
        
        #index column adjustments
        df.index = pd.to_datetime(df.index)
        df = df.groupby([df.index.year, df.index.month]).apply(filter_last_date)
        df.index = df.index.droplevel(0)
        df.index = df.index.droplevel(0)
        
    return df

#processing all csvs
processed_dfs = [process_file(file) for file in files]
final_df = pd.concat(processed_dfs, axis=1)

#adjusting index matching
final_df.index = final_df.index.to_period('M')
final_df = final_df.groupby(final_df.index).first()

#account for NaN values and dropping non matches rows
final_df = final_df.fillna({"FRN" : 0, "Agencies" : 0})
df = final_df.dropna()

#%% Graphing - Data Allocation

fig, ax = plt.subplots(figsize=(10,10))
missing = final_df.isnull()
sns.heatmap(missing, cbar=False, cmap="Greys")
plt.title('Missing Value Heatmap: Original Merge',fontsize='20',pad='20.0')
plt.show()

fig, ax = plt.subplots(figsize=(10,10))
missing = df.isnull()
sns.heatmap(missing, cbar=False, cmap="Greys")
plt.title('Missing Value Heatmap: Data Matched Merge',fontsize='20',pad='20.0')
plt.show()


#%% Data Pre Processing
df = df.drop(['Volume_mdm','Volume_mem', 'Volume_mulc', 'Volume_mmtr', 'Volume_musc'],axis=1)

del files, processed_dfs, final_df

X = df.iloc[: , 1:]
y = df.iloc[: , :1].to_numpy().ravel()

scaler = StandardScaler()
scaler.fit(X)

X = scaler.transform(X)

df = pd.concat([pd.DataFrame(X,columns=df.iloc[: , 1:].columns),pd.DataFrame(y,columns=["Median Sale Price"])],axis=1)

#%% Feature Selection
corr_matrix = df.corr().abs()

top_corr_features = corr_matrix["Median Sale Price"].abs().sort_values(ascending=False).head(19).index
df = df[top_corr_features]



X = df.iloc[: , 1:]
y = df.iloc[: , :1].to_numpy().ravel()

del top_corr_features
#%% Graphing - Feature Selection

# first corr matrix
fig, ax = plt.subplots(figsize=(40,30))
sns.heatmap(corr_matrix, fmt=".1f", ax=ax, annot=True, cmap="Greys")
plt.title('Correlation: Pre Feature Selection',fontsize='20',pad='20.0')
plt.show()

# second corr matrix
fig, ax = plt.subplots(figsize=(20,15))
sns.heatmap(df.corr().abs(), fmt=".1f", ax=ax, annot=True, cmap="Greys")
plt.title('Correlation: Post Feature Selection',fontsize='20',pad='20.0')
plt.show()


del corr_matrix
#%% Train Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=0)

modelResults = PrettyTable(["Model", "Base Score", "Base RMSE", "Tuned Score", "Tuned RMSE"]) 
topFeatures = PrettyTable(["Model", "Feature", "Importance"])

#%% Daniel - Gradient Boosted Decision Tree
# Default
gdr = GradientBoostingRegressor(random_state=0)
gdr.fit(X_train, y_train)

y_pred = gdr.predict(X_test)
score = gdr.score(X_test, y_test)
mse = mean_squared_error(y_test, y_pred)
rmse = sqrt(mse)
print(f'Gradient Boosted Decision Tree (Default) Score: {score:.4f}')
print(f'Gradient Boosted Decision Tree (Default) RMSE: {rmse:.4f}')

# HyperParameter Tuning
'''param_grid = {'learning_rate': [0.01, 0.02, 0.03, 0.04],
              'subsample': [1.0, 0.9, 0,7, 0.5, 0.1],
              'n_estimators': [100, 200, 300, 500, 700, 800],
              'max_depth': [3, 4, 5, 6, 8],
              'min_samples_split': [2, 4, 6],
              'min_samples_leaf': [1, 2, 3],
              'max_features': ['auto', 'sqrt', 'log2', None]}'''

param_grid = {'learning_rate': [0.04],
              'subsample': [0.5],
              'n_estimators': [700, 800],
              'max_depth': [6],
              'min_samples_split': [2],
              'min_samples_leaf': [1, 2, 3],
              'max_features': ['sqrt', 'log2', None]}
grid = GridSearchCV(gdr, param_grid, verbose = 1, n_jobs=-1)

best_gb = grid.fit(X_train, y_train)

print('Best learning_rate:', best_gb.best_estimator_.get_params()['learning_rate'])
print('Best subsample:', best_gb.best_estimator_.get_params()['subsample'])
print('Best n_estimators:', best_gb.best_estimator_.get_params()['n_estimators'])
print('Best max_depth:', best_gb.best_estimator_.get_params()['max_depth'])
print('Best min_samples_split:', best_gb.best_estimator_.get_params()['min_samples_split'])
print('Best min_samples_leaf:', best_gb.best_estimator_.get_params()['min_samples_leaf'])
print('Best max_features:', best_gb.best_estimator_.get_params()['max_features'])

#%% Daniel - Gradient Boosted Decision Tree Pt 2
b_gdr = GradientBoostingRegressor(**best_gb.best_estimator_.get_params())
b_gdr.fit(X_train, y_train)
b_score = b_gdr.score(X_test, y_test)
y_pred = b_gdr.predict(X_test)
b_mse = mean_squared_error(y_test, y_pred)
b_rmse = sqrt(b_mse)
print(f'Gradient Boosted Decision Tree (Tuned) Score: {b_score:.4f}')
print(f'Gradient Boosted Decision Tree (Tuned) RMSE: {rmse:.4f}')

#myTable = PrettyTable(["Model", "Base Score", "Base RMSE", "Tuned Score", "Tuned RMSE"])
modelResults.add_row(["Gradient Boosted Regressor", round(score, 4), round(rmse, 4), round(b_score, 4), round(b_rmse, 4)]) 


#%% Daniel- Graphing Feature Importance
feature_importance = b_gdr.feature_importances_
feature_importance_series = pd.Series(feature_importance, index=X_train.columns)
feature_importance_series = pd.Series(feature_importance, index=X_train.columns)
sorted_feature_importance = feature_importance_series.sort_values(ascending=False)

# Add top 5 features to the table
for feature, importance in sorted_feature_importance[:5].items():
    topFeatures.add_row(["Gradient Boosted Regressor", feature, importance])

plt.figure(figsize=(20,15))
sns.barplot(x=sorted_feature_importance, y=sorted_feature_importance.index,palette="Greys")
plt.title('Feature Importance: Gradient Boosted Regressor',fontsize='20',pad='20.0')
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.show()


#%% Kzzy - Random Forest
rf_default = RandomForestRegressor(random_state=0)
rf_default.fit(X_train, y_train)

y_pred = rf_default.predict(X_test)
score = rf_default.score(X_test, y_test)
mse = mean_squared_error(y_test, y_pred)
rmse = sqrt(mse)

print(f'Random Forest Regressor (Default) Score: {score:.4f}')
print(f'Random Forest Regressor (Default) RMSE: {rmse:.4f}')

#print("Default Random Forest Model Performance:")
#print("MSE: %.2f" % mean_squared_error(y_test, rf_default_predictions))
#print("R\u00b2: %.2f \n" % r2_score(y_test, rf_default_predictions))

# This is optimal parameter grid after tuning
print('Random Forest Hyperparameters:')
n_estimators = [50, 100]
max_depth = [90, 100]
max_features = ['log2']
min_samples_leaf = [1, 2]
min_samples_split = [2, 5]
rf_hyperparameters = dict(n_estimators=n_estimators, max_depth=max_depth, max_features=max_features, min_samples_leaf=min_samples_leaf, min_samples_split=min_samples_split)

rf_2 = RandomForestRegressor()
rf_gs = GridSearchCV(rf_2, rf_hyperparameters, cv=10, n_jobs=-1, verbose=1)

best_rf = rf_gs.fit(X, y)

print('Best n_estimators:', best_rf.best_estimator_.get_params()['n_estimators'])
print('Best max_depth:', best_rf.best_estimator_.get_params()['max_depth'])
print('Best max_features:', best_rf.best_estimator_.get_params()['max_features'])
print('Best min_samples_leaf:', best_rf.best_estimator_.get_params()['min_samples_leaf'])
print('Best min_samples_split:', best_rf.best_estimator_.get_params()['min_samples_split'])

best_rf_model = best_rf.best_estimator_
best_rf_model.fit(X_train, y_train)

b_score = best_rf_model.score(X_test, y_test)
y_pred = best_rf_model.predict(X_test)
b_mse = mean_squared_error(y_test, y_pred)
b_rmse = sqrt(b_mse)

print(f'Random Forest Regressor (Tuned) Score: {b_score:.4f}')
print(f'Random Forest Regressor (Tuned) RMSE: {rmse:.4f}')

y_pred = best_rf_model.predict(X_test)

modelResults.add_row(["Random Forest Regressor", round(score, 4), round(rmse, 4), round(b_score, 4), round(b_rmse, 4)]) 

# Feature importance
feature_importance = best_rf_model.feature_importances_
sorted_idx = np.argsort(feature_importance)

# Assuming b_gdr is the best random forest model from the previous context
feature_importance = best_rf_model.feature_importances_
feature_importance_series = pd.Series(feature_importance, index=X_train.columns)
sorted_feature_importance = feature_importance_series.sort_values(ascending=False)

# Add top 5 features to the table
for feature, importance in sorted_feature_importance[:5].items():
    topFeatures.add_row(["Random Forest Regressor", feature, importance])

plt.figure(figsize=(20,15))
sns.barplot(x=sorted_feature_importance, y=sorted_feature_importance.index, palette="Greys")
plt.title('Feature Importance: Random Forest Regressor',fontsize='20',pad='20.0')
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.show()

#%% Harsha Support Vector Machine 
# kernel is rbf to signify non-linear kernel
# Testing with higher C (allowing for more misclassifications in model), gamma(influencing
# shape of decision boundary), epsilon (fitting the training data more precisely)
# Standardizing the target variable
scaler_y = StandardScaler()
y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()

# Fitting SVR model with default parameters
svr = SVR(kernel='rbf')
svr.fit(X_train, y_train_scaled)

# Making predictions on the test set
y_pred_default = svr.predict(X_test)

# Inverse transforming to get predictions in the original scale
y_pred_default_trans = scaler_y.inverse_transform(y_pred_default.reshape(-1, 1)).ravel()

y_pred = svr.predict(X_test)
score = r2_score(y_test, y_pred_default_trans)
mse = mean_squared_error(y_test, y_pred_default_trans)
rmse = sqrt(mse)

print(f'Support Vector Regressor (Default) Score: {score:.4f}')
print(f'Support Vector Regressor (Default) RMSE: {rmse:.4f}')

# Tuning the hyperparameters
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.01, 0.1, 1, 10],
    'epsilon': [0.01, 0.1, 0.2]
}

svr_gs = GridSearchCV(SVR(kernel='rbf'), param_grid, refit=True, verbose=1, n_jobs=-1)

# Fitting the GridSearchCV to find the best model
svr_gs.fit(X_train, y_train_scaled)

# Getting the best parameters
best_params = svr_gs.best_params_

print('Best C:', best_params['C'])
print('Best gamma:', best_params['gamma'])
print('Best epsilon:', best_params['epsilon'])

# Creating and fitting a new SVR model with the best parameters
best_svr = SVR(kernel='rbf', C=best_params['C'], gamma=best_params['gamma'], epsilon=best_params['epsilon'])
best_svr.fit(X_train, y_train_scaled)

# Making predictions using the best model
y_pred_best = best_svr.predict(X_test)

# Inverse transforming to get predictions in the original scale
y_pred_best_trans = scaler_y.inverse_transform(y_pred_best.reshape(-1, 1)).ravel()

# Evaluating the best SVR model
b_score = r2_score(y_test, y_pred_best_trans)
y_pred = best_svr.predict(X_test)
b_mse = mean_squared_error(y_test, y_pred_best_trans)
b_rmse = sqrt(b_mse)

print(f'Support Vector Regressor (Tuned) Score: {b_score:.4f}')
print(f'Support Vector Regressor (Tuned) RMSE: {rmse:.4f}')

modelResults.add_row(["Support Vector Regressor", round(score, 4), round(rmse, 4), round(b_score, 4), round(b_rmse, 4)]) 

perm_importance = permutation_importance(best_svr, X_test, y_test, n_repeats=10, random_state=42)
sorted_idx = perm_importance.importances_mean.argsort()

sorted_importances = pd.Series(perm_importance.importances_mean[sorted_idx], index=X.columns[sorted_idx])


plt.figure(figsize=(20,15))
sns.barplot(x=sorted_importances, y=sorted_importances.index, palette="Greys")
plt.title('Permutation Importance: Support Vector Regressor', fontsize=20, pad=20.0)
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.show()


# Add top 5 features to the table
for idx in sorted_idx[-5:]:  # Get indices of top 5 features
    feature_name = X.columns[idx]
    importance = perm_importance.importances_mean[idx]
    topFeatures.add_row(["Support Vector Regressor", feature_name, importance])


#%% Mir - KNN
KNNReg = KNeighborsRegressor()
KNNReg.fit(X_train, y_train)

y_pred = KNNReg.predict(X_test)
score = KNNReg.score(X_test, y_test)
mse = mean_squared_error(y_test, y_pred)
rmse = sqrt(mse)

print(f'KNN Regressor (Default) Score: {score:.4f}')
print(f'KNN Regressor (Default) RMSE: {rmse:.4f}')

param_grid = {
    'n_neighbors': np.arange(1, 100),  # Adjust the range based on your preference
    'weights': ['uniform', 'distance'],
    'p': [1, 2]  # 1 for Manhattan distance, 2 for Euclidean distance
}

grid_search = GridSearchCV(KNNReg, param_grid, scoring='r2', cv=5)
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
print("Best Hyperparameters:", best_params)

results = grid_search.cv_results_
n_neighbors = param_grid['n_neighbors']

knn_mse = mean_squared_error(y_test, y_pred)

b_score = grid_search.score(X_test, y_test)
y_pred = grid_search.predict(X_test)
b_mse = mean_squared_error(y_test, y_pred)
b_rmse = sqrt(b_mse)

print(f'KNN Regressor (Tuned) Score: {b_score:.4f}')
print(f'KNN Regressor (Tuned) RMSE: {rmse:.4f}')

modelResults.add_row(["KNN Regressor", round(score, 4), round(rmse, 4), round(b_score, 4), round(b_rmse, 4)]) 

perm_importance = permutation_importance(grid_search, X_test, y_test, n_repeats=10, random_state=42)
sorted_idx = perm_importance.importances_mean.argsort()

sorted_importances = pd.Series(perm_importance.importances_mean[sorted_idx], index=X.columns[sorted_idx])


plt.figure(figsize=(20,15))
sns.barplot(x=sorted_importances, y=sorted_importances.index, palette="Greys")
plt.title('Permutation Importance: KNN Regressor', fontsize=20, pad=20.0)
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.show()


# Add top 5 features to the table
for idx in sorted_idx[-5:]:  # Get indices of top 5 features
    feature_name = X.columns[idx]
    importance = perm_importance.importances_mean[idx]
    topFeatures.add_row(["KNN Regressor", feature_name, importance])
    
#%%
# Assuming 'results' is obtained from grid_search.cv_results_
n_neighbors = results['param_n_neighbors'].data.astype(int)  # Convert to integer for plotting

# Set the Seaborn style
sns.set(style="darkgrid")

# Create the plot
plt.figure(figsize=(20,15))

# Create a line plot with Seaborn
sns.lineplot(x=n_neighbors, y=results['mean_test_score'], label='Mean Test Score', color='grey')

# Add fill_between with Matplotlib
std_dev = results['std_test_score']
plt.fill_between(n_neighbors, results['mean_test_score'] - std_dev,
                 results['mean_test_score'] + std_dev, color='grey', alpha=0.2, label='± 1 STD')

# Add labels and title
plt.xlabel('Number of Neighbors')
plt.ylabel('R2 Score')  # Adjust based on your scoring metric
plt.title('KNN Regressor Performance with Different Neighbors')
plt.legend()

# Show the plot
plt.show()