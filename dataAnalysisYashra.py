from pymongo import MongoClient
import datetime

class UserAnalytics:
    def __init__(self, connection_string, db_name, collection_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def close_connection(self):
        self.client.close()

    def total_users_visited_in_a_day(self, date):
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

    def total_users_visited_in_range_dates(self, start_date, end_date):
        if datetime.datetime.strptime(start_date, "%Y-%m-%d") > datetime.datetime.strptime(end_date, "%Y-%m-%d"):
            return "Start date should be less than end date"
        if datetime.datetime.strptime(start_date, "%Y-%m-%d") == datetime.datetime.strptime(end_date, "%Y-%m-%d"):
            return "Start date and end date should not be the same"
        if datetime.datetime.strptime(start_date, "%Y-%m-%d") > datetime.datetime.now().date():
            return "Start date should not be greater than today's date"
        if datetime.datetime.strptime(end_date, "%Y-%m-%d") > datetime.datetime.now().date():
            return "End date should not be greater than today's date"

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

# Usage example
analytics = UserAnalytics(
    "mongodb://rem_user_mongo:myserver%40123@151.106.35.158:27017/?authMechanism=DEFAULT",
    "product_db",
    "user_details"
)

user_visited_today = analytics.total_users_visited_in_range_dates("2023-07-14", "2023-07-13")
print(user_visited_today)

analytics.close_connection()
