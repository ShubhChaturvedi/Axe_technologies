from bs4 import BeautifulSoup
import requests

link = "https://kiwla.com/products/Unicorn-Snot-Holographic-Body-Glitter-Gel-Vegan-Cruelty-Free-Perfect-for-Festival-Rave-Halloween-Costume-Silver-17oz"
response = requests.get(link)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
dict = {
    "Product Name": soup.find('h1', class_='productView-title').get_text(strip=True),
    "Product Price": soup.find('span', class_='price--main').get_text(strip=True).split("₹")[1],
    "Product link" : link,
    "in_stock" : soup.find('div', class_='productView-stockLabel').get_text(strip=True)
}

print(dict)