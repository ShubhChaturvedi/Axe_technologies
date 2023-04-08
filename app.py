from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time

def get_links(part_number, platforms, product_title, product_id):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="/home/shubh/Downloads/chromedriver_linux64.exe")
    driver.maximize_window()
    driver.get("https://www.google.com")
    try:
        query = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
        query.send_keys(part_number)
        query.send_keys(Keys.ENTER)
        js = f"""
                let links = []
                
                let search = "{part_number:s}".split("-");
                if(search.length === 1){{
                    search = "{part_number:s}".split("/");
                }}
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
                if platform in link[0].split("."):
                    new_links.append(link)
                    break


        with open('output.csv', mode='a', newline='') as file:
            # Create a writer object
            writer = csv.writer(file)
            for item in new_links:
                if len(item[0].split('#')) != 1:
                    item[0] = item[0].split('#')[0]
            # Write the data to the CSV file
            writer.writerow([product_id ,product_title ,new_links])

    except Exception as e:
        print(e)
        driver.close()
        get_links(part_number, platforms, product_title, product_id)
    driver.close()

if __name__ == "__main__":
    part_number = 'WA65A4002VS/TL'
    platforms = ['amazon', 'flipkart', 'reliancedigital', 'croma', 'vijaysales', 'samsung', 'hp', 'redmi', 'mi',
                 'nykaa', 'myntra']
    get_links(part_number, platforms, "SAMSUNG 6.5 kg Diamond Drum feature Fully Automatic Top Load Silver(WA65A4002VS/TL)","731665")