import pandas as pd
url = r'https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/annual-messages-congress-the-state-the-union-0'
df = pd.read_html(url) # Returns list of all tables on page
df = df[0]

del url

df.columns = df.iloc[0]
df = df.drop(df[df['President']=='President'].index)

df = df.drop(df[df['President'].str.contains('NOT')== True].index)
df = df.fillna(method='ffill')

spoken = df[df['Format'] == 'spoken']

import plotly.express as px

fig = px.bar(spoken.groupby('President').President.count(), x=spoken.groupby('President').President.count().index, y="President")
fig.show()