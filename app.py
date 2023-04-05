from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv

def get_links(part_number, platforms, product_title):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="/home/shubh/Downloads/chromedriver_linux64.exe")
    driver.maximize_window()
    driver.get("https://www.google.com")
    query = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
    query.send_keys(part_number)
    query.send_keys(Keys.ENTER)
    js = f"""
            let links = []
            let search = "{part_number:s}".split("-");
            for(let i=0;i<document.getElementsByClassName('lyLwlc').length;i++){{
                let divs = document.getElementsByClassName('lyLwlc')[i];
                let spans = divs.getElementsByTagName("span")[0];
                if(spans != undefined && spans.getElementsByTagName("em")[0] != undefined && spans.getElementsByTagName("em")[1] != undefined){{
                    if(spans.getElementsByTagName("em")[0].innerHTML === search[0] && spans.getElementsByTagName("em")[1].innerHTML === search[1]){{
                        let a = document.getElementsByClassName('yuRUbf')[i].getElementsByTagName("a")[0].getAttribute("href");
                        let link = [a];
                        links.push(link);
                    }}
                
                }}
                else if(spans != undefined && spans.getElementsByTagName("em")[0] != undefined){{
                    if(spans.getElementsByTagName("em")[0].innerHTML === search[0]){{
                        let a = document.getElementsByClassName('yuRUbf')[i].getElementsByTagName("a")[0].getAttribute("href");
                        let link = [a];
                        links.push(link);
                    }}
                
                }}
            }}
            return links;
        """
    links = driver.execute_script(js)
    new_links = []
    for link in links:
        for platform in platforms:
            if platform in link[0]:
                new_links.append(link)
                break


    with open('output.csv', mode='a', newline='') as file:
        # Create a writer object
        writer = csv.writer(file)

        # Write the data to the CSV file
        for link in new_links:
            writer.writerow([product_title ,link[0]])


    driver.close()

if __name__ == "__main__":
    part_number = 'D560871WIN9B'
    platforms = ['amazon', 'flipkart', 'reliancedigital', 'croma', 'vijaysales', 'samsung', 'hp', 'redmi', 'mi',
                 'nykaa', 'myntra']
    get_links(part_number, platforms, "laptop")