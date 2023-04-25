import requests
from bs4 import BeautifulSoup
def findPrice():
    url = "https://www.samsung.com/in/smartphones/galaxy-m/galaxy-m33-5g-blue-128gb-storage-8gb-ram-sm-m336bzbrins/buy/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    product_price = soup.find("span", class_="pd-option-selector__sub-text")
    product_name = soup.find("h2", class_="pd-info__title")
    result = f"""Product Name: {product_name.text.strip()},
    Product Price: {(product_price.text.strip().split())[-1]},
    Product Avaialblity : in stock"""
    print(result)

if __name__ == '__main__':
    findPrice()