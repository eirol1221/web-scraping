import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

SHEETY_URL = os.environ["SHEETY_URL"]

response = requests.get(SHEETY_URL)
sheet_data = response.json()

options = Options()
options.add_argument("start-maximized")

s = Service(r"Your chromedriver path")

driver = webdriver.Chrome(service=s, options=options)
sub_driver = webdriver.Chrome(service=s, options=options)
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, TimeoutException)
wait = WebDriverWait(driver=driver, timeout=5, ignored_exceptions=ignored_exceptions)

pages_path = "https://www.acecqa.gov.au/resources/national-registers/services?s=&f%5B0%5D=service_state%3ANSW&page="

# ------------ GET SUB URLS ------------ #
for page_num in range(1, 3):
    driver.get(f"{pages_path}{page_num}")
    results = driver.find_elements(By.CSS_SELECTOR, "div.search__content a")

    sub_urls = [item.get_attribute("href") for item in results]

    for index in range(len(sub_urls)):
        sub_driver.get(sub_urls[index])

        try:
            centre_name = sub_driver.find_element(By.CSS_SELECTOR, "div.content h1").text
        except:
            centre_name = "No data"
        try:
            address = (sub_driver.find_element(By.CSS_SELECTOR, "div.address span.address-line1").text +
                       sub_driver.find_element(By.CSS_SELECTOR, "div.address span.address-postal-code").text)
        except:
            address = "No data"
        try:
            phone = sub_driver.find_element(By.CSS_SELECTOR, "div.field--name-field-service-phone-number div.field--item").text
        except:
            phone = "No data"
        try:
            email = sub_driver.find_element(By.CSS_SELECTOR, "div.field--name-field-service-email a").text
        except:
            email = "No data"
        try:
            approved_places = sub_driver.find_element(By.CSS_SELECTOR, "div.field--name-field-max-place-numbers div.field--item").text
        except:
            approved_places = "No data"
        try:
            provider_name = sub_driver.find_element(By.CSS_SELECTOR, "div.field--name-field-provider-reference a").text
        except:
            provider_name = "No data"
        try:
            service_approval_granted_date = sub_driver.find_element(By.CSS_SELECTOR, "div.field--name-field-approval-date time").text
        except:
            service_approval_granted_date = "No data"

        body = {
            "detail": {
                "centreName": centre_name,
                "address": address,
                "phone": phone,
                "email": email,
                "approvedPlaces": approved_places,
                "providerName": provider_name,
                "serviceApprovalGrantedDate": service_approval_granted_date
            }
        }
        sheety_response = requests.post(SHEETY_URL, json=body)

driver.quit()