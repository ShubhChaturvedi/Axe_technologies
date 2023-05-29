from bs4 import BeautifulSoup
import requests
import csv
import re

response = requests.get("https://www.ibhejo.com/vitamin/multi-vitamins")
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')

lst = []
for i in range(5):
    h3_tag = soup.find_all('h3', class_='product-title')[i]
    anchor_tag = h3_tag.find('a')
    # price = soup.find_all('span', class_='price')[i]
    link = anchor_tag['href']
    product_page = requests.get(link)
    html_content = product_page.text
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.find_all('h1', class_='product-title')
    price = soup.find('strong', class_='lbl-price')
    lst.append({
        "link": link,
        "text": title[0].get_text(strip=True),
        "price": price.get_text(strip=True)

    })

with open('ibhejo.csv', mode='w', newline='') as file:
    # Create a writer object
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Product Name", "Product Price", "Product Link"])
    # Write the data to the CSV file
    for item in lst:
        writer.writerow([item["text"], item["price"], item["link"]])