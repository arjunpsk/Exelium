# Final project: Exelium 
# Create a prototype for real estate analysis. 

"""
Commented to show all the elements I need to scrape from the website. 

Root element of each listing = ef447dde

CLASS NAMES of Elements
Name = class="_7afabd84"
Price = class="f343d9ce"
Sqft = class="b6a29bc0"
URL = class="_287661cb"
Beds = class="_0c8a5353 c1b40987"
Baths = class="_0c8a5353 fa6c05cc"
Area = class="_0c8a5353 d2db01cb"

links = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "_357a9937"))).find_elements(By.CSS_SELECTOR, "li>article>._4041eb80>a")

FILTER PARAMETERS: 
Enter location :  Input field
Purpose : Rent, Buy
Rent frequency : Yearly, Monthly, Weekly, Daily, Any
Beds : Studio, 1, 2, 3, 4, 5, 6, 7, 8+
Baths : 1, 2, 3, 4, 5, 6+
Minimum sqft : Input field
Maximum sqft : Input field
Minimum Price : Input field
Maximum Price : Input field
Residential : Apartment, Townhouse, Villa Compound, Residential Plot, Residential Building,
                Villa, Penthouse, Hotel Apartment, Residential Floor
Commercial : Office, Warehouse, Commercial Villa, Commercial Plot, Commercial Building,
                Industrial Land, Showroom, Shop, Labour Camp, Bulk Unit, Commercial Floor, 
                Factory, Mixed Use Land, Other Commercial
"""

from ast import Num
import os

# Setting environment file
from dotenv import load_dotenv
load_dotenv()

from array import array
from pickle import APPEND, TRUE
import pandas as pd
import numpy as np
from IPython.display import display
import math 
import time
import csv
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
file_name = str(current_time.year) + str(current_time.month) + str(current_time.day) + str(current_time.hour) + str(current_time.second)

# create webdriver object
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = ChromeService(executable_path = r'./Driver/chromedriver')

driver = webdriver.Chrome(service=service, options=options)

# Variable to set the URL. 
# I am using a .env file to load the URL in case the URL link triggers any alerts on the main site and flags my ip.
url = os.getenv('URL3')

# Function to scrape from pre-defined URL

# def get_locations():
    # scrape locations and url
    # save to locay.csv
    # Exit function

# def user_input_location():
#     # User gets a dropdown of locations
#     # They select location 
#     # Then call def first_deliverable():
      
def scrape_properties():
    # Create an empty CSV
    # with open("results_01.csv", "w") as my_empty_csv:
    #     my_empty_csv.write('Name, Price, URL, Room, Bath, Sqft, Price/sqft \n')

    try:    
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        driver.maximize_window() # For maximizing window
        driver.implicitly_wait(10) # gives an implicit wait for 20 seconds
        
        # The number of searches visible at any given time is 24 listings per page.
        # So first we have to find the total number of properties in a given search parameter. 
        # Then dividing the total number of properties by 24 to see how many pages to be scraped from.
        total_prop_temp = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_6cab5d36'))).find_element(By.CLASS_NAME, "ca3976f7")
        total_prop = total_prop_temp.text
        total_prop = total_prop.replace(',',"")
        total_prop = [int(s) for s in total_prop.split() if s.isdigit()]
        total_prop = total_prop[2]
        pagnation = math.ceil(total_prop/24)

        print("This is just decorative for the sake of easy readability: \n\n\n*************** STARTS FROM HERE ***************", end="\n\n\n")
        print("The number of properties found:", total_prop, end="\n\n")
        print("The number of pages to scrape properties from:", pagnation, end="\n\n")

        print("This is just decorative for the sake of easy readability: HELLO WORLD - MIC CHECK ONE OH - GOODBYE WORLD", end="\n\n\n")

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
                # 'Beds':listing.find_element(By.XPATH, '//*[@aria-label="Beds"]').text,
                # 'Bath':listing.find_element(By.XPATH, '//*[@aria-label="Baths"]').text,
                'Sqft':listing.find_element(By.XPATH, '//*[@aria-label="Area"]').text
                }
                # //./span[@aria-label="Area"]

                details_of_listing.append(List_dict)
  
            df_all_details = pd.DataFrame(details_of_listing, columns=['Name', 'URL', 'Sqft', 'Price'])
            # df_sqft = pd.DataFrame(list_sqft_01, columns = ['Room', 'Bath', 'Sqft'])
            # print(df_all_details)
            # Concat both DFs
            # df_all_details = pd.concat([df_list, df_sqft], axis=1)
            df_all_details['Sqft'] = df_all_details['Sqft'].map(lambda x: x.rstrip('sqft'))
            df_all_details['Price'] = df_all_details['Price'].replace(',','', regex=True)
            df_all_details['Sqft'] = df_all_details['Sqft'].replace(',','', regex=True)
            # df_all_details[["Price", "Bath", "Sqft"]] = df_all_details[["Price", "Bath", "Sqft"]].apply(pd.to_numeric)
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
        df_all_details.to_csv('Properties_' + file_name + '.csv', mode='w', index=True, header=True)
        display(df_all_details)

        driver.implicitly_wait(10) 
        driver.close()
        driver.quit()

scrape_properties()



