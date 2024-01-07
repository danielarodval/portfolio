# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 00:43:15 2022

@author: danma
"""

#%% Getting Cleaned Data from R
import pandas as pd;
file_path = 'C:/Users/danma/OneDrive/Documents/R/STA 4164/Data/Pizza Restaurant Sales/Clean Data.csv'
df = pd.read_csv(file_path)
df.head()
#%% OneHotEncoder so that we can plot similiarly from the R code
from sklearn.preprocessing import OneHotEncoder

enc = OneHotEncoder()

#encode order_time
encoded_ot = enc.fit_transform(df[["order_time"]])
encoded_ot = pd.DataFrame(encoded_ot.toarray(),columns=["morning","afternoon","evening","night"])
df = df.join(encoded_ot,how='left')

#encode pizza_size
encoded_ps = enc.fit_transform(df[["pizza_size"]])
encoded_ps = pd.DataFrame(encoded_ps.toarray(),columns=["S","M","L","XL","XXL"])
df = df.join(encoded_ps,how='left')

#drop original categorical columns
df = df.loc[:, df.columns != "order_time"]
df = df.loc[:, df.columns != "pizza_size"]
#drops na values
df = df.dropna()
print("\nFinal Data Frame (after encoding categorical columns):\n",df.head())
del encoded_ot, encoded_ps, enc

#%%
import seaborn as sns
sns.set_theme(style="ticks")

sns.pairplot(df)
sns.pairplot(df, hue='pizza_ingredients', palette='Paired', kind='scatter')

#%%
#regresssuib linear model
import statsmodels.api as sm
x = df.drop(['total_price'],axis=1)
y = df['total_price']
result = sm.OLS(y,x).fit()
print(result.summary())

import matplotlib.pyplot as plt
sns.set_style("darkgrid")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
plot_lm_1 = plt.figure(dpi=1200)
plot_lm_1.axes[0] = sns.residplot(result.fittedvalues, y, data=df,
                          lowess=True,
                          scatter_kws={'alpha': 0.5},
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plot_lm_1.axes[0].set_title('Residuals vs Fitted')
plot_lm_1.axes[0].set_xlabel('Fitted values')
plot_lm_1.axes[0].set_ylabel('Residuals')

#%%
file_path = 'C:/Users/danma/OneDrive/Documents/R/STA 4164/Data/Pizza Restaurant Sales/Best Cat.csv'
df2 = pd.read_csv(file_path)

#regresssuib linear model
import statsmodels.api as sm
x = df2.drop(['total_price'],axis=1)
y = df2['total_price']
result = sm.OLS(y,x).fit()
print(result.summary())

import matplotlib.pyplot as plt
sns.set_style("darkgrid")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
plot_lm_1 = plt.figure(dpi=1200)
plot_lm_1.axes[0] = sns.residplot(result.fittedvalues, y, data=df,
                          lowess=True,
                          scatter_kws={'alpha': 0.5},
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plot_lm_1.axes[0].set_title('Residuals vs Fitted')
plot_lm_1.axes[0].set_xlabel('Fitted values')
plot_lm_1.axes[0].set_ylabel('Residuals')