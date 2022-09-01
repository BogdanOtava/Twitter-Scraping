from config import CONFIG, ROOT
from configparser import ConfigParser
from pandas import DataFrame
from datetime import datetime
from abc import ABC
import tweepy
import json
import os

class Scraper(ABC):
    """Abstract class used as a blueprint for other classes.
    """

    def __init__(self, query:str, count:int):
        self.query = query
        self.count = count

        try:
            assert self.count > 0
        except AssertionError:
            print(f"Count parameter has to be greater than 0, got {count}.")

    def get_api(self):
        """Enables direct access to Twitter using Twitter API. Takes the keys used to log in to the API from the config file in the main directory. Method is inherited by other classes and used by it's methods, and not straight by the user.
        """

        config = ConfigParser()
        config.read(CONFIG)

        api_key = config["twitter"]["api_key"]
        api_key_secret = config["twitter"]["api_key_secret"]
        access_token = config["twitter"]["access_token"]
        access_token_secret = config["twitter"]["access_token_secret"]

        auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        return api

    def get_activity(self):
        """Gets information whenever an object is instantiated from one of the classes that inherits the Scraper class.
        """

        tag = str(self.query)
        scraped_statuses = self.count
        date_time = str(datetime.now().strftime("%d-%m-%Y / %H:%M:%S"))

        activity = {tag: {"scraped_statuses": scraped_statuses, "date_time": date_time}}

        return activity

    def export_user_activity(self):
        """Exports information about the instantiated object in a JSON file.
        """

        path = f"{ROOT}/activity" 
        user_path = f"{ROOT}/activity/user_activity.json"

        if not os.path.isdir(path):
            os.mkdir(path)

        if os.path.exists(user_path):
            with open(user_path, "r") as file:
                activity = json.load(file)

            activity.append(self.get_activity())

            with open(user_path, "w") as file:
                json.dump(activity, file, indent=4)

        else:
            with open(user_path, "w") as file:
                activity = [self.get_activity()]

                json.dump(activity, file, indent=4)

    def export_status_activity(self):
        """Export information about the instantiated object in a JSON file.
        """

        path = f"{ROOT}/activity"
        status_path = f"{ROOT}/activity/status_activity.json"

        if not os.path.isdir(path):
            os.mkdir(path)

        if os.path.exists(status_path):
            with open(status_path, "r") as file:
                activity = json.load(file)

            activity.append(self.get_activity())

            with open(status_path, "w") as file:
                json.dump(activity, file, indent=4)

        else:
            with open(status_path, "w") as file:
                activity = [self.get_activity()]

                json.dump(activity, file, indent=4)

    def export_to_csv(self, dataframe: DataFrame):
        """Exports the dataframe given as parameter to a CSV file in 'data' directory which is located in the main directory. If 'data' doesn't exist it will create it first and then save the CSV file in it."""

        path = f"{ROOT}/data"

        if not os.path.isdir(path):
            os.mkdir(path)

        dataframe.to_csv(f"{ROOT}/data/{self.query}_data.csv", index=False, encoding="UTF-8")
