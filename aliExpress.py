from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Chrome(executable_path="/home/shubh/Downloads/chromedriver_linux64.exe")
driver.maximize_window()

driver.get("https://www.aliexpress.com")
time.sleep(1)
query = driver.find_element(by=By.XPATH, value='//*[@id="search-key"]')
search = 'smartphone'
query.send_keys(search)
time.sleep(1)
query.send_keys(Keys.ENTER)
js = """
    let data = {
        "source_name": "aliexpress"
    };
    let content = document.getElementsByClassName('manhattan--container--1lP57Ag cards--gallery--2o6yJVt');
    for(let i=0;i<content.length;i++){
        content[i].click();
        let sample = {
            "product_title": "",
            "product_detail_page_url": content[i].getAttribute("href"),
            "product_brand": "",
            "product_features": "",
            "product_part_number": "",
            "product_model_number": "",
            "product_price": "",
            "product_display_price": "",
            "product_currency": "",
            "category_id": 2,
            "product_source_id": "",
            "product_specifications": "",
            "is_active": "",
            "product_image_url": "",
            "product_image_type": "",
            "product_image_type_size": "",
            "product_image_height": "",
            "product_image_width": "",
            
            };
            data[i] = sample;
        };
        return data;
"""

data = driver.execute_script(js)
print(data)
time.sleep(20)

driver.close()