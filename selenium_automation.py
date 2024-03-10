from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

application_url = "https://friends1.e6xlabs.cloud/login"
email = "task@e6x.io"
password = "Abcd@123"
cluster_name_input = "TestClusterCreation"
chrome_webdriver_path = os.getenv("CHROME_WEB_DRIVER")

def setup_driver():
    #Initializes the webdriver
    service = Service(chrome_webdriver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(application_url)
    return driver

def login(driver, email, password):
    # Logs into the application using the provided credentials
    
    time.sleep(10)
    
    email_input = driver.find_element(By.CLASS_NAME, 'form-control')
    email_input.send_keys(email)
    password_input = driver.find_element(By.CLASS_NAME, 'password.form-control')
    password_input.send_keys(password)
    time.sleep(3)
    password_input.send_keys(Keys.ENTER)
    time.sleep(10)

def list_options(driver):
    # Lists down options available in the left navigation
    nav_bar = driver.find_element(By.CLASS_NAME, 'left-nav')
    nav_items = nav_bar.find_elements(By.CLASS_NAME, 'list')
    for nav_item in nav_items:
        item_text = nav_item.find_element(By.TAG_NAME, 'span').get_attribute('textContent').strip()
        print(item_text)

def record_list_details(driver, option):
    # Navigates to a specified item in the navigation and lists details
    try: 
        nav_bar = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'left-nav')))
        nav_items = nav_bar.find_elements(By.CLASS_NAME, 'list')
        for nav_item in nav_items:
            item_text = nav_item.find_element(By.TAG_NAME, 'span').get_attribute('textContent').strip()
            if item_text == option:
                option_link = nav_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if option_link:
                    driver.get(option_link)
                    time.sleep(10) 
                    rows = driver.find_elements(By.XPATH, "//tbody[@class='p-datatable-tbody']/tr[@role='row']")
                    print("Total Count of", (option), len(rows))
                    for row in rows:
                        name_element = row.find_element(By.XPATH, ".//td[1]/a[@class='hyperlink-cls']")                   
                        cluster_name = name_element.text.strip()
                        
                        status_element = row.find_element(By.TAG_NAME, 'span').get_attribute('textContent').strip()

                        if item_text == "Clusters":
                            created_by = row.find_element(By.XPATH, ".//td[5]").text.strip()
                        if item_text == "Catalogs":
                            created_by = row.find_element(By.XPATH, ".//td[4]").text.strip()

                        print(f"Name: {cluster_name}, Created By: {created_by}, Status: {status_element}")
    except Exception as err:
        pass

def create_new_cluster(driver, cluster_name_input):
    try:
        create_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Create"]'))
        )
        create_button.click()

        cluster_name = driver.find_element(By.XPATH, '//input[@placeholder="Enter cluster name"]')
        cluster_name.clear()
        cluster_name.send_keys(cluster_name_input)
        
        cache_checkbox = driver.find_element(By.XPATH, '//input[@id="cacheEnabled"]')
        cache_checkbox.click()
        
        advance_settings_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='semi-bold' and text()='Advanced Settings']"))
        )
        advance_settings_button.click()

        time.sleep(3)
        auto_suspension_checkbox = driver.find_element(By.XPATH, '//input[@id="enable_auto_suspension"]')

        sustime_input = driver.find_element(By.XPATH, '//input[@id="susTime"]')
        sustime_input.clear()
        sustime_input.send_keys("10")

        query_timeout_checkbox = driver.find_element(By.XPATH, '//input[@id="defaultQuery"]')
        query_timeout_checkbox.click()
        
        catalog_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".react-select__dropdown-indicator"))
        )
        catalog_dropdown.click()
        time.sleep(1)  

        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN)
        time.sleep(1)  
        actions.send_keys(Keys.DOWN)  
        time.sleep(1)  
        actions.send_keys(Keys.ENTER) 
        time.sleep(2)

        actions.perform() 
        dropdown_indicator = driver.find_element(By.CSS_SELECTOR, ".react-select__dropdown-indicator")
        actions.move_to_element(dropdown_indicator).click().perform()

        time.sleep(3)

        create_cluster_button = driver.find_element(By.XPATH, "//span/button[contains(@class, 'ml-3 btn btn-primary')][text()='Create']")

        create_cluster_button.click()
        time.sleep(30)

    except Exception as err:
        print("The error is", err)

def delete_cluster(driver, cluster_name_input):
    actions = ActionChains(driver)
    try:
        rows = driver.find_elements(By.XPATH, "//tbody[@class='p-datatable-tbody']/tr[@role='row']")
        
        for row in rows:
            name_element = row.find_element(By.XPATH, ".//td[1]")
            cluster_name = name_element.text.strip()
            time.sleep(150)
            
            if cluster_name == cluster_name_input:
                time.sleep(10)
                status = row.find_element(By.TAG_NAME, 'span').get_attribute('textContent').strip()
                if status.lower() == "active":
                    dropdown_button = row.find_element(By.ID, "dropdown-autoclose-true")
                    dropdown_button.click()
                    delete_option = driver.find_element(By.XPATH, "//a[@data-rr-ui-dropdown-item]//span[text()='Delete']")
                    delete_option.click()
                    password_input = driver.find_element(By.ID, "formBasicPassword")
                    password_input.clear()
                    password_input.send_keys("Delete")

                    actions.send_keys(Keys.ENTER).perform()
    except Exception as err:
        print("The error is", err)

def query_history_records(driver):
    try:
        nav_bar = driver.find_element(By.CLASS_NAME, 'left-nav')
        nav_bar.click()

        query_history_link = driver.find_element(By.XPATH, "//span[contains(text(), 'Query history')]")
        query_history_link.click()

        daterangepicker_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".e6daterangepicker-input")))
        daterangepicker_input.click()

        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".e6daterangepicker-filter")))

        last_7_days_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'menu-item') and contains(., 'Last 7 days')]")))
        last_7_days_option.click()

        time.sleep(8)

    except Exception as err:
        print(err)


def main():
    driver = setup_driver()

    # task 1: log in 
    login(driver, email, password)

    hyperlink = driver.find_element(By.XPATH, "//a[@class='hyperlink-cls' and text()='plt-infra']")
    hyperlink.click()
    time.sleep(5)

    # task 2: list nav-options
    list_options(driver)

    # task 3: listing details for records
    record_list_details(driver, "Catalogs")
    record_list_details(driver, "Clusters")

    # task 4: creating new cluster
    create_new_cluster(driver, cluster_name_input)
    # task 5: deleting the new cluster
    delete_cluster(driver, cluster_name_input)
    # task 6: query history records
    query_history_records(driver)
    
    driver.quit()

if __name__ == "__main__":
    main()


