import pandas as pd

df = pd.read_csv('C:/Users/danma/Downloads/ISC 4551/Assignment 5/owid-co2-data.csv')
print(df.head())

from countrygroups import EUROPEAN_UNION as EU
EU.names

df_eu = df[df['country'].isin(EU.names).values]
df_eu_2021 = df_eu[(df_eu['year'] == 2021).values]
compact = df_eu_2021[['country','co2','co2_per_capita','iso_code']]

