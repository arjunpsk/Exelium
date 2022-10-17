# Scrape bayut.com
"""
Commented to show all the elements I need to scrape from the website. 

Root element of each listing = ef447dde

Name = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[1]
Price = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[2]/div/span[3]
Sqft = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[3]/div/div/span[3]/span[2]
URL = //*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[1]/a

Name = class="_7afabd84"
Price = class="f343d9ce"
Sqft = class="b6a29bc0"
URL = class="_287661cb"

links = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "_357a9937"))).find_elements(By.CSS_SELECTOR, "li>article>._4041eb80>a")

"""


import pandas as pd

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

Name = '//*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[1]'
Price = '//*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[2]/div/span[3]'
Sqft = '//*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[3]/div/div/span[3]/span[2]'
URL = '//*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[1]/a'

# Function to scrape from URL

def open_chrome_new():
    name = []
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    driver.maximize_window() # For maximizing window
    driver.implicitly_wait(10) # gives an implicit wait for 20 seconds
    
    # listings = driver.find_elements(By.CLASS_NAME, "ef447dde").text
    listings = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "_357a9937"))).find_elements(By.CLASS_NAME, "ef447dde") # works
    # listings = wait.until(EC.presence_of_element_located((By.NAME , "_357a9937"))).find_elements(By.NAME, "ef447dde")
   
    print(listings)
    print("HELLO WORLD - HELLO WORLD - HELLO WORLD - HELLO WORLD - HELLO WORLD - HELLO WORLD - HELLO WORLD - HELLO WORLD")

    for listing in listings:
        list_name = listing.find_element(By.XPATH, '//*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[1]')
        list_price = listing.find_element(By.XPATH, '//*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[2]/div/span[3]').text
        list_sqft = listing.find_element(By.XPATH, '//*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[3]/div[3]/div[3]/div/div/span[3]/span[2]').get_attribute(".b6a29bc0")
        list_url = listing.find_element(By.XPATH, '//*[@id="body-wrapper"]/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/article/div[1]/a').get_attribute("href")
        # print(list_name, list_price, list_sqft, list_url)
        print(listing, list_price, list_url, end="\n")
        # list_url = listing.find_element(By.NAME, "_287661cb")


        # print(list_name, list_price, list_sqft, list_url, "NEXT", len(listings))
        # print(list_url)
        
    
    # for listing in listings:
    #     list_name = listing.find_element(By.XPATH, Name).text
    #     list_price = listing.find_element(By.

    #     list_price = listing.find_element(By.XPATH, Price).text
    #     list_sqft =listing.find_element(By.XPATH, Sqft).text
    #     list_url = listing.find_element(By.XPATH, URL).text

    # try:

    #     wait = WebDriverWait(driver, 10)
    #     # elements = wait.until(EC.presence_of_element_located((By.ID , "table-rows"))).find_elements_by_css_selector("tr>td>a")
    #     # links = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "_357a9937"))).find_elements(By.CSS_SELECTOR, "li>article>._4041eb80>a")
    #     prices = wait.until(EC.presence_of_element_located((By.CLASS_NAME , "ef447dde"))).find_elements(By.CLASS_NAME, "li>article>._4041eb80>a")

    #     # f343d9ce
    #     print(prices)
    #     urls = []
    #     prices = []
    #     for element in prices:
    #         print(element.get_attribute("href"))
    #         print(element.text)
    #         urls.append(element.get_attribute("href"))
    #     # dictionary of lists  
    #     # dict = {'price': prices, 'website': urls}  
    #     # for element in prices:
    #     #     print(element.text)
    #     # df = pd.DataFrame(dict) 
            
    #     # # saving the dataframe 
    #     # df.to_csv('./result.csv') 
       
    # finally:
    #     driver.quit()
    driver.implicitly_wait(10) # gives an implicit wait for 20 seconds

    driver.close()
    driver.quit()
    
open_chrome_new()