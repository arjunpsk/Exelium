# Locations = class="f1ab04e0"
# Single location = class="_1c4ffff0"

# from ast import Num
import os

# Setting environment file
from dotenv import load_dotenv
load_dotenv()

from array import array
# from pickle import APPEND, TRUE
import pandas as pd
# import numpy as np
from IPython.display import display
from datetime import datetime

# Import selenium webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException

# Waiting
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# using now() to get current time
current_time = datetime.now()
file_name = str(current_time.year) + str(current_time.month)

# create webdriver object
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = ChromeService(executable_path = r'./Driver/chromedriver')

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)
# driver.implicitly_wait(10) # gives an implicit wait for 20 seconds

# driver.implicitly_wait(10) # gives an implicit wait for 20 seconds

url = os.getenv('BASE_URL')
      
def get_urls():
  
    try:    
        driver.get(url)
        driver.maximize_window() # For maximizing window
        
        # The number of searches visible at any given time is 24 listings per page.
        # So first we have to find the total number of properties in a given search parameter. 
        # Then dividing the total number of properties by 24 to see how many pages to be scraped from.
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "f1ab04e0"))).find_element(By.CLASS_NAME, "_44977ec6").click()
        # time.sleep(10)
    
# _1c4ffff0

        # print("This is just decorative for the sake of easy readability: \n\n\n*************** STARTS FROM HERE ***************", end="\n\n\n")
   

        # print("This is just decorative for the sake of easy readability: HELLO WORLD - MIC CHECK ONE OH - GOODBYE WORLD", end="\n\n\n")

        # Define list variable 
        locations = []

        listings = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "b7a55500"))).find_elements(By.CLASS_NAME, "_1c4ffff0") # works
        for listing in listings:

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_7afabd84')))

            List_dict={
            'Name':listing.find_element(By.CLASS_NAME, '_9878d019').text,
            'URL':listing.find_element(By.CLASS_NAME, '_9878d019').get_attribute("href"),
            'Properties':listing.find_element(By.CLASS_NAME, '_1f6ed510').text
            }

            locations.append(List_dict)

        df_all_details = pd.DataFrame(locations, columns=['Name', 'URL', 'Properties'])
        # display(df_all_details)

    finally: # regardsless of outcome above kill the driver because unclosed drivers are killing my flow.

        # Save to a CSV file. 
        # df_all_details.to_csv('Location_URLs_' + file_name + '.csv', mode='w', index=False, header=True)
        df_all_details.to_csv('Location_URLs.csv', mode='w', index=False, header=True)

        display(df_all_details)
        return(df_all_details)
        driver.close()
        driver.quit()

get_urls()


