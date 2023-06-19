import requests
from bs4 import BeautifulSoup

link = "https://www.myg.in/tv/oneplus/oneplus-y-series-108-cm-43-inch-full-hd-led-smart-android-tv-43fa0a00/"
response = requests.get(link)

soup = BeautifulSoup(response.text, 'html.parser')
dict = {
    "Product Name": soup.find('h1', class_="ty-product-block-title").find("bdi").get_text(strip=True),
    "Product Price": soup.find('span', id="sec_discounted_price_1707").get_text(strip=True),
    "Product link": link,
    "in_stock": soup.find("span", class_="ty-qty-in-stock").get_text(strip=True)
}
print(dict)