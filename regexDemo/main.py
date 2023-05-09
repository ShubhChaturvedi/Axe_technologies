# import csv
# import requests
# from bs4 import BeautifulSoup
# import time
# # Open the CSV file and create a reader object
#
# def getPrice(url):
#     try:
#         time.sleep(5)
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#         response = requests.get(url, headers=headers)
#
#         # response = requests.get(url)
#         html_content = response.text
#         soup = BeautifulSoup(html_content, 'html.parser')
#         print(soup.prettify())
#         price_element = soup.find('div', class_='price-inner-text')
#         price_value = price_element.p.text.strip('₹')
#         print(price_value)
#         # with open('app_product_master.csv', mode='r', newline='') as csvfile:
#         #     reader = csv.reader(csvfile)
#         #     rows = list(reader)
#         # for i in range(len(rows)):
#         #     rows[i][3] = price_value
#         # with open('app_product_master.csv', mode='w', newline='') as csvfile:
#         #     writer = csv.writer(csvfile)
#         #     writer.writerows(rows)
#     except:
#         print("Error in fetching price")
# getPrice("https://in.iherb.com/pr/life-extension-two-per-day-multivitamin-120-capsules/86453")
# # with open('app_product_master.csv', newline='') as csvfile:
# #     reader = csv.reader(csvfile)
# #
# #     column_index = 2
# #     for row in reader:
# #         url = row[column_index]
# #         getPrice(url)
from bs4 import BeautifulSoup
import requests
import socks
import socket
from stem import Signal
from stem.control import Controller
import time
import random

def get_tor_session():
    session = requests.session()
    # Tor uses the SOCKS protocol to connect to the internet
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

def renew_tor_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def getRandomUserAgent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    ]
    return random.choice(user_agents)

def getPrice(url):
    try:
        time.sleep(5)
        session = get_tor_session()
        headers = {
            'User-Agent': getRandomUserAgent()}
        response = session.get(url, headers=headers)

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        print(soup.prettify())
        price_element = soup.find('div', class_='price-inner-text')
        price_value = price_element.p.text.strip('₹')
        print(price_value)
    except:
        print("Error in fetching price")
    finally:
        session.close()

if __name__ == '__main__':
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    getPrice("https://in.iherb.com/pr/life-extension-two")

