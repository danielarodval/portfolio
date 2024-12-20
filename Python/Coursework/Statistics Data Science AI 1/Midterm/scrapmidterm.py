# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 17:44:12 2022

@author: danma
"""

#%% Step 1 - Import and Clean Data
import pandas as pd;
#import data
file_path = 'C:/Users/danma/Downloads/midterm_data_1.csv'
colnames=['response', 'a', 'b', 'c', 'd', 'e', 'f', 'g','h', 'i'] 
df = pd.read_table(file_path, sep=",",names=colnames)
df = df.iloc[1: , :]
df = df.astype(float)
df = df.reset_index(drop=True)
#remove row column as predictor
df = df.loc[:, df.columns != 'row']
#drops na values
df = df.dropna()
print("Original Data Frame (after cleaning):\n",df.head())
del file_path, colnames
#%% Step 2 - Format feat.c and feat.g as Categorical
from sklearn.preprocessing import OneHotEncoder;
oe = OneHotEncoder()
#encode C
encoded_C = oe.fit_transform(df[["c"]])
encoded_C = pd.DataFrame(encoded_C.toarray(),columns=["c_1","c_2","c_3","c_4"])
df = df.join(encoded_C,how='left')
#encode G
encoded_G = oe.fit_transform(df[["g"]])
encoded_G = pd.DataFrame(encoded_G.toarray(),columns=["g_1","g_2","g_3"])
df = df.join(encoded_G,how='left')
#drop original categorical columns
df = df.loc[:, df.columns != "c"]
df = df.loc[:, df.columns != "g"]
#drops na values
df = df.dropna()
print("\nFinal Data Frame (after encoding categorical columns):\n",df.head())
del encoded_C, encoded_G, oe
#%% Step 3 - Pairwise Plots and Numerical Correlations
import seaborn as sns
sns.set_theme(style="ticks")
sns.pairplot(df)

print("\nCorrelation Matrix (Numerical):\n",df.iloc[: , :8].corr())
#%% Step 4 - Split Data into Training and Testing
from sklearn.model_selection import train_test_split as TTS;

x = df.loc[:, df.columns != 'response']
y = df['response']
#turns y into a 1-d array instead of a dataframe column
y = y.to_numpy()
y = y.ravel()
train, test = TTS(df, test_size=0.25)
x_train = train.loc[:, df.columns != 'response']
y_train = train['response']
x_test = test.loc[:, df.columns != 'response']
y_test = test['response']
del x, y
#%% Step 5 - Create Linear Model and Show Summary Screen
import numpy as np;
import statsmodels.api as sm;

model = sm.OLS(y_train,x_train).fit()
print(model.summary())
print("\nResidual Standard Error:")
print(np.sqrt(model.mse_resid))

import matplotlib.pyplot as plt;
plt.style.use('seaborn') # pretty matplotlib plots
plt.rc('font', size=14)
plt.rc('figure', titlesize=18)
plt.rc('axes', labelsize=15)
plt.rc('axes', titlesize=18)
#%% Step 6 - Plot Residuals vs Fitted
#Residuals vs Fitted Plot
plt.figure()
sns.residplot(x=model.fittedvalues, y=y_train,
                          lowess=True,
                          scatter_kws={'alpha': 0.5},
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plt.title('Residuals vs Fitted')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.show()
#%% Step 7 - Make Linear Model with Interaction
import statsmodels.formula.api as smf
#preliminary terms for model
inter = 'response ~ a + b + c_1 + c_2 + c_3 + c_4 + d + e + f + g_1 + g_2 + g_3 + h + i'
#interaction terms with a
a_inter = '+ a:b + a:c_1 + a:c_2 + a:c_3 + a:c_4 + a:d + a:e + a:f + a:g_1 + a:g_2 + a:g_3 + a:h + a:i'
#interaction terms with b
b_inter = '+ b:c_1 + b:c_2 + b:c_3 + b:c_4 + b:d + b:e + b:f + b:g_1 + b:g_2 + b:g_3 + b:h + b:i'
#interaction terms with c
c_1_inter = '+ c_1:c_2 + c_1:c_3 + c_1:c_4 + c_1:d + c_1:e + c_1:f + c_1:g_1 + c_1:g_2 + c_1:g_3 + c_1:h + c_1:i'
c_2_inter = '+ c_2:c_3 + c_2:c_4 + c_2:d + c_2:e + c_2:f + c_2:g_1 + c_2:g_2 + c_2:g_3 + c_2:h + c_2:i'
c_3_inter = '+ c_3:c_4 + c_3:d + c_3:e + c_3:f + c_3:g_1 + c_3:g_2 + c_3:g_3 + c_3:h + c_3:i'
c_4_inter = '+ c_4:d + c_4:e + c_4:f + c_4:g_1 + c_4:g_2 + c_4:g_3 + c_4:h + c_4:i'
#interaction terms with d
d_inter = '+ d:e + d:f + d:g_1 + d:g_2 + d:g_3 + d:h + d:i'
#interaction terms with e
e_inter = '+ e:f + e:g_1 + e:g_2 + e:g_3 + e:h + e:i'
#interaction terms with f
f_inter = '+ f:g_1 + f:g_2 + f:g_3 + f:h + f:i'
#interaction terms with g
g_1_inter = '+ g_1:g_2 + g_1:g_3 + g_1:h + g_1:i'
g_2_inter = '+ g_2:g_3 + g_2:h + g_2:i'
g_3_inter = '+ g_3:h + g_3:i'
#interaction terms with h
h_inter = '+ h:i'
#create quadratic terms for numerical (non-categorical)
quadterms = '+ np.square(a) + np.square(b) + np.square(d) + np.square(e) + np.square(f) + np.square(h) + np.square(i)'
fullterms  = inter+a_inter+b_inter+c_1_inter+c_2_inter+c_3_inter+c_4_inter+d_inter+e_inter+f_inter+g_1_inter+g_2_inter+g_3_inter+h_inter+quadterms
model2 =  smf.ols(fullterms, data=train).fit()
print(model2.summary())
print("\nResidual Standard Error:")
print(np.sqrt(model2.mse_resid))

#%% Step 8 - create reduced model
print("\n\nReduced Model:\n")
selectedterms = 'response ~ b + c_1 + c_2 + c_3 + c_4 + d + e + f + g_1 + g_2 + g_3 + h + i + c_1:c_2 + c_1:c_3 + c_1:c_4 + c_1:e + c_1:f + c_1:g_1 + c_1:g_2 + c_1:g_3 + c_1:i+ g_1:h + g_1:i + g_2:h + g_2:i'
reducedterms = selectedterms+b_inter+c_2_inter+c_3_inter+c_4_inter+d_inter+e_inter+f_inter+g_3_inter+h_inter+quadterms
reducedmodel = smf.ols(reducedterms, data=train).fit()
print(reducedmodel.summary())
print("\nResidual Standard Error:")
print(np.sqrt(reducedmodel.mse_resid))

# Step 9 - create residual plot from reduced model
#Residuals vs Fitted Plot
plt.figure()
sns.residplot(x=reducedmodel.fittedvalues, y=y_train,
                          lowess=True,
                          scatter_kws={'alpha': 0.5},
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plt.title('Residuals vs Fitted')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.show()

del fullterms, inter, a_inter, b_inter, c_1_inter, c_2_inter, c_3_inter, c_4_inter, d_inter, e_inter, f_inter, g_1_inter, g_2_inter, g_3_inter, h_inter, quadterms, selectedterms
#%% Step 9 - MSE Comparison
print("MSE for full quadratic model: %.3f" %model2.mse_model)
print("MSE for reduced model: %.3f" %reducedmodel.mse_model)
#%% Step 10 - Predict Confidence Interval
dt = reducedmodel.get_prediction(x_test).summary_frame(alpha = 0.05)
ym_ci_lower = dt['mean_ci_lower'] 
ym_ci_upper = dt['mean_ci_upper']
comparison = pd.concat([ym_ci_lower,y_test.reset_index(),ym_ci_upper], axis=1)
in_conf_int = len(comparison.query('mean_ci_lower<=response & mean_ci_upper>=response'))
perc_conf = in_conf_int / len(y_test) * 100
print("A total of %.2f" %perc_conf, "% of true observations fall within the confidence interval.")
del dt, in_conf_int, model, model2, reducedmodel, reducedterms, comparison