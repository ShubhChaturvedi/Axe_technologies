import requests
from bs4 import BeautifulSoup


def findPrice(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    product_price = soup.find("div", class_="order-list-section__item-spacer")
    # product_price = product_price.find("strong")
    product_name = soup.find("span", class_="header")
    print(product_name)
    result = f"""Product Name: {product_name.text.strip()}
    Product Price: {product_price},
    Product Avaialblity : in stock"""
    print(result)


if __name__ == '__main__':
    url = "https://www.mi.com/in/product/redmi-10a/?skupanel=1&gid=4221600006"
    findPrice(url)