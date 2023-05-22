from bs4 import BeautifulSoup
import requests
import csv

response = requests.get("https://www.flipkart.com/search?q=latest+mobile&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_9_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_9_na_na_na&as-pos=1&as-type=RECENT&suggestionId=latest+mobile%7CMobiles&requestId=67475549-e096-427d-891e-ee4c5bd1796f&as-backfill=on")
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
data = []
for i in range(20):
        data.append({
                "title": soup.find_all('div', class_='_4rR01T')[i].text,
                "storage": (soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[0].text,
                "display": (soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[1].text,
                "camera": (soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[2].text,
                "battery": (soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[3].text,
                "processor": (soup.find_all('ul', class_='_1xgFaf')[i]).find_all('li')[4].text,
                "price": soup.find_all('div', class_='_30jeq3 _1_WHN1')[i].text,
                "link": "https://www.flipkart.com" + soup.find_all('a', class_='_1fQZEK')[i]['href']
        })
csv_file = 'mobile_data.csv'

# Define the field names
field_names = ['title', 'storage', 'display', 'camera', 'battery', 'processor', 'price', 'link']

# Open the CSV file in write mode
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)

    # Write the header row
    writer.writeheader()
    for item in data:
            writer.writerow(item)
