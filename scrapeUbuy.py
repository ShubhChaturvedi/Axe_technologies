from selenium import webdriver

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
link = "https://www.ubuy.co.in/product/7H7EPL0MW-apple-watch-series-8-gps-45mm-smart-watch-w-midnight-aluminum-case-with-midnight-sport-band-m-l-fitness-tracker-blood-oxygen-ecg-apps"
driver.get(link)

script = f"""
            let title = document.getElementsByClassName("title")[0].innerText;
            let price = document.getElementsByClassName("product-price")[0].innerText;
            let stock =  document.getElementById("availability-status").innerText
            return [title, price ,stock]
        """
data = driver.execute_script(script)
dict = {
    "Product Name": data[0],
    "Product Price": data[1],
    "Product link": link,
    "in_stock": data[2],
}
print(dict)
