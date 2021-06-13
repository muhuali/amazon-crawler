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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


TARGET_ASINS = set(["B08XY39PR7", "B08XXPM853", "B08XXR3WJH", "B08XXS74G8", "B08XXR8TGD"])
NOISE_ASINS= set(["B07W417P6P", "B0892BMS16", "B08CD56C8P","B07SKX5XB6", "B0892BHQLF"])
# list_to_search = ["blue+leather+refillable+journal", "leather+journal", "travel+journal"]
list_to_search = ["travelers+notebook+for+women","leather+journal+men","traveler+notebook+for+men", "leather+journal", "travel+journal"]
POST_CODES = ["15213", "10005", "94404", "95123", "98109", "89048"]
ASIN_TO_PRODUCT_DICT = {
    "B08XXPM853":"BLUE TP" ,"B08XXR3WJH": "BLUE TN", "B08XXS74G8": "PINK TP", "B08XXR8TGD":"PINK TN"}

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
        print("Error in changing Address" + str(e))

def is_sponsored_result(parent_element):
    try:
        parent_element.find_element_by_xpath(".//span[text()='Sponsored']")
        return True
    except:
        return False


def find_element_by_asin(driver, asin, key_word, page):
    try:
        # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@data-index = '20'")))
        target_element = driver.find_element_by_xpath("//div[@data-asin = '" + asin + "']")
        rank_in_page = target_element.get_attribute("data-index")
        is_sponsored = is_sponsored_result(target_element)
        product = ASIN_TO_PRODUCT_DICT.get(asin, "NOISE")

        if rank_in_page:
            print("Asin:%s, Keyword: %s, page: %s, rank: %s, sponsored: %s, product: %s" % 
                    (asin, key_word, page, rank_in_page, is_sponsored, product))

        # Check if this is a sponsored result, don't return sponsored result back, otherwise will incure CPC charge
        # If no rank, returns None as well.
        if is_sponsored and asin in TARGET_ASINS:
            return None
    
        if not rank_in_page:
            return None
        return target_element
    except Exception as e:
        return None


def add_to_cart(driver, element, asin, search_page_link):
    if not element:
        return
    try:
        # Firstly move your cursor to the element
        action = webdriver.ActionChains(driver)
        action.move_to_element(element).perform()

        # Click the product and lead to a new page
        element.click()

        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "add-to-cart-button"))).click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "nav-hamburger-menu")))
        print("Add Asin: %s to cart" % (asin))

        # Return the previous search page
        driver.get(search_page_link)
        sleep(0.15)
        return True
    except Exception as e:
        print("============Add to cart error===============" + str(e))
        return False

def initialize_driver():
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
    # options.add_argument('--window-size=1920,1080') # Set to be max when used in headless
    # options.add_argument('--remote-debugging-port=9222')
    # options.add_argument('--shm-size=2g')
    options.add_experimental_option('useAutomationExtension', False)
    # Change user agent
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")     
    capabilities = options.to_capabilities()

    driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", capabilities)
    return driver

def main(driver=None):
    # Change the address to be in the US
    change_address(driver)

    # Print cookies and sessions.
    # print("=============driver.session_id: " + driver.session_id)
    # print("=============driver.cookes: " + "\n".join([str(i) for i in driver.get_cookies()]))
    print("=============driver.user_agent: " + str(driver.execute_script("return navigator.userAgent;")))
    result = []
    target_element = None
    found_noise_elements = set()
    # Search the keyword in the list and find the rank.
    for keyword in list_to_search:
        link = "https://www.amazon.com/s?k=%s" % keyword

        reformat_keyword = " ".join(keyword.split("+"))
        # Find the rank if it is within first 5 pages
        for i in range(1, 6):
            final_link = "%s&page=%d" % (link, i)
            driver.get(final_link)

            # If the target already found on the previous search result, skip
            if not target_element:
                for asin in TARGET_ASINS:
                    tmp_target = find_element_by_asin(driver, asin, reformat_keyword, i)
                    is_added = add_to_cart(driver, tmp_target, asin, final_link)
                    # Only assin when it is not None
                    # if tmp_target and is_added:
                    #     target_element = tmp_target

            for asin in NOISE_ASINS:
                if asin not in found_noise_elements:
                    noise_element = find_element_by_asin(driver, asin, reformat_keyword, i)
                    add_to_cart(driver, noise_element, asin, final_link)
                    if noise_element:
                        found_noise_elements.add(asin)


            # Aim to find one target and all NOISE, unless we searched all the pages.
            if target_element and found_noise_elements == NOISE_ASINS:
                result.append("Complete add to cart")
                driver.quit()
                return

    #Written the result to the file
    driver.quit()

for i in range(0, 3):
    driver = None
    try:
        driver = initialize_driver()
        main(driver)
    except Exception as e:
        print("===========Main Exception=========="+str(e))
        driver.quit()
        continue