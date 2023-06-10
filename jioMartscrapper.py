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
link = "https://www.jiomart.com/p/premiumfruits/pear-packham-premium-imported-4-pc-approx-740-g-860-g/591057892"
driver.get(link)

script = f"""
            let title = document.getElementsByClassName("product-header-name")[0].innerText;
            let price = document.getElementsByClassName("jm-heading-xs")[0].innerText;
            return [title, price]
        """
data = driver.execute_script(script)
dict = {
    "Product Name": data[0],
    "Product Price": data[1],
    "Product link": link,
    "in_stock": "in_stock"
}
print(dict)
