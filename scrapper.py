from bs4 import BeautifulSoup
import requests

class Scrapper:
    def __init__(self, link):
        try:
            self.link = link
            self.response = requests.get(link)
            self.html_content = self.response.text
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", str(e))

    def scrape_styledotty(self):
        try:
            product_name = self.soup.find('h1', class_='ty-mainbox-title').get_text(strip=True)
            product_price = self.soup.find('span', id='sec_discounted_price_428').get_text(strip=True)
            in_stock = self.soup.find('span', class_='ty-qty-in-stock').get_text(strip=True)

            data = {
                "Product Name": product_name,
                "Product Price": product_price,
                "Product link": self.link,
                "in_stock": in_stock
            }

            return data
        except AttributeError as e:
            print("An error occurred while scraping styledotty:", str(e))
            return None

    def scrape_kiwla(self):
        try:
            product_name = self.soup.find('h1', class_='productView-title').get_text(strip=True)
            product_price = self.soup.find('span', class_='price--main').get_text(strip=True).split("₹")[1]
            in_stock = self.soup.find('div', class_='productView-stockLabel').get_text(strip=True)

            data = {
                "Product Name": product_name,
                "Product Price": product_price,
                "Product link": self.link,
                "in_stock": in_stock
            }

            return data
        except AttributeError as e:
            print("An error occurred while scraping kiwla:", str(e))
            return None

    def scrape_ibhejo(self):
        try:
            product_name = self.soup.find('h1', class_='product-title').get_text(strip=True)
            product_price = self.soup.find('strong', class_='lbl-price').get_text(strip=True).split("₹")[2]
            in_stock = self.soup.find('span', class_='status-in-stock').get_text(strip=True)

            data = {
                "Product Name": product_name,
                "Product Price": product_price,
                "Product link": self.link,
                "in_stock": in_stock
            }

            return data
        except AttributeError as e:
            print("An error occurred while scraping ibhejo:", str(e))
            return None

    def scrape_shasvahealth(self):
        try:
            self.soup = BeautifulSoup(self.response.text, "lxml")
            name = self.soup.find(class_="product__title")
            data = {
                "product_name": name.find("h1").get_text(strip=True),
                "product_url": "https://shasvahealth.in/" + name.find("a")["href"],
                "price": self.soup.find(class_="price-item price-item--sale price-item--last").get_text(strip=True).replace(
                    "Rs.", "")

            }

            return data
        except AttributeError as e:
            print("An error occurred while scraping shasvahealth:", str(e))
            return None

    def scrape_health_mall(self):
        try:
            self.soup = BeautifulSoup(self.response.text, "lxml")
            name = self.soup.find(class_="col-md-7 product-single__meta")

            data = {
                "product_name": name.find("h1").get_text(strip=True),
                "price": name.findAll("h1")[1].get_text(strip=True).encode("ascii", "ignore").decode().replace("Price() : ", ""),
                "product url": self.link
            }

            return data
        except AttributeError as e:
            print("An error occurred while scraping health_mall:", str(e))
            return None




