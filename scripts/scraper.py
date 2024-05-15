import pandas as pd
import time
from src.exception import CustomException
from src.logger import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

def wait_for_header(header_string_xpath, wait):
    wait.until(EC.visibility_of_element_located((By.XPATH, header_string_xpath)))
    

def scrape_data(driver, wait):
    scroll_increment = 1000  # Adjust this value to control the scroll speed
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # print(page_height)
    for _ in range(0, page_height, scroll_increment):
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(0.1)

    # This returns a list of TAB CONTAINERS
    containers = driver.find_elements(by='xpath', value='//div[@class="container-fluid individual_internship visibilityTrackerItem "]')
    print(len(containers))

    names = []
    links = []
    companies = []      
    locations = []
    start_dates = []
    durations = []
    salaries = []
    employment_types = []
    statuses = []

    for container in containers:
        name = container.find_element(by='xpath', value='.//h3[@class="heading_4_5 profile"]').text
        print(name)
        
        try:
            link = container.find_element(by='xpath', value='.//a[@class="button_easy_apply_t view_detail_button"]').get_attribute('href')
        except Exception as e:
            raise CustomException(e, sys)
        
        company = container.find_element(by='xpath', value='.//div[@class="company_and_premium"]/p').text
        try:
            multiple_locations = []
            loc_list = container.find_elements(by='xpath', value='.//div[@id="location_names"]/span/a')
            if len(loc_list) > 1:
                for ele in loc_list:
                    multiple_locations.append(ele.text)
                locations.append(multiple_locations)
            else:
                location = container.find_element(by='xpath', value='.//div[@id="location_names"]/span/a').text
                locations.append(location)
        except Exception as e:
            print(f"An Exception Error {e}")

        try:    
            start_date = container.find_element(by='xpath', value='.//div[@id="start-date-first"]/span[2]').text
        except:
            start_date = "Could Not Fetch"

        try:
            duration = container.find_element(by='xpath', value='.//div[@class="other_detail_item "][2]/div[@class="item_body"]').text
        except:
            duration = container.find_element(by='xpath', value='.//div[@class="other_detail_item large_stipend_text"][2]/div[@class="item_body"]').text
        # print(start_date, duration)
        try:
            salary = container.find_element(by='xpath', value='.//span[@class="stipend"]').text
        except:
            salary = "Could Not Fetch"
            print(salary)
        employment_type = container.find_element(by='xpath', value='.//div[@class="other_label_container"]/div[1]/div').text
        status = container.find_element(by='xpath', value='.//div[@class="success_and_early_applicant_wrapper"]/div').text
        
        names.append(name)
        links.append(link)
        companies.append(company)
        start_dates.append(start_date)
        durations.append(duration)
        salaries.append(salary)
        employment_types.append(employment_type)
        statuses.append(status)

    data = {
            "Name": names,
            "Link": links,
            "Location": locations,
            "Company": companies,
            "Start Date": start_dates,
            "Duration": durations,
            "Salary": salaries,
            "Employment Type": employment_types,
            "Status": statuses
            }
    df = pd.DataFrame(data)
    
    logging.info("DataFrame Created")
    
    return df