from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import pandas as pd

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_table_to_load(driver, table_selector, num_rows):
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, table_selector)))
    num_current_rows = len(table.find_elements(By.TAG_NAME, "tr")) - 1 # minus 1 to exclude header row
    while num_current_rows < num_rows:
        time.sleep(1) # wait for 1 second
        num_current_rows = len(table.find_elements(By.TAG_NAME, "tr")) - 1

url = "https://indexes.morningstar.com/our-indexes/details/morningstar-us-small-cap-FSUSA00KGS?currency=USD&variant=TR&tab=performance"

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
        
    return temp_df, html

test = web_scrape(url)