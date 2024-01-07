# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 20:58:09 2022

@author: danma
"""

import pandas as pa;
file_path = 'C:/Users/danma/Downloads/STA 4364/Assignment 2/Auto.csv'
df = pa.read_csv(file_path)
df = df[df['horsepower'] != '?']
df['horsepower'] = df['horsepower'].astype(int)
df.head()

import seaborn as sns
sns.set_theme(style="ticks")

sns.pairplot(df)

df_quant = df.drop(['name'],axis=1)
df_quant.corr()

#regresssuib linear model
import statsmodels.api as sm
x = df_quant.drop(['horsepower'],axis=1)
y = df_quant['horsepower']
result = sm.OLS(y,x).fit()
print(result.summary())


import matplotlib.pyplot as plt
plot_lm_1 = plt.figure()
plot_lm_1.axes[0] = sns.residplot(result.fittedvalues, y, data=df,
                          lowess=True,
                          scatter_kws={'alpha': 0.5},
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plot_lm_1.axes[0].set_title('Residuals vs Fitted')
plot_lm_1.axes[0].set_xlabel('Fitted values')
plot_lm_1.axes[0].set_ylabel('Residuals')
#%%
from statsmodels.graphics.gofplots import ProbPlot
import numpy as np

QQ = ProbPlot(result.get_influence().resid_studentized_internal)
plot_lm_2 = QQ.qqplot(line='45', alpha=0.5, color='#4C72B0', lw=1)
plot_lm_2.axes[0].set_title('Normal Q-Q')
plot_lm_2.axes[0].set_xlabel('Theoretical Quantiles')
plot_lm_2.axes[0].set_ylabel('Standardized Residuals');
# annotations
abs_norm_resid = np.flip(np.argsort(np.abs(result.get_influence().resid_studentized_internal)), 0)
abs_norm_resid_top_3 = abs_norm_resid[:3]
for r, i in enumerate(abs_norm_resid_top_3):
    plot_lm_2.axes[0].annotate(i,
                               xy=(np.flip(QQ.theoretical_quantiles, 0)[r],
                                   result.get_influence().resid_studentized_internal[i]));
    
#%%

plot_lm_3 = plt.figure()
plt.scatter(result.fittedvalues, np.sqrt(np.abs(result.get_influence().resid_studentized_internal)), alpha=0.5);
sns.regplot(result.fittedvalues, np.sqrt(np.abs(result.get_influence().resid_studentized_internal)),
              scatter=False,
              ci=False,
              lowess=True,
              line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8});
plot_lm_3.axes[0].set_title('Scale-Location')
plot_lm_3.axes[0].set_xlabel('Fitted values')
plot_lm_3.axes[0].set_ylabel('$\sqrt{|Standardized Residuals|}$');

# annotations
abs_sq_norm_resid = np.flip(np.argsort(np.sqrt(np.abs(result.get_influence().resid_studentized_internal))), 0)
abs_sq_norm_resid_top_3 = abs_sq_norm_resid[:3]
for i in abs_norm_resid_top_3:
      plot_lm_3.axes[0].annotate(i,
                                 xy=(result.fittedvalues[i],
                                     np.sqrt(np.abs(result.get_influence().resid_studentized_internal))[i]));
      
#%%
plot_lm_4 = plt.figure();
plt.scatter(result.get_influence().hat_matrix_diag, np.sqrt(np.abs(result.get_influence().resid_studentized_internal)), alpha=0.5);
sns.regplot(result.get_influence().hat_matrix_diag, np.sqrt(np.abs(result.get_influence().resid_studentized_internal)),
              scatter=False,
              ci=False,
              lowess=True,
              line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8});
plot_lm_4.axes[0].set_xlim(0, max(result.get_influence().hat_matrix_diag)+0.01)
plot_lm_4.axes[0].set_ylim(-3, 5)
plot_lm_4.axes[0].set_title('Residuals vs Leverage')
plot_lm_4.axes[0].set_xlabel('Leverage')
plot_lm_4.axes[0].set_ylabel('Standardized Residuals');

# annotations
leverage_top_3 = np.flip(np.argsort(result.get_influence().cooks_distance[0]), 0)[:3]
for i in leverage_top_3:
      plot_lm_4.axes[0].annotate(i,
                                 xy=(result.get_influence().hat_matrix_diag[i],
                                     np.sqrt(np.abs(result.get_influence().resid_studentized_internal))[i]));
      
      #%%
#regresssuib linear model
import statsmodels.formula.api as smf
result = smf.ols('mpg ~ horsepower*displacement', data=df_quant).fit()
print(result.summary())
#regresssuib linear model
import statsmodels.formula.api as smf
result = smf.ols('mpg ~ displacement:weight', data=df_quant).fit()
print(result.summary())
#regresssuib linear model
import statsmodels.formula.api as smf
result = smf.ols('mpg ~ displacement:cylinders+displacement:weight+acceleration:horsepower', data=df_quant).fit()
print(result.summary())
#regresssuib linear model
import statsmodels.formula.api as smf
result = smf.ols('mpg ~ displacement:cylinders+displacement:weight+year:origin+acceleration:horsepower', data=df_quant).fit()
print(result.summary())
#regresssuib linear model
import statsmodels.formula.api as smf
result = smf.ols('mpg ~ year:origin+displacement:weight+displacement:weight+acceleration:horsepower+acceleration:weight', data=df_quant).fit()
print(result.summary())