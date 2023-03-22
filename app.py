from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(executable_path="/home/shubh/Downloads/chromedriver_linux64.exe")
driver.maximize_window()

driver.get("https://www.google.com")
time.sleep(1)
query = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
part_number = '90NR03U2'
query.send_keys(part_number)

time.sleep(1)
query.send_keys(Keys.ENTER)
query2 = driver.find_element(by=By.XPATH, value='//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[2]/div/span/em').text
print(query2)

js = """
        for(let i=0;i<document.getElementsByClassName('lyLwlc').length;i++){
            let divs = document.getElementsByClassName('lyLwlc')[i]
            let spans = divs.getElementsByTagName("span")[0]
            if(spans != undefined){
                if(spans.getElementsByTagName("em")[0].innerHTML === "90NR03U2" ){
                    console.log("sahi h tu")
                }
            }
        }
    """
driver.execute_script(js)
# if(query2 == ):
time.sleep(100)

driver.close()