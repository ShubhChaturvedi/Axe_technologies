from bs4 import BeautifulSoup
import requests
import mysql.connector
from datetime import datetime

class Scrapper:
    def __init__(self, link):
        try:
            self.link = link
            self.response = requests.get(link)
            self.html_content = self.response.text
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
            self.site_address_id = 0
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", str(e))

    def scrape_styledotty(self):
        try:
            product_name = self.soup.find('h1', class_='ty-mainbox-title').get_text(strip=True)
            product_price = self.soup.find('span', id='sec_discounted_price_428').get_text(strip=True)
            in_stock = self.soup.find('span', class_='ty-qty-in-stock').get_text(strip=True)
            self.site_address_id = 38
            data = {
                "Product Name": product_name,
                "Product Price": product_price or None,
                "Product link": self.link,
                "in_stock": in_stock or None
            }

            self.save_to_database(data, self.site_address_id)
            return data
        except AttributeError as e:
            print("An error occurred while scraping styledotty:", str(e))
            return None

    def scrape_kiwla(self):
        try:
            product_name = self.soup.find('h1', class_='productView-title').get_text(strip=True)
            product_price = self.soup.find('span', class_='price--main').get_text(strip=True).split("₹")[1]
            in_stock = self.soup.find('div', class_='productView-stockLabel').get_text(strip=True)
            self.site_address_id = 39
            data = {
                "Product Name": product_name,
                "Product Price": product_price or None,
                "Product link": self.link,
                "in_stock": in_stock or None
            }

            self.save_to_database(data, self.site_address_id)
            return data
        except AttributeError as e:
            print("An error occurred while scraping kiwla:", str(e))
            return None

    def scrape_ibhejo(self):
        try:
            product_name = self.soup.find('h1', class_='product-title').get_text(strip=True)
            product_price = self.soup.find('strong', class_='lbl-price').get_text(strip=True).split("₹")[2]
            in_stock = self.soup.find('span', class_='status-in-stock').get_text(strip=True)
            self.site_address_id = 40
            data = {
                "Product Name": product_name,
                "Product Price": product_price or None,
                "Product link": self.link,
                "in_stock": in_stock or None
            }

            self.save_to_database(data, self.site_address_id)
            return data
        except AttributeError as e:
            print("An error occurred while scraping ibhejo:", str(e))
            return None

    def scrape_shasvahealth(self):
        try:
            self.soup = BeautifulSoup(self.response.text, "lxml")
            name = self.soup.find(class_="product__title")
            self.site_address_id = 41
            data = {
                "Product Name": name.find("h1").get_text(strip=True),
                "Product link": "https://shasvahealth.in/" + name.find("a")["href"],
                "Product Price": self.soup.find(class_="price-item price-item--sale price-item--last").get_text(strip=True).replace(
                    "Rs.", "") or None,
                "in_stock": "In Stock"

            }

            self.save_to_database(data, self.site_address_id)
            return data
        except AttributeError as e:
            print("An error occurred while scraping shasvahealth:", str(e))
            return None

    def scrape_health_mall(self):
        try:
            self.soup = BeautifulSoup(self.response.text, "lxml")
            name = self.soup.find(class_="col-md-7 product-single__meta")
            self.site_address_id = 42
            data = {
                "Product Name": name.find("h1").get_text(strip=True),
                "Product Price": name.findAll("h1")[1].get_text(strip=True).encode("ascii", "ignore").decode().replace("Price() : ", "") or None,
                "Product link": self.link,
                "in_stock": "In Stock"
            }

            self.save_to_database(data, self.site_address_id)
            return data
        except AttributeError as e:
            print("An error occurred while scraping health_mall:", str(e))
            return None

    def save_to_database(self, data, site_address_id):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="shubh-compare",
                password="Shubh1710",
                database="compare_app"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                # Execute your SQL queries to save data to the database
                # For example:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                insert_query = "INSERT INTO app_product_url_mapper (url, site_address_id, created_at, updated_at, price, in_stock, product_id, product_name, key_matched, image_url) VALUES (%s , %d, %s, %s, %s, %d, %d, %s, %d, %s)"
                values = (data["Product link"], site_address_id,current_time , current_time, data['Product Price'],data['in_stock'] , data['Product Name'], 0, None)
                cursor.execute(insert_query, values)
                connection.commit()
                cursor.close()
                connection.close()
        except mysql.connector.Error as error:
            print("Error while connecting to MySQL:", error)



if __name__ == "__main__":
    test_link = "https://www.ibhejo.com/one-a-day-womens-prenatal-advanced-complete-multivitamin-with-brain-support-with-choline-folic-acid-omega-3-dha-iron-for-pre-during-and-post-pregnancy-6060-count-120-count-total-set-250389"
    scraper = Scrapper(test_link)
    print(scraper.scrape_ibhejo())




