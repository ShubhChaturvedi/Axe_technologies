import requests
from bs4 import BeautifulSoup

url = "https://www.samsung.com/in/smartphones/galaxy-a/"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

# Find all the smartphone product containers
product_containers = soup.find_all("div", class_="pd03-product-card__product-content")

# Loop through each container and extract the necessary information
for product in product_containers:
    product_name = product.find("p",class_="pd03-product-card__product-name-text").text.strip()
    product_price = product.find("p", class_="pd03-product-card__price-main ").text.strip()
    product_availablity = product.find("span", class_="pd03-product-card__stock-icons").text.strip()

    # Print the extracted information
    result = f""" Product Name: {product_name},
                Product Price: {product_price},
                Product Avaialblity : {product_availablity}"""
    print(result)
