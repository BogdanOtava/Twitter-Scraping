from config import CONFIG, ROOT
from configparser import ConfigParser
from pandas import DataFrame
from datetime import datetime
from abc import ABC
import sys
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
            self.query.lower() == self.get_api().get_user(screen_name=self.query).screen_name.lower()
        except tweepy.Unauthorized:
            print("Could not authenticate to Twitter API. Make sure the keys are correct.")
            sys.exit()
        except tweepy.NotFound:
            print(f"Account {self.query} could not be found. Make sure the name is correctly written.")
            sys.exit()

        try:
            assert count > 0
        except AssertionError:
            print(f"Count parameter has to be greater than 0, got {count}.")
            sys.exit()

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
        """Gets information about the instance that will be used as an activity history. Returns a dictonary.
        """

        tag = str(self.query)
        account = str(self.get_api().get_user(screen_name=self.query).name)
        scraped_statuses = self.count
        date_time = str(datetime.now().strftime("%d-%m-%Y / %H:%M:%S"))

        activity_log = {tag: {"account_name": account, "scraped_statuses": scraped_statuses, "date_time": date_time}}

        return activity_log

    def export_user_activity(self):
        """Will be automatically called every time an instance of UserProfileScraper class is created and save the information in a JSON file. It will create the necessary directory and files if they don't exist already.
        """

        path = f"{ROOT}/activity" 
        json_path = f"{ROOT}/activity/user_activity.json"

        if not os.path.isdir(path):
            os.mkdir(path)

        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                activity = json.load(file)

            activity.append(self.get_activity())

            with open(json_path, "w") as file:
                json.dump(activity, file, indent=4)

        else:
            with open(json_path, "w") as file:
                activity = [self.get_activity()]

                json.dump(activity, file, indent=4)

    def export_to_csv(self, dataframe: DataFrame):
        """Exports the dataframe given as parameter to a CSV file in 'data' directory which is located in the main directory. If 'data' doesn't exist it will create it first and then save the CSV file in it."""

        path = f"{ROOT}/data"

        if not os.path.isdir(path):
            os.mkdir(path)

        dataframe.to_csv(f"{ROOT}/data/{self.query}_data.csv", index=False, encoding="UTF-8")
