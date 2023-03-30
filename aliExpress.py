from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Chrome(executable_path="/home/shubh/Downloads/chromedriver_linux64.exe")
driver.maximize_window()

driver.get("https://www.aliexpress.com")
time.sleep(1)
# query = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
# search = "aliexpress"
# query.send_keys(search)
#
# time.sleep(1)
# query.send_keys(Keys.ENTER)
# query2 = driver.find_element(by=By.XPATH, value='//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/a').click()
# time.sleep(10)
#
# js = """
#         let data = {};
#
#     """
# links = driver.execute_script(js)



driver.close()