from bs4 import BeautifulSoup
import requests

link = "https://www.ibhejo.com/kirkland-signature-men-50-multivitamin-365-tablets-288811"
response = requests.get(link)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
dict = {
    "Product Name": soup.find('h1', class_='product-title').get_text(strip=True),
    "Product Price": soup.find('strong', class_='lbl-price').get_text(strip=True),
    "Product link" : link
}

print(dict)