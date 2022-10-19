# Final project: Exelium 
# Create a prototype for real estate analysis. 

"""
Commented to show all the elements I need to scrape from the website. 

Root element of each listing = ef447dde

XPATHS of Elements
Name = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[1]
Price = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[2]/div/span[3]
Area = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[3]/div/div/span[3]/span[2]
URL = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[1]/a

CLASS NAMES of Elements
Name = class="_7afabd84"
Price = class="f343d9ce"
Area = class="b6a29bc0"
URL = class="_287661cb"

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
from pickle import APPEND
import pandas as pd
import numpy as np
from IPython.display import display
import math 

# Import selenium webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# Waiting
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# create webdriver object
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = ChromeService(executable_path = r'./Driver/chromedriver')

driver = webdriver.Chrome(service=service, options=options)

# Variable to set the URL. 
# I am using a .env file to load the URL in case the URL link triggers any alerts on the main site and flags my ip.
url = os.getenv('URL')

# Function to scrape from pre-defined URL

def first_deliverable():
    try:    
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        driver.maximize_window() # For maximizing window
        driver.implicitly_wait(10) # gives an implicit wait for 20 seconds
        
        # listings = driver.find_elements(By.CLASS_NAME, "ef447dde").text
        listings = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "_357a9937"))).find_elements(By.CLASS_NAME, "ef447dde") # works

        # Each search parameter is 
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

        for listing in listings:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_7afabd84')))

            List_dict={
            'Name':listing.find_element(By.CLASS_NAME, '_7afabd84').text,
            'Price':listing.find_element(By.CLASS_NAME, 'f343d9ce').text,
            'URL':listing.find_element(By.CLASS_NAME, '_287661cb').get_attribute("href")
            }

            details_of_listing.append(List_dict)

            # The sqft details are wrapped in one class 'b6a29bc0' along with the 'Beds' and 'Baths'.
            # So every time 'b6a29bc0' is scrapped, it returns 3 values. 
            # This means that I have to first scrape it, append to a list, 
            # and then reshape it into an array of (-1, 3)

            # All of this fails if one of these values ('Beds', 'Bath', 'Area') are missing from the listing 
            # since it no longer remains a multiple of 3.
            list_sqft = listing.find_elements(By.CLASS_NAME, 'b6a29bc0')

            for element in list_sqft:
                sqft_temp.append(element.text)
                
        list_sqft = np.array(sqft_temp).reshape(-1,3)    # reshape the sqft list to an array of 3 columns.
        
        # Create DF of the two list and concat them
        df_list = pd.DataFrame(details_of_listing, columns=['Name', 'Price', 'URL'])
        df_sqft = pd.DataFrame(list_sqft, columns = ['Room', 'Bath', 'Area'])
        df_all_details = pd.concat([df_list,df_sqft], axis=1)
        display(df_all_details)

        # Remove the commas from 'Price' and 'sqft' from Area
        df_all_details['Area'] = df_all_details['Area'].map(lambda x: x.rstrip('sqft'))
        df_all_details['Price'] = df_all_details['Price'].replace(',','', regex=True)
        df_all_details['Area'] = df_all_details['Area'].replace(',','', regex=True)
        display(df_all_details.info())

        print("This is just decorative for the sake of easy readability: HELLO WORLD - MIC CHECK ONE OH - GOODBYE WORLD", end="\n\n\n")

        # Make the 'Price', 'Bath', and 'Area'
        df_all_details[["Price", "Bath", "Area"]] = df_all_details[["Price", "Bath", "Area"]].apply(pd.to_numeric)
        display(df_all_details.info())
        display(df_all_details)

        print("This is just decorative for the sake of easy readability: HELLO WORLD - MIC CHECK ONE OH - GOODBYE WORLD", end="\n\n\n")

        df_all_details["Price/sqft"] = (df_all_details["Price"]/df_all_details["Area"]).round(decimals=2)
        display(df_all_details)

        # saving the dataframe 
        df_all_details.to_csv('./result.csv') 
    
    finally: # regardsless of outcome above kill the driver because unclosed drivers are killing my flow.

        driver.implicitly_wait(10) # gives an implicit wait for 20 seconds 
        driver.close()
        driver.quit()
    
first_deliverable()

 

