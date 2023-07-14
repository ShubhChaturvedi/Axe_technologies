from pymongo import MongoClient
import datetime

class UserAnalytics:
    """
    This class is used to get the user analytics from the database.
    """
    def __init__(self, connection_string, db_name, collection_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def close_connection(self):
        """
        This method is used to close the connection.
        """
        self.client.close()
    def total_users_visited_today(self):
        """
        This method is used to get the total users visited today.
        :return: dict
        """
        try:
            todays_date = datetime.datetime.now().date()
            find_user_details = self.collection.find({str(todays_date): {"$exists": True}})
            count = self.collection.count_documents({str(todays_date): {"$exists": True}})
            result = {
                "date": str(todays_date),
                "active_users": count,
            }
            for user, data in enumerate(find_user_details):
                result[user] = data
            return result
        except Exception as e:
            print(e)
        return 0
    def total_users_visited_in_a_day(self, date):
        """
        This method is used to get the total users visited in a day.
        :param date:
        :return: dict
        """
        try:
            find_user_details = self.collection.find({date: {"$exists": True}})
            count = self.collection.count_documents({date: {"$exists": True}})
            result = {
                "date": date,
                "active_users": count,
            }
            for user, data in enumerate(find_user_details):
                result[user] = data
            return result
        except Exception as e:
            print(e)
        return 0

    def total_users_visited_in_last_week(self):
        try:
            todays_date = datetime.datetime.now().date()
            last_week_date = todays_date - datetime.timedelta(days=7)

            date_list = []
            current_date = last_week_date
            while current_date <= todays_date:
                date_str = current_date.strftime("%Y-%m-%d")
                date_list.append(date_str)
                current_date += datetime.timedelta(days=1)

            find_user_details = []
            count = 0
            for date in date_list:
                find_user_details += self.collection.find({date: {"$exists": True}})
                count += self.collection.count_documents({date: {"$exists": True}})
            result = {
                "date": f"{last_week_date.strftime('%Y-%m-%d')} to {todays_date.strftime('%Y-%m-%d')}",
                "active_users": count,
            }
            for user, data in enumerate(find_user_details):
                result[user] = data
            return result
        except Exception as e:
            print(e)
        return 0

    def total_users_visited_in_last_month(self):
        try:
            todays_date = datetime.datetime.now().date()
            last_month_date = todays_date - datetime.timedelta(days=30)

            date_list = []
            current_date = last_month_date
            while current_date <= todays_date:
                date_str = current_date.strftime("%Y-%m-%d")
                date_list.append(date_str)
                current_date += datetime.timedelta(days=1)

            find_user_details = []
            count = 0
            for date in date_list:
                find_user_details += self.collection.find({date: {"$exists": True}})
                count += self.collection.count_documents({date: {"$exists": True}})
            result = {
                "date": f"{last_month_date.strftime('%Y-%m-%d')} to {todays_date.strftime('%Y-%m-%d')}",
                "active_users": count,
            }
            for user, data in enumerate(find_user_details):
                result[user] = data
            return result
        except Exception as e:
            print(e)
        return 0
    def total_users_visited(self):
        """
        This method is used to get the total users visited.
        :return: int
        """
        try:
            count = self.collection.count_documents({})
            return count
        except Exception as e:
            print(e)
        return 0
    def total_users_visited_in_range_dates(self, start_date, end_date):
        if datetime.datetime.strptime(start_date, "%Y-%m-%d") > datetime.datetime.strptime(end_date, "%Y-%m-%d"):
            return "Start date should be less than end date"
        if datetime.datetime.strptime(start_date, "%Y-%m-%d") == datetime.datetime.strptime(end_date, "%Y-%m-%d"):
            return "Start date and end date should not be the same"

        try:
            date_list = []
            current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            while current_date <= datetime.datetime.strptime(end_date, "%Y-%m-%d"):
                date_str = current_date.strftime("%Y-%m-%d")
                date_list.append(date_str)
                current_date += datetime.timedelta(days=1)

            find_user_details = []
            count = 0
            for date in date_list:
                find_user_details += self.collection.find({date: {"$exists": True}})
                count += self.collection.count_documents({date: {"$exists": True}})
            result = {
                "date": f"{start_date} to {end_date}",
                "active_users": count,
            }
            for user, data in enumerate(find_user_details):
                result[user] = data
            return result

        except Exception as e:
            print(e)
        return 0
    def frequency_searched_keywords(self):
        """
        This method is used to get the frequency of searched keywords.
        :return: dict
        """
        try:
            find_user_details = self.collection.find({})
            result = {}
            for user, data in enumerate(find_user_details):
                for key , value in data.items():
                    if key != "_id" and key!="ip":
                        search_keywords = [item['search_keywords'] for item in data[key]['search_list']]

                        # Print the search keywords
                        for keyword in search_keywords:
                            if keyword in result:
                                result[keyword] += 1
                            else:
                                result[keyword] = 1


            # Sort the result in descending order
            result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
            return result
        except Exception as e:
            print(e)
        return 0
    def top_10_categories(self):
        """
        This method is used to get the top 10 categories.
        :return: dict
        """
        try:
            find_user_details = self.collection.find({})
            result = {}
            for user, data in enumerate(find_user_details):
                for key , value in data.items():
                    if key != "_id" and key!="ip":
                        categories = [item['category_id'] for item in data[key]['category_list']]

                        # Print the search keywords
                        for category in categories:
                            if category in result:
                                result[category] += 1
                            else:
                                result[category] = 1
            #sort the top 10 results in descending order
            result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:10])
            return result
        except Exception as e:
            print(e)
        return 0
    def top_10_products(self):
        """
        This method is used to get the top 10 products.
        :return: dict
        """
        try:
            find_user_details = self.collection.find({})
            result = {}
            for user, data in enumerate(find_user_details):
                for key , value in data.items():
                    if key != "_id" and key!="ip":
                        products = [item['product_id'] for item in data[key]['product_list']]

                        # Print the search keywords
                        for product in products:
                            if product in result:
                                result[product] += 1
                            else:
                                result[product] = 1
            #sort the top 10 results in descending order
            result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:10])
            return result
        except Exception as e:
            print(e)
        return 0
    def maximum_visit_portals(self):
        """
        This method is used to get the maximum visit portals.
        :return: dict
        """
        try:
            find_user_details = self.collection.find({})
            result = {}
            for user, data in enumerate(find_user_details):
                for key , value in data.items():
                    if key != "_id" and key!="ip":
                        portals = [item['source'] for item in data[key]['redirect_list']]

                        # Print the search keywords
                        for portal in portals:
                            if portal in result:
                                result[portal] += 1
                            else:
                                result[portal] = 1
            #sort the top 5 results in descending order
            result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:5])
            return result
        except Exception as e:
            print(e)
        return 0

if __name__ == '__main__':

    analytics = UserAnalytics(
        "****YOUR MONGODB CONNECTION STRING****",
        "product_db",
        "user_details"
    )

    # Get the total users visited
    total_users_visited = analytics.total_users_visited()
    print(f"Total users visited: {total_users_visited}")

    # Get the total users visited in range of dates
    total_users_visited_in_range_dates = analytics.total_users_visited_in_range_dates("2023-07-12", "2023-07-14")
    print(f"Total users visited in range of dates: {total_users_visited_in_range_dates}")

    # Get the frequency of searched keywords
    frequency_searched_keywords = analytics.frequency_searched_keywords()
    print(f"Frequency of searched keywords: {frequency_searched_keywords}")

    # Get the top 10 categories
    top_10_categories = analytics.top_10_categories()
    print(f"Top 10 categories: {top_10_categories}")

    # Get the top 10 products
    top_10_products = analytics.top_10_products()
    print(f"Top 10 products: {top_10_products}")

    # Get the maximum visit portals
    maximum_visit_portals = analytics.maximum_visit_portals()
    print(f"Maximum visit portals: {maximum_visit_portals}")

    # Close the connection

    analytics.close_connection()
