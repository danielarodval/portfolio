import yfinance as yf

billClinton = yf.download("^GSPC", start = "1993-01-20", end = "2001-01-19")
georgeBush = yf.download("^GSPC", start = "2001-01-20", end = "2009-01-19")
barrackObama = yf.download("^GSPC", start = "2009-01-20", end = "2017-01-19")
donaldTrump = yf.download("^GSPC", start = "2017-01-20", end = "2021-01-19")
joeBiden = yf.download("^GSPC", start = "2021-01-20", end = "2023-01-27")

import numpy as np
billClinton['Days'] = (billClinton.index - billClinton.index.min()) / np.timedelta64(1,'D')
georgeBush['Days'] = (georgeBush.index - georgeBush.index.min()) / np.timedelta64(1,'D')
barrackObama['Days'] = (barrackObama.index - barrackObama.index.min()) / np.timedelta64(1,'D')
donaldTrump['Days'] = (donaldTrump.index - donaldTrump.index.min()) / np.timedelta64(1,'D')
joeBiden['Days'] = (joeBiden.index - joeBiden.index.min()) / np.timedelta64(1,'D')

billClinton['Days'] = billClinton['Days'].astype(int)
georgeBush['Days'] = georgeBush['Days'].astype(int)
barrackObama['Days'] = barrackObama['Days'].astype(int)
donaldTrump['Days'] = donaldTrump['Days'].astype(int)
joeBiden['Days'] = joeBiden['Days'].astype(int)

billClinton['name'] = 'Bill CLinton'
georgeBush['name'] = 'George Bush'
barrackObama['name'] = 'Barrack Obama'
donaldTrump['name'] = 'Donald Trump'
joeBiden['name'] = 'Joe Biden'

changeInValue = billClinton["Close"] - billClinton["Close"][0]
relativeChange = changeInValue/billClinton["Close"][0]
percentChange = relativeChange*100
billClinton["percentChange"] = percentChange

changeInValue = georgeBush["Close"] - georgeBush["Close"][0]
relativeChange = changeInValue/georgeBush["Close"][0]
percentChange = relativeChange*100
georgeBush["percentChange"] = percentChange

changeInValue = barrackObama["Close"] - barrackObama["Close"][0]
relativeChange = changeInValue/barrackObama["Close"][0]
percentChange = relativeChange*100
barrackObama["percentChange"] = percentChange

changeInValue = donaldTrump["Close"] - donaldTrump["Close"][0]
relativeChange = changeInValue/donaldTrump["Close"][0]
percentChange = relativeChange*100
donaldTrump["percentChange"] = percentChange

changeInValue = joeBiden["Close"] - joeBiden["Close"][0]
relativeChange = changeInValue/joeBiden["Close"][0]
percentChange = relativeChange*100
joeBiden["percentChange"] = percentChange

import pandas as pd
df = billClinton[['name','Days','percentChange']]
df = pd.concat([df,georgeBush[['name','Days','percentChange']]],join='inner')
df = pd.concat([df,barrackObama[['name','Days','percentChange']]],join='inner')
df = pd.concat([df,donaldTrump[['name','Days','percentChange']]],join='inner')
df = pd.concat([df,joeBiden[['name','Days','percentChange']]],join='inner')
#%%
import plotly.express as px
import plotly.graph_objects as go

px.line(df,x='days',y='percent change')