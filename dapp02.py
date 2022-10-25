import streamlit as st
import pandas as pd
import numpy as np
import math 
import os
import time

from array import array
import pandas as pd
from IPython.display import display
from datetime import datetime

# Import selenium webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Waiting
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# using now() to get current time
current_time = datetime.now()

# create webdriver object
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = ChromeService(executable_path = r'./Driver/chromedriver')

file_name = str(current_time.year) + str(current_time.month) + str(current_time.day) + "_" + str(current_time.hour) + "_" + str(current_time.minute) + "_" + str(current_time.second)

url = "https://www.bayut.com/for-sale/property/abu-dhabi/"

header = st.container()
container_url = st.container()
container_properties = st.container()

@st.cache(suppress_st_warning=True)
def get_urls(filename):
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 1)
    st.write("Cache miss: Hey Arjun, Function ran even though @st.cache is defined.")
# try:    
    driver.get(url)
    driver.maximize_window()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "f1ab04e0"))).find_element(By.CLASS_NAME, "_44977ec6").click()

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

    url_list = pd.DataFrame(locations, columns=['Name', 'URL', 'Properties'])

    # Save to a CSV file. 
    url_list.to_csv(filename, mode='w', index=False, header=True)

    # display(url_list) 
    
    driver.close()
    driver.quit()
    return url_list # this is the addition for the streamlit app.


@st.cache(suppress_st_warning=True)
def scrape_properties():

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    service = ChromeService(executable_path = r'./Driver/chromedriver')

    driver = webdriver.Chrome(service=service, options=options)

    url = os.getenv('URL3')

    try:    
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        driver.maximize_window()
        
        # The number of searches visible at any given time is 24 listings per page.
        # So first we have to find the total number of properties in a given search parameter. 
        # Then dividing the total number of properties by 24 to see how many pages to be scraped from.
        total_prop_temp = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_6cab5d36'))).find_element(By.CLASS_NAME, "ca3976f7")
        total_prop = total_prop_temp.text
        total_prop = total_prop.replace(',',"")
        total_prop = [int(s) for s in total_prop.split() if s.isdigit()]
        total_prop = total_prop[2]
        pagnation = math.ceil(total_prop/24)

        # Define list variables 
        sqft_temp = []
        details_of_listing = []

        pagecounter = 0
        
        for i in range(pagnation):
            # listings = driver.find_elements(By.CLASS_NAME, "ef447dde").text
            listings = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "_357a9937"))).find_elements(By.CLASS_NAME, "ef447dde") # works
          
            for listing in listings:

                wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_7afabd84')))

                List_dict={
                'Name':listing.find_element(By.CLASS_NAME, '_7afabd84').text,
                'Price':listing.find_element(By.CLASS_NAME, 'f343d9ce').text,
                'URL':listing.find_element(By.CLASS_NAME, '_287661cb').get_attribute("href"),
                'Sqft':listing.find_element(By.XPATH, '//*[@aria-label="Area"]').text
                }

                details_of_listing.append(List_dict)
  
            df_all_details = pd.DataFrame(details_of_listing, columns=['Name', 'URL', 'Sqft', 'Price'])
            df_all_details['Sqft'] = df_all_details['Sqft'].map(lambda x: x.rstrip('sqft'))
            df_all_details['Price'] = df_all_details['Price'].replace(',','', regex=True)
            df_all_details['Sqft'] = df_all_details['Sqft'].replace(',','', regex=True)
            df_all_details[["Price", "Sqft"]] = df_all_details[["Price", "Sqft"]].apply(pd.to_numeric)
            df_all_details["Price/sqft"] = (df_all_details["Price"]/df_all_details["Sqft"]).round(decimals=2)
            display(df_all_details)
             
            try:    

                #Checks if there are more pages with links 
                next_link = driver.find_element(By.XPATH, "//a[@title='Next']")
                next_link.click() 
                time.sleep(5) 
                print(pagecounter)
                pagecounter += 1

            except NoSuchElementException: 
                print("Oh ho, You're reached the end of the road here, buddy.")

    finally: # regardsless of outcome above kill the driver because unclosed drivers are killing my flow.

        # Save to a CSV file. 
        df_all_details.to_csv('Properties_' + file_name + '.csv', mode='w', index=False, header=True)
        display(df_all_details)

        driver.implicitly_wait(10) 
        driver.close()
        driver.quit()


with header:
    st.title('Welcome to my project')
    st.text("This project has two steps. First is to scrape the URL's of the properties in Dubai.\n" 
    "Second step is to then offer the scraped URL's to the user for selection.\n"
    "Third step is to then scrape all the properties from the user selected URL/property")

with container_url:
    st.title('Scrapped URLs')

    url_list = get_urls('Location_URLs_.csv')
    st.write("Calling Arjun's get_urls() function.")
    option = st.selectbox('Select your asset:', url_list) 
    st.write('You selected:', option)
    st.dataframe(url_list)

# with container_properties:
    # def choosing_asset():
        # choosing_asset() I will scrape another URL based on the choice made from the list of URL's returned from def get_urls(filename):


