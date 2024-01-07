#%% Import Packages
import pandas as pd
import numpy as np
from os import listdir
from os.path import join
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from math import sqrt
from prettytable import PrettyTable

#%% Data Allocation

global path 
path = "C:/Users/danma/Downloads/MAP 4191/Project Data"
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

df = df.drop(['Volume_mdm','Volume_mem', 'Volume_mulc', 'Volume_mmtr', 'Volume_musc'],axis=1)

del files, processed_dfs

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

X = df.iloc[: , 1:]
y = df.iloc[: , :1].to_numpy().ravel()

scaler = StandardScaler()
scaler.fit(X)

X = scaler.transform(X)

del scaler

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

myTable = PrettyTable(["Model", "Base Score", "Base RMSE", "Tuned Score", "Tuned RMSE"]) 

#%% Decision Tree Regression
dt = DecisionTreeRegressor()
dt.fit(X_train, y_train)

y_pred = dt.predict(X_test)
score = dt.score(X_test, y_test)
mse = mean_squared_error(y_test, y_pred)
rmse = sqrt(mse)
print(f'Decision Tree Regression (Default) Score: {score:.4f}')
print(f'Decision Tree Regression (Default) RMSE: {rmse:.4f}')

param_grid = {
    'max_depth': [None, 3, 4, 5, 6, 8],
    'min_samples_split': [2, 4, 6, 0.1, 0.2, 0.3],
    'min_samples_leaf': [1, 2, 3, 0.1, 0.2, 0.3],
    'min_weight_fraction_leaf': [0.0, 0.1, 0.2, 0.3],
    'max_features': [None, "sqrt", "log2"],
    'max_leaf_nodes': [None, 10, 20, 30, 40, 50]
}

grid = GridSearchCV(dt, param_grid, verbose = 1, n_jobs=-1)

best_dt = grid.fit(X_train, y_train)

print('Best max_depth:', best_dt.best_estimator_.get_params()['max_depth'])
print('Best min_samples_split:', best_dt.best_estimator_.get_params()['min_samples_split'])
print('Best min_samples_leaf:', best_dt.best_estimator_.get_params()['min_samples_leaf'])
print('Best min_weight_fraction_leaf:', best_dt.best_estimator_.get_params()['min_weight_fraction_leaf'])
print('Best max_features:', best_dt.best_estimator_.get_params()['max_features'])
print('Best max_leaf_nodes:', best_dt.best_estimator_.get_params()['max_leaf_nodes'])

#%% Decision Tree Regression Part 2
b_dt = DecisionTreeRegressor(**best_dt.best_estimator_.get_params())
b_dt.fit(X_train, y_train)
b_dt.predict(X_test)
b_score = b_dt.score(X_test, y_test)
y_pred = b_dt.predict(X_test)
b_mse = mean_squared_error(y_test, y_pred)
b_rmse = sqrt(b_mse)
print(f'Decision Tree Regression (Tuned) Score: {b_score:.4f}')
print(f'Decision Tree Regression (Tuned) RMSE: {rmse:.4f}')

#myTable = PrettyTable(["Model", "Base Score", "Base RMSE", "Tuned Score", "Tuned RMSE"])
myTable.add_row(["Decision Tree Regression", round(score, 4), round(rmse, 4), round(b_score, 4), round(b_rmse, 4)])

#%% KNN Regression
knn = KNeighborsRegressor()
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
score = knn.score(X_test, y_test)
mse = mean_squared_error(y_test, y_pred)
rmse = sqrt(mse)
print(f'KNN Regression (Default) Score: {score:.4f}')
print(f'KNN Regression (Default) RMSE: {rmse:.4f}')

param_grid = {
    'n_neighbors': [3, 5, 7, 10, 15],
    'weights': ['uniform', 'distance'],
    'algorithm': ['ball_tree', 'kd_tree', 'brute'],
    'leaf_size': [10, 20, 30, 40, 50]
}

grid = GridSearchCV(knn, param_grid, verbose = 1, n_jobs=-1)

best_knn = grid.fit(X_train, y_train)

print('Best n_neighbors:', best_knn.best_estimator_.get_params()['n_neighbors'])
print('Best weights:', best_knn.best_estimator_.get_params()['weights'])
print('Best algorithm:', best_knn.best_estimator_.get_params()['algorithm'])
print('Best leaf_size:', best_knn.best_estimator_.get_params()['leaf_size'])

#%% KNN Regression Part 2
b_knn = KNeighborsRegressor(**best_knn.best_estimator_.get_params())
b_knn.fit(X_train, y_train)
b_knn.predict(X_test)
b_score = b_knn.score(X_test, y_test)
y_pred = b_knn.predict(X_test)
b_mse = mean_squared_error(y_test, y_pred)
b_rmse = sqrt(b_mse)
print(f'KNN Regression (Tuned) Score: {b_score:.4f}')
print(f'KNN Regression (Tuned) RMSE: {rmse:.4f}')

#myTable = PrettyTable(["Model", "Base Score", "Base RMSE", "Tuned Score", "Tuned RMSE"])
myTable.add_row(["KNN Regression", round(score, 4), round(rmse, 4), round(b_score, 4), round(b_rmse, 4)])

#%% Gradient Boosted Decision Tree
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

#%% Gradient Boosted Decision Tree Pt 2
b_gdr = GradientBoostingRegressor(**best_gb.best_estimator_.get_params())
b_gdr.fit(X_train, y_train)
b_gdr.predict(X_test)
b_score = b_gdr.score(X_test, y_test)
y_pred = b_gdr.predict(X_test)
b_mse = mean_squared_error(y_test, y_pred)
b_rmse = sqrt(b_mse)
print(f'Gradient Boosted Decision Tree (Tuned) Score: {b_score:.4f}')
print(f'Gradient Boosted Decision Tree (Tuned) RMSE: {rmse:.4f}')

#myTable = PrettyTable(["Model", "Base Score", "Base RMSE", "Tuned Score", "Tuned RMSE"])
myTable.add_row(["Gradient Boosted Decision Tree", round(score, 4), round(rmse, 4), round(b_score, 4), round(b_rmse, 4)]) 

#%% Graphing Feature Importance
feature_importance = b_gdr.feature_importances_
feature_importance_series = pd.Series(feature_importance, index=X_train.columns)
feature_importance_series = pd.Series(feature_importance, index=X_train.columns)
sorted_feature_importance = feature_importance_series.sort_values(ascending=False)

plt.figure(figsize=(20,15))
sns.barplot(x=sorted_feature_importance, y=sorted_feature_importance.index)
plt.title('Feature Importance: Gradient Boosted Regressor',fontsize='20',pad='20.0')
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.show()

print(myTable)