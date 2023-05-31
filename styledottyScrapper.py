from bs4 import BeautifulSoup
import requests

link = "https://www.styledotty.com/skincare/cerave/cerave-cream-16-oz-tub/"
response = requests.get(link)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
dict = {
    "Product Name": soup.find('h1', class_='ty-mainbox-title').get_text(strip=True),
    "Product Price": soup.find('span', id ='sec_discounted_price_428').get_text(strip=True),
    "Product link" : link,
    "in_stock" : soup.find('span', class_='ty-qty-in-stock').get_text(strip=True)
}

print(dict)