import os
from dotenv import load_dotenv
from selenium import webdriver
import pandas as pd
import time
import math
from src.exception import CustomException
from src.logger import logging
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from scripts.preprocess_data import preprocessor
from scripts.scraper import scrape_data, wait_for_header
import sys
load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/CWC/AppData/Local/Google/Chrome/User Data")
options.add_argument("--profile-directory=Default")
CHROMEDRIVER = Service("E:/Projects/WEBDRIVER/chromedriver_124.exe")

website_page = os.getenv("INTERNSHALA_PAGE_URL")
driver = webdriver.Chrome(service=CHROMEDRIVER, options=options)
driver.get(website_page)
wait = WebDriverWait(driver, 10)

header_string_xpath = 'https://internshala.com/internships/apis,analytics,business-analysis,data-analysis,data-analytics,data-science,google-suite-g-suite,google-workspace,ms-sql-server,market-business-research,mysql,power-bi,product,product-management,product-strategy,programming,python,research-and-analytics,sql,selenium,sports,statistical-modeling,tableau,artificial-intelligence-internship/page-1/'
header_string = driver.find_element(by='xpath', value=header_string_xpath).text
total_posts = int(header_string.split()[0])
number_of_pages = math.ceil(total_posts/40)

try:
    df = scrape_data(driver, wait)
except Exception as e:
    raise CustomException(e, sys)

try:
    if number_of_pages > 1:
        for page_number in range(2, 3):
            website_page = website_page.replace(website_page[-2], str(page_number))
            driver.execute_script("window.open('', '_blank');")
            driver.switch_to.window(driver.window_handles[page_number-1])
            driver.get(website_page)
            wait_for_header(header_string_xpath, wait)
            new_df = scrape_data(driver, wait)
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            time.sleep(2)
except Exception as e:
    raise CustomException(e, sys)
finally:
    driver.quit()

df, date_variable = preprocessor(df)

file_name = f"{date_variable} Scraped {df.shape[0]} opportunities.xlsx"
folder_name = 'Scraped Data'
file_path = os.path.join(folder_name, file_name)

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Save the DataFrame to Excel
df.to_excel(file_path, index=False)


