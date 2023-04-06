import app
import csv
if __name__ == '__main__':
    with open('app_product_data.csv', mode='r') as file:
        reader = csv.reader(file)
        platforms = ['amazon', 'flipkart', 'reliancedigital', 'croma', 'vijaysales', 'samsung', 'hp', 'redmi', 'mi',
                     'nykaa', 'myntra']
        for row in reader:
            product_id = row[0]
            part_number = row[2]
            product_title = row[1]
            app.get_links(part_number, platforms, product_title, product_id)