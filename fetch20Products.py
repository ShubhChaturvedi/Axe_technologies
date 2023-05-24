from bs4 import BeautifulSoup
import requests
import csv

response = requests.get("https://www.flipkart.com/search?q=latest+mobile&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_9_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_9_na_na_na&as-pos=1&as-type=RECENT&suggestionId=latest+mobile%7CMobiles&requestId=67475549-e096-427d-891e-ee4c5bd1796f&as-backfill=on")
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
data = []
try:
    for i in range(20):
            data.append({
                    "id": i,

                    "product_title": soup.find_all('div', class_='_4rR01T')[i].text,
                    "product_website_sales_rank": 6,
                    "link": "https://www.flipkart.com" + soup.find_all('a', class_='_1fQZEK')[i]['href'],
                    "brand_name": soup.find_all('div', class_='_4rR01T')[i].text.split()[0],
                    "maufacturer_name": soup.find_all('div', class_='_4rR01T')[i].text.split()[0],
                    "product_featurs" : [(soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[0].text, (soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[1].text, (soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[2].text, (soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[3].text, (soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[4].text],
                    "product_part_number": soup.find_all('div', class_='_4rR01T')[i].text.split()[0],
                    "product_model_number": soup.find_all('div', class_='_4rR01T')[i].text.split()[0],
                    "product_warranty": "",
                    "release_date": "",
                    "product_price": soup.find_all('div', class_='_30jeq3 _1_WHN1')[i].text,
                    "product_display_price": soup.find_all('div', class_='_30jeq3 _1_WHN1')[i].text,
                    "product_currency": "INR",
                    "product_price_per_unit": soup.find_all('div', class_='_30jeq3 _1_WHN1')[i].text,
                    "product_savings_price": "",
                    "product_savings_display_price":"",
                    "product_savings_currency":"",
                    "product_savings_price_per_unit" :"",
                    "product_savings_percentage":"",
                    "max_order_quantity":"",
                    "min_order_quantity":"",
                    "is_active": 1,
            })
except:
    pass
csv_file = 'mobile_data.csv'

# Define the field names
field_names = ['id', 'product_title', 'product_website_sales_rank', 'link', 'brand_name', 'maufacturer_name', 'product_featurs', 'product_part_number', 'product_model_number', 'product_warranty', 'release_date', 'product_price', 'product_display_price', 'product_currency', 'product_price_per_unit', 'product_savings_price', 'product_savings_display_price', 'product_savings_currency', 'product_savings_price_per_unit', 'product_savings_percentage', 'max_order_quantity', 'min_order_quantity', 'is_active']

# Open the CSV file in write mode
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)

    # Write the header row
    writer.writeheader()
    for item in data:
            writer.writerow(item)
