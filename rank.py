# coding=utf-8

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import re
from datetime import datetime,timedelta
import json

tmp_list = [

]

keyword_list = [
    "journal",
    "journals",
    "planner",
    "leather+journal",    # 50000 search
    "leather+notebook",   # 19700 search
    "travel+journal",     # 15800 search
    "notebook+journal",   # 13800
    "journal+notebook",   # 8000
    "travelers+notebook",  # 8000 search
    "vintage+journal",     # 8000 search
    "leather+bound+journal",  # 7900
    "japanese+notebook",  # 7078
    "leather+planner",    # 5400
    "notebook+binder",    # 5100
    "drawing+notebook",   # 5120
    "pink+notebook",      # 5120
    "leather+journal+for+men",  # 5120
    "leather+journal+for+women", # 5120
    "planner+notebook",  # 4293
    "refillable+notebook",  # 4200
    "refillable+journal",   # 4000

    "traveler+journal",
    "traveler+notebook",
    "travelers+journal",

    "refillable+leather+journal",
    "refillable+leather+notebook",
    "leather+refillable+journal",
    "leather+refillable+notebook",
    "leather+journal+refillable",
    "leather+notebook+refillable",

    "leather+journal+men",
    "leather+journal+women",

    "leather+notebook+for+women",
    "leather+notebook+for+men",

    "traveler+journal+for+women",
    "traveler+notebook+for+women",
    "travelers+journal+for+women",
    "travelers+notebook+for+women",
    "traveler+journal+for+men",
    "traveler+notebook+for+men",
    "travelers+journal+for+men",
    "travelers+notebook+for+men",
    "refillable+journal+for+men",
    "refillable+notebook+for+men",
    "refillable+journal+for+women",
    "refillable+notebook+for+women",
]
my_asins = ["B08XY39PR7", "B08XXPM853", "B08XXR3WJH", "B08XXS74G8", "B08XXR8TGD"]
ASIN_TO_PRODUCT = {"B08XXPM853": "BLUE TP", "B08XXR3WJH": "BLUE TN", "B08XXS74G8": "PINK TP", "B08XXR8TGD": "PINK TN"}
POST_CODES = ["15213", "10005", "94404", "95123", "98109"]


def find_flight_by_link(driver=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    # applicable to windows os only
    options.add_argument('--disable-gpu')
    # overcome limited resource problems
    options.add_argument('--disable-dev-shm-usage')
    # open Browser in maximized mode
    options.add_argument('--disable-extensions')
    # options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080') # Set to be max when used in headless
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--shm-size=2g')
    options.add_experimental_option('useAutomationExtension', False)
    capabilities = options.to_capabilities()

    driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", capabilities)

    # Change the address to be in the US
    change_address(driver)

    result = []
    # Search the keyword in the list and find the rank.
    list_to_search = keyword_list
    if tmp_list:
        list_to_search = tmp_list

    for keyword in list_to_search:
        link = "https://www.amazon.com/s?k=%s" % keyword

        target_element = None
        reformat_keyword = " ".join(keyword.split("+"))
        # Find the rank if it is within first 4 pages
        for i in range(1, 5):
            final_link = "%s&page=%d" % (link, i)
            driver.get(final_link)
            sleep(0.15)

            for asin in my_asins:
                try:
                    target_element = driver.find_element_by_xpath("//div[@data-asin = '" + asin + "']")
                    rank_in_page = target_element.get_attribute("data-index")
                    is_sponsored = is_sponsored_result(target_element)
                    product = ASIN_TO_PRODUCT[asin]
                    result.append("Keyword: %s, page: %s, rank: %s, sponsored: %s, product: %s"
                                  % (reformat_keyword, i, rank_in_page, is_sponsored, product))
                    print(result[-1])
                except:
                    continue

        if not target_element:
            result.append("Keyword: %s, ========Not Found==========" % reformat_keyword)
            print(result[-1])


    #Written the result to the file
    driver.quit()
    with open("data/amazon_rank.csv", "w") as f:
        for i in range(len(result)):
            f.write(result[i] + '\n')
            # Adda an empty line for easy read.
            if i % 5 == 0:
                f.write('\n')


def is_sponsored_result(parent_element):
    try:
        parent_element.find_element_by_xpath(".//span[text()='Sponsored']")
        return True
    except:
        return False

def change_address(driver):
    try:    
        driver.get("https://www.amazon.com/")

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'nav-global-location-slot')))
        driver.find_element_by_xpath("//div[@id='nav-global-location-slot']").click()
        
        post_code = POST_CODES[random.randint(0, len(POST_CODES) - 1)]
        print("Chosse the post code: %s" % post_code)    
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'GLUXZipUpdateInput')))
        driver.find_element_by_xpath("//input[@id='GLUXZipUpdateInput']").send_keys(post_code)
        driver.find_element_by_xpath("//span[@id='GLUXZipUpdate']").click()
        sleep(0.1)
    except Exception as e:
        print(str(e))


find_flight_by_link()