import pandas as pd
url = r'https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/annual-messages-congress-the-state-the-union-0'
df = pd.read_html(url) # Returns list of all tables on page
df = df[0]

df.columns = df.iloc[0]
df = df.drop(df[df['President']=='President'].index)

df = df.drop(df[df['President'].str.contains('NOT')== True].index)
df = df.fillna(method='ffill')

spoken = df[df['Format'] == 'spoken']

import plotly.express as px

fig = px.bar(spoken.groupby('President').President.count(), x="President", y=spoken.groupby('President').President.count().index,orientation='h')
fig.update_traces(textposition = 'outside')
fig.update_layout(yaxis={'categoryorder':"total descending"})
fig.show()
del fig
    
#%% Part 2

url = 'https://github.com/awhstin/Dataset-List/blob/master/presidents.csv'
affil = pd.read_html(url) # Returns list of all tables on page
affil = affil[0]
affil.pop('Unnamed: 0')
#affil = affil.to_dict(orient='records')
del url

def time_convert(x):
    if 'apx' in x:
        print(type(x))
        return [int(s) for s in x.split() if s.isdigit()][0]
    h,m,s = map(int,x.split(':'))
    return (h*60+m)

spoken['Minutes'] = spoken['Minutes'].apply(time_convert)
spoken['Date'] = pd.to_datetime(spoken['Date'])
#%%

spoken['New'] = spoken['President'].str.split().str[-1] +' (' + pd.DatetimeIndex(spoken['Date']).year.astype(str) + ')'
#renamed president columns to match with dictionary
spoken.loc[spoken['President'].str.contains('Gerald R. Ford'),'President'] = 'Gerald Ford'
spoken.loc[spoken['President'].str.contains('Jimmy Carter'),'President'] = 'James (Jimmy) Carter'
spoken.loc[spoken['President'].str.contains('George Bush'),'President'] = 'George H.W. Bush'
spoken.loc[spoken['President'].str.contains('William J. Clinton'),'President'] = 'William (Bill) Clinton'
spoken.loc[spoken['President'].str.contains('Donald J. Trump'),'President'] = 'Donald Trump'
spoken.loc[spoken['President'].str.contains('Joseph R. Biden'),'President'] = 'Joe Biden'

spoken = spoken.merge(affil,left_on='President',right_on='President Name')

spoken = spoken.sort_values(by=['Minutes'])
