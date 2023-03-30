from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Chrome(executable_path="/home/shubh/Downloads/chromedriver_linux64.exe")
driver.maximize_window()

driver.get("https://www.google.com")
time.sleep(1)
query = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
part_number = '90NR03U2'
query.send_keys(part_number)

time.sleep(1)
query.send_keys(Keys.ENTER)
js = """
        let links = []
        for(let i=0;i<document.getElementsByClassName('lyLwlc').length;i++){
            let divs = document.getElementsByClassName('lyLwlc')[i];
            let spans = divs.getElementsByTagName("span")[0];
            if(spans != undefined && spans.getElementsByTagName("em")[0] != undefined){
                if(spans.getElementsByTagName("em")[0].innerHTML === "90NR03U2" ){
                    let a = document.getElementsByClassName('yuRUbf')[i].getElementsByTagName("a")[0].getAttribute("href");
                    let link = [a];
                    links.push(link);
                }
            
            }
        }
        return links;
    """
links = driver.execute_script(js)
with open('output.csv', mode='a', newline='') as file:
    # Create a writer object
    writer = csv.writer(file)

    # Write the data to the CSV file
    for link in links:
        writer.writerow(link)


driver.close()
