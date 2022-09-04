from config import CONFIG, ACTIVITY_PATH, RAW_TWEETS_PATH, DATA_PATH
from configparser import ConfigParser
from pandas import DataFrame
from datetime import datetime
from logger import logger
import tweepy
import json
import sys
import os

class Scraper:
    """Abstract class used as a blueprint for other classes.
    """

    def __init__(self, query:str, count:int):
        self.check_value(count)

        self.query = query
        self.count = count

    def check_value(self, count:int):
        """Checks for the count parameter to be greater than 0, else it will stop the execution.
        """

        try:
            assert count > 0
        except AssertionError:
            logger.error(f"Count parameter has to be greater than 0, got {count}.", exc_info=True)
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
        """Gets information whenever an object is instantiated from one of the classes that inherits the Scraper class.
        """

        tag = str(self.query)
        scraped_statuses = self.count
        date_time = str(datetime.now().strftime("%d-%m-%Y / %H:%M:%S"))

        activity = {tag: {"scraped_statuses": scraped_statuses, "date_time": date_time}}

        return activity

    def export_activity(self, path):
        """It will automatically export information about the instantiated object in JSON format.
        """

        if not os.path.isdir(ACTIVITY_PATH):
            os.mkdir(ACTIVITY_PATH)

        if os.path.exists(path):
            with open(path, "r") as file:
                activity = json.load(file)

            activity.append(self.get_activity())

            with open(path, "w") as file:
                json.dump(activity, file, indent=4)

        else:
            with open(path, "w") as file:
                activity = [self.get_activity()]

                json.dump(activity, file, indent=4)

    def export_dataframe(self, dataframe: DataFrame):
        """Exports the dataframe given as parameter to a CSV file in 'data/raw_tweets'."""

        if not os.path.isdir(DATA_PATH):
            os.mkdir(DATA_PATH)

        if not os.path.isdir(RAW_TWEETS_PATH):
            os.mkdir(RAW_TWEETS_PATH)

        dataframe.to_csv(f"{RAW_TWEETS_PATH}/{self.query}_data.csv", index=False, encoding="UTF-8")
        logger.info("Export successful!")
