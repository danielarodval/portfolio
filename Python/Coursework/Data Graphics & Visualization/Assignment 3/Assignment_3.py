# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 21:32:48 2023

@author: danma
"""

import pandas as pd
file_path = 'C:/Users/danma/Downloads/ISC 4551/Assignment 3/NCD_RisC_Lancet_2020_height_child_adolescent_country.csv'
df = pd.read_csv(file_path)

file_path = 'C:/Users/danma/Downloads/ISC 4551/Assignment 3/country_to_continent.json'
import json
with open(file_path) as json_file :
    country_to_continent = json.load(json_file)
df['Continent'] = df['Country'].map(country_to_continent)

filter_df = df[df['Age group'] > 18]
filter_df = filter_df[filter_df['Year'] == 2019]

filter_df = filter_df.reset_index(drop=True)

filter_df = filter_df.drop(filter_df.columns[[2,3,5,6,7]],axis=1)

import plotly.express as px

fig = px.strip(filter_df, x="Mean height", y="Country")
fig.show()

fig = px.histogram()

#%% Assignment 2
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