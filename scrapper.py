from bs4 import BeautifulSoup
import requests

class Scrapper:
    def __init__(self, link):
        self.link = link
        self.response = requests.get(link)
        self.html_content = self.response.text
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def scrape_styledotty(self):
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

    def scrape_kiwla(self):
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

    def scrape_ibhejo(self):
        product_name = self.soup.find('h1', class_='product-title').get_text(strip=True)
        product_price = self.soup.find('strong', class_='lbl-price').get_text(strip=True).split("₹")[2]
        in_stock = "in stock"

        data = {
            "Product Name": product_name,
            "Product Price": product_price,
            "Product link": self.link,
            "in_stock": in_stock
        }

        return data
