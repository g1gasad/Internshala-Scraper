import os
import sys
from dotenv import load_dotenv
from selenium import webdriver
import pandas as pd
import time
import math
from src.logger import logging
from src.exception import CustomException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from scripts.preprocess_data import preprocessor
from scripts.scraper import scrape_data, wait_for_header
load_dotenv()

def automation(posts_per_page, pages_to_scrape):

    options = webdriver.ChromeOptions()
    options.add_argument(os.getenv("CHROME_PATH"))
    options.add_argument(os.getenv("DEFAULT_PROFILE_PATH"))
    CHROMEDRIVER = Service(os.getenv("CHROMEDRIVER_PATH"))
    website_page = os.getenv("INTERNSHALA_PAGE_URL")
    header_string_xpath = os.getenv("HEADER_STRING_XPATH")
    
    logging.info("Loaded environment variables")
    driver = webdriver.Chrome(service=CHROMEDRIVER, options=options)
    
    logging.info("Starting automation")
    
    driver.get(website_page)
    wait = WebDriverWait(driver, 10)

    header_string = driver.find_element(by='xpath', value=header_string_xpath).text
    total_posts = int(header_string.split()[0])
    number_of_pages = math.ceil(total_posts / posts_per_page)

    df = scrape_data(driver, wait)
    
    logging.info("Scraped data from Page:1")
    
    try:
        if number_of_pages > 1:
            for page_number in range(2, pages_to_scrape + 1):
                website_page = website_page.replace(website_page[-2], str(page_number))
                driver.execute_script("window.open('', '_blank');")
                driver.switch_to.window(driver.window_handles[page_number-1])
                driver.get(website_page)
                wait_for_header(header_string_xpath, wait)
                new_df = scrape_data(driver, wait)
                
                logging.info(f"Scraped data from Page:{page_number}")
                
                df = pd.concat([df, new_df], axis=0, ignore_index=True)
                
                logging.info(f"Concatenated data from Page:{page_number}")
                
                time.sleep(2)
                
    except Exception as e:
        logging.error(f"Error: {e}")
        raise CustomException(e, sys)
    
    finally:
        driver.quit()

    df, date_variable = preprocessor(df)

    file_name = f"{date_variable} Scraped {df.shape[0]} opportunities.xlsx"
    folder_name = 'ScrapedData'
    file_path = os.path.join(folder_name, file_name)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Save the DataFrame to Excel
    df.to_excel(file_path, index=False)

    logging.info("Saved data to Excel")

