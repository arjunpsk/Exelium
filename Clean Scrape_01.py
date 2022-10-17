# Scrape bayut.com
"""
Commented to show all the elements I need to scrape from the website. 

Root element of each listing = ef447dde

XPATHS of Elements
Name = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[1]
Price = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[2]/div/span[3]
Sqft = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[3]/div/div/span[3]/span[2]
URL = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[1]/a

CLASS NAMES of Elements
Name = class="_7afabd84"
Price = class="f343d9ce"
Sqft = class="b6a29bc0"
URL = class="_287661cb"

links = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "_357a9937"))).find_elements(By.CSS_SELECTOR, "li>article>._4041eb80>a")

"""


from array import array
from pickle import APPEND
import pandas as pd
import numpy as np
from IPython.display import display


# waiting
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

service = ChromeService(executable_path = r'./Driver/chromedriver')

# create webdriver object
driver = webdriver.Chrome(service=service, options=options)

# Variable to set the URL
url = "https://www.bayut.com/for-sale/property/dubai/jumeirah-lake-towers-jlt/"

# Function to scrape from URL

def open_chrome_new():
    try:    
        name = []
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        driver.maximize_window() # For maximizing window
        driver.implicitly_wait(10) # gives an implicit wait for 20 seconds
        
        # listings = driver.find_elements(By.CLASS_NAME, "ef447dde").text
        listings = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "_357a9937"))).find_elements(By.CLASS_NAME, "ef447dde") # works
    
        print("The number of properties found:", len(listings), end="\n\n\n\n\n\n")

        print("This is just decorative for the sake of easy readability: \n\n\n*************** STARTS FROM HERE ***************", end="\n\n\n")

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

            list_sqft = listing.find_elements(By.CLASS_NAME, 'b6a29bc0')

            details_of_listing.append(List_dict)

            for element in list_sqft:
                sqft_temp.append(element.text)
                
        list_sqft = np.array(sqft_temp).reshape(-1,3)    # reshape the sqft list to an array of 3 columns.
        
        df_list = pd.DataFrame(details_of_listing, columns=['Name', 'Price', 'URL'])
        df_sqft = pd.DataFrame(list_sqft, columns = ['Room', 'Bath', 'Sqft'])

        df_all_details = pd.concat([df_list,df_sqft], axis=1)
        display(df_all_details)

        df_all_details['Sqft'] = df_all_details['Sqft'].map(lambda x: x.rstrip('sqft'))
        df_all_details['Price'] = df_all_details['Price'].replace(',','', regex=True)
        df_all_details['Sqft'] = df_all_details['Sqft'].replace(',','', regex=True)

        display(df_all_details.info())

        print("This is just decorative for the sake of easy readability: HELLO WORLD - MIC CHECK ONE OH - GOODBYE WORLD", end="\n\n\n")

        df_all_details[["Price", "Bath", "Sqft"]] = df_all_details[["Price", "Bath", "Sqft"]].apply(pd.to_numeric)
        display(df_all_details.info())
        display(df_all_details)

        print("This is just decorative for the sake of easy readability: HELLO WORLD - MIC CHECK ONE OH - GOODBYE WORLD", end="\n\n\n")

        df_all_details["Price/sqft"] = (df_all_details["Price"]/df_all_details["Sqft"]).round(decimals=2)
        display(df_all_details)

        # saving the dataframe 
        df_all_details.to_csv('./result.csv') 
        
    
    finally: # regardsless of outcome above kill the driver because unclosed drivers are killing my flow.

        driver.implicitly_wait(10) # gives an implicit wait for 20 seconds 
        driver.close()
        driver.quit()
    
open_chrome_new()