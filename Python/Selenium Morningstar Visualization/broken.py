#%% imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

url = "https://indexes.morningstar.com/our-indexes/details/morningstar-us-small-cap-FSUSA00KGS?currency=USD&variant=TR&tab=performance"
url = "https://indexes.morningstar.com/indexes/details/morningstar-developed-markets-ex-us-FS00009P5R?currency=USD&variant=TR&tab=performance"

#%%
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
driver.execute_script("window.scrollBy(0, 600);")

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
driver.implicitly_wait(1000)

# select volume data
filter_button = driver.find_element(By.CSS_SELECTOR, '[data-id="priceVolumeDetail"]')
filter_button.click()
driver.implicitly_wait(1000)
driver.execute_script("window.scrollBy(0, 600);")

select_chart.click()

# select all data
dropdown_button = driver.find_elements(By.CSS_SELECTOR,'[class="mds-select___markets mds-select--small___markets"]')
dropdown_button = dropdown_button[1]#class="mds-icon___markets mds-button__icon___markets"
dropdown_button.click()
driver.implicitly_wait(1000)

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