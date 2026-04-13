# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 17:27:12 2023

@author: danma
"""

import pandas as pd
file_path = 'C:/Users/danma/Downloads/ISC 4551/Assignment 2/2000_acs_sample.dta'
df = pd.read_stata(file_path)
print(df.columns)

dropunique = []
for (colName, colData) in df.iteritems():
    if len(colData.unique()) == 1:
        print(colName)
        dropunique.append(colName)
        
df = df.drop(dropunique, axis=1)

df = df.drop(['us2000c_pnum','us2000c_serialno'], axis=1)

df = df.rename(columns={'serial':'household',
'pernum':'person',
'us2000c_sex':'sex',
'us2000c_age':'age',
'us2000c_hispan':'hispanic',
'us2000c_race1':'race',
'us2000c_marstat':'marital_status',
'us2000c_educ':'edu',
'us2000c_inctot':'income'})

df['income'] = pd.to_numeric(df['income'],errors='coerce')

df['sex'].replace('1','Male',inplace=True)
df['sex'].replace('2','Female',inplace=True)

df['marital_status'].replace('1','Now married',inplace=True)
df['marital_status'].replace('2','Widowed',inplace=True)
df['marital_status'].replace('3','Divorced',inplace=True)
df['marital_status'].replace('4','Separated',inplace=True)
df['marital_status'].replace('5','Never married (includes under 15 years)',inplace=True)

df = df.fillna({'income' : df['income'].mode()[0]})