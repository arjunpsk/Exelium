import streamlit as st
import pandas as pd
import numpy as np
import csv
import subprocess
import sys
from st_aggrid import AgGrid
import os
import math 
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


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = ChromeService(executable_path = r'./Driver/chromedriver')

url = "https://www.bayut.com/for-sale/property/abu-dhabi/"

header = st.container()
cont_url = st.container()
cont_properties = st.container()

# using now() to get current time for the file name
current_time = datetime.now()
file_name = str(current_time.year) + str(current_time.month) + str(current_time.day) + "_" + str(current_time.hour) + "_" + str(current_time.minute) + "_" + str(current_time.second)
CSV_filename = 'Properties_' + file_name + '.csv'

@st.experimental_memo(suppress_st_warning=True)
def get_urls(filename):
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 1)
    # st.write("Cache miss: Hey Arjun, Function ran even though @st.cache is defined.")
# try:    
    driver.get(url)
    driver.maximize_window() # For maximizing window
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "f1ab04e0"))).find_element(By.CLASS_NAME, "_44977ec6").click()

    locations = []

    listings = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "b7a55500"))).find_elements(By.CLASS_NAME, "_1c4ffff0") # works
    for listing in listings:

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_7afabd84')))

        List_dict={
        'Name':listing.find_element(By.CLASS_NAME, '_9878d019').text,
        'Properties':listing.find_element(By.CLASS_NAME, '_1f6ed510').text,
        'URL':listing.find_element(By.CLASS_NAME, '_9878d019').get_attribute("href")
        }

        locations.append(List_dict)

    url_list = pd.DataFrame(locations, columns=['Name', 'URL', 'Properties'])
    url_list.to_csv(filename, mode='w', index=False, header=True)
    driver.close()
    driver.quit()
    return url_list # this is the addition for the streamlit app.


# def scrape_properties():
# scrape_properties() This function will scrape the URL based on the choice made from the list of URL's returned from def get_urls(filename)
@st.experimental_memo(suppress_st_warning=True)
def scrape_properties(user_selected_url):

    driver = webdriver.Chrome(service=service, options=options)

    url = user_selected_url
    wait = WebDriverWait(driver, 1)
    try:    
        driver.get(url)
        

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
        
        details_of_listing = []

        pagecounter = 0
        
        for i in range(pagnation):
            # listings = driver.find_elements(By.CLASS_NAME, "ef447dde").text
            listings = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "_357a9937"))).find_elements(By.CLASS_NAME, "ef447dde") # works
          
            for listing in listings:

                # wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_7afabd84')))

                List_dict={
                'Name':listing.find_element(By.CLASS_NAME, '_7afabd84').text,
                'Price':listing.find_element(By.CLASS_NAME, 'f343d9ce').text,
                'URL':listing.find_element(By.CLASS_NAME, '_287661cb').get_attribute("href"),
                # 'Sqft':listing.find_element(By.XPATH, '//*[@aria-label="Area"]').text
                # 'Beds':listing.find_element(By.XPATH, './/*[@class="b6a29bc0"][@aria-label="Beds"]').text,
                # 'Baths':listing.find_element(By.XPATH, './/*[@class="b6a29bc0"][@aria-label="Baths"]').text,
                'Sqft':listing.find_element(By.XPATH, './/*[@class="b6a29bc0"][@aria-label="Area"]').text
                }
                # print(listing)
                # print(listing.find_element(By.XPATH, '//li/span[@class="b6a29bc0"][@aria-label="Area"]/span').text)
                details_of_listing.append(List_dict)
  
            df_all_details = pd.DataFrame(details_of_listing, columns=['Name', 'URL', 'Sqft', 'Price'])
            df_all_details['Sqft'] = df_all_details['Sqft'].map(lambda x: x.rstrip('sqft'))
            df_all_details['Price'] = df_all_details['Price'].replace(',','', regex=True)
            df_all_details['Sqft'] = df_all_details['Sqft'].replace(',','', regex=True)
            df_all_details[["Price", "Sqft"]] = df_all_details[["Price", "Sqft"]].apply(pd.to_numeric)
            df_all_details["Price/sqft"] = (df_all_details["Price"]/df_all_details["Sqft"]).round(decimals=2)
            # display(df_all_details)
             
            try:    

                #Checks if there are more pages with links 
                next_link = driver.find_element(By.XPATH, "//a[@title='Next']")
                next_link.click() 
                # time.sleep(5) 
                print(pagecounter)
                pagecounter += 1

            except NoSuchElementException: 
                print("Oh ho, You're reached the end of the road here, buddy.")

    finally: # regardsless of outcome above kill the driver because unclosed drivers are killing my flow.

        # Save to a CSV file. 
        
        df_all_details.to_csv(CSV_filename, mode='w', index=False, header=True)
        # display(df_all_details)

        driver.implicitly_wait(3) 
        driver.close()
        driver.quit()
        return df_all_details

with cont_url:
    st.title('Properties for sale')

    url_list = get_urls('Location_URLs_.csv')
    df_url_list = pd.DataFrame(url_list)
    prop_name = url_list['Name'].tolist()
    prop_url = url_list['URL'].tolist()
    prop_numbers = url_list['Properties'].tolist()

    dic = dict(zip(prop_url, prop_name))

    user_select = st.selectbox('Select your asset:', options=prop_url, format_func=lambda x: dic[x])
# 
    # st.write("Calling Arjun's get_urls() function.")
    # option = st.selectbox('Select your asset:', url_list) 
    st.write('You selected:', user_select)
    st.dataframe(df_url_list, 1000, 250)


# with cont_properties:
    if st.button('Click me to scrape your selected property'):
        result = scrape_properties(user_select)
        # st.write('result: %s' % result)
        st.dataframe(result)