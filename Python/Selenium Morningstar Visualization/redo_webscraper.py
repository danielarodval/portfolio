#%% imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import os

#%% defining functions

def web_scrape(url):
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(1000)
    
    # Navigate to the desired webpage
    driver.get(url)
    driver.implicitly_wait(1000)
    
    # Internally navigate the webpage
    # select overview tab
    select_page = driver.find_element(By.ID, "tab-overview")
    select_page.click()
    driver.implicitly_wait(1000)
    
    # select time period bar
    select_chart = driver.find_element(By.ID, "chart-container")
    select_chart.click()
    driver.implicitly_wait(1000)
    
    buttons = driver.find_elements(By.CSS_SELECTOR,'[class="mds-button___markets mds-button--flat___markets markets-ui-button mwc-markets-chart-time-interval__btn"]')
    
    for button in buttons:
        if button.text == 'MAX':
            button.click()
    
    select_chart.click()
    
    # select table format
    table_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Table"]')
    table_button.click()
    driver.implicitly_wait(150)
    
    # select volume data
    filter_button = driver.find_element(By.CSS_SELECTOR, '[data-id="priceVolumeDetail"]')
    filter_button.click()
    driver.implicitly_wait(300)
    driver.execute_script("window.scrollBy(0, 600);")
    
    select_chart.click()
    
    # select all data
    dropdown_button = driver.find_elements(By.CSS_SELECTOR,'[class="mds-select___markets mds-select--small___markets"]')
    dropdown_button = dropdown_button[1]
    dropdown_button.click()
    driver.implicitly_wait(300)
    
    dropdown_divs = driver.find_elements(By.CSS_SELECTOR, '.mds-select___markets.mds-select--small___markets')
    dropdown_div = dropdown_divs[1]  # Use the second dropdown as per your code
    
    select_element = dropdown_div.find_element(By.TAG_NAME, 'select')
    
    select_object = Select(select_element)
    
    select_object.select_by_visible_text('All')
    
    # select table
    driver.execute_script("window.scrollBy(0, 600);")
    select_chart.click()
    driver.implicitly_wait(1000)
    select_chart.click()
    html = driver.page_source
    
    driver.implicitly_wait(1000)
    
    driver.quit()
    
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    temp_df = pd.DataFrame(columns=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
    table = table.find_all('tr')
    for row in table:
        cols = row.find_all('td')
        row_data = [col.text.strip() for col in cols]
        if len(row_data) != len(temp_df.columns):
            row_data += [''] * (len(temp_df.columns) - len(row_data))
        temp_df.loc[len(temp_df)] = row_data
        
    return temp_df

def calculate_yearly_pct_change(df, df_name):
    df['Date'] = pd.to_datetime(df['Date'])
    end_date = df['Date'].max()
    end_row = df.loc[df['Date'] == end_date]
    end_row = end_row.set_index(pd.Index([end_date.year]))

    # Filter DataFrame to only include December dates
    december_df = df[df['Date'].dt.month == 12]

    # Group data by year and select last row for each year
    end_of_year_df = december_df.groupby(december_df['Date'].dt.year).last().loc[2007:]
    final_df = pd.concat([end_of_year_df,end_row])

    final_df['Close'] = pd.to_numeric(final_df['Close'].str.replace(',', ''))
    final_df['Close_pct_change'] = final_df['Close'].pct_change()
    final_df = final_df.iloc[1:]

    final_df['Close_pct_change'] = final_df['Close_pct_change'].apply(lambda x: '{:.1f}'.format(x*100))
    
    # Transpose the DataFrame and set the index to the DataFrame name
    final_df = final_df[['Close_pct_change']].transpose()
    final_df.index = [df_name]
    
    # Set column names to years
    final_df.columns = final_df.columns.astype(str)

    return final_df

def add_fund_name(arr):
    arr_2 = []
    pct_change_df = pd.DataFrame()
    for url in arr:
        # get file name
        title = url.split("details/")[1].split("-FS")[0]
        
        # create dataframes & csv files
        df = web_scrape(url)
        df = df.loc[1:]
        df.to_csv(os.path.dirname(os.path.realpath(__file__))+"/csv_export/"+title+".csv")
        
        # process dataframe 
        pct_change_df = pd.concat([pct_change_df,calculate_yearly_pct_change(df,title)])
        
        arr_2.append([title,url,df])
        
        
    return arr_2, pct_change_df


web_urls = [
    "https://indexes.morningstar.com/our-indexes/details/morningstar-us-small-cap-FSUSA00KGS?currency=USD&variant=TR&tab=performance",
    "https://indexes.morningstar.com/indexes/details/morningstar-us-large-cap-FSUSA00KH5?currency=USD&variant=TR&tab=performance",
    "https://indexes.morningstar.com/indexes/details/morningstar-developed-markets-ex-us-FS00009P5R?currency=USD&variant=TR&tab=performance",
    "https://indexes.morningstar.com/indexes/details/morningstar-emerging-markets-FS00009P5Q?currency=USD&variant=TR&tab=performance",
    "https://indexes.morningstar.com/indexes/details/morningstar-us-5-10-yr-treasury-bond-FS0000E728?currency=USD&variant=TR&tab=performance",
    "https://indexes.morningstar.com/indexes/details/morningstar-us-5-10-yr-corporate-bond-FS0000DZER?currency=USD&variant=TR&tab=performance",
    "https://indexes.morningstar.com/indexes/details/morningstar-us-high-yield-bond-FS0000E18W?currency=USD&variant=TR&tab=performance",
    "https://indexes.morningstar.com/indexes/details/morningstar-moderate-target-risk-FSUSA09PYI?currency=USD&variant=TR&tab=performance"
]

arr_web_urls, pct_change_df = add_fund_name(web_urls)

#%% visualization
import matplotlib.pyplot as plt
import numpy as np

# Convert percentage strings to float
df_float = pct_change_df.applymap(lambda x: float(x) if isinstance(x, str) else x)
# Prepare data
#print(df_float)
years = df_float.columns
asset_classes = df_float.index

# Create a custom colormap
cmap = plt.get_cmap("viridis")
cmap.set_bad(color="white")

# Prepare the data as a masked array
masked_data = np.ma.masked_invalid(df_float.to_numpy())

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(16, 8))

# Display the data as blocks
cax = ax.imshow(masked_data, cmap=cmap, aspect='auto')

# Set labels and ticks
ax.set_xticks(range(len(years)))
ax.set_xticklabels(years)
ax.set_yticks(range(len(asset_classes)))
ax.set_yticklabels(asset_classes)

# Add a colorbar
cbar = fig.colorbar(cax, ax=ax)

# Loop through rows and columns of the normalized dataframe
for i in range(len(asset_classes)):
    for j in range(len(years)):
        # Add the value as text at the center of the cell
        ax.annotate(df_float.iloc[i, j], xy=(j, i),
                    ha='center', va='center', color='white')

ax.set_title('Asset Class Winners and Losers')
        
# Show the plot
plt.show()

del df_float, years, asset_classes, cmap, masked_data, fig, ax, cax, cbar, i, j
# %% plotly graphs
import plotly.express as px

# Create the heatmap plot
fig = px.imshow(pct_change_df,
                labels=dict(x="Years", y="Asset Class", color="Percentage"),
                x=pct_change_df.columns,
                y=pct_change_df.index,
               )

# Update the layout and x-axis
fig.update_xaxes(side="top")
fig.update_layout(title="Asset Class Winners and Losers")

# Add percentage values to the heatmap
for i, row in enumerate(pct_change_df.index):
    for j, col in enumerate(pct_change_df.columns):
        value = pct_change_df.loc[row, col]
        fig.add_annotation(dict(x=j, y=i, text=value, ax=0, ay=0, xref="x", yref="y", 
                                showarrow=False, font=dict(size=12, color="white")))

fig.show()

del fig, i, row, j, col, value
# %% plotly graphs
# Convert the dataframe to long format
df_long = df_float.reset_index().melt(id_vars="index", var_name="Year", value_name="Percentage")
df_long.columns = ['Asset Class', 'Year', 'Percentage']

# Create the heatmap-like plot using px.bar
fig = px.bar(df_long,
             x="Year",
             y="Percentage",
             color="Asset Class",
             text="Percentage",
             labels={"Year": "Years", "Percentage": "Percentage", "Asset Class": "Asset Class"},
             color_discrete_sequence=px.colors.qualitative.Pastel,
             width=1000,
             height=600)

# Customize the plot appearance
fig.update_layout(title="Asset Class Winners and Losers")
fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

fig.show()