from config import CONFIG, ROOT
from configparser import ConfigParser
from datetime import datetime
from abc import ABC
import tweepy
import json
import os

class Scraper(ABC):
    """Abstract class used as a blueprint for other classes."""

    def __init__(self, query:str, count:int):
        self.query = query
        self.count = count

    def get_api(self):
        """Enables direct access to Twitter using Twitter API. Takes the keys used to log in to the API from the config file in the main directory. Method is inherited by other classes and used by it's methods, and not straight by the user."""

        config = ConfigParser()
        config.read(CONFIG)

        api_key = config["twitter"]["api_key"]
        api_key_secret = config["twitter"]["api_key_secret"]
        access_token = config["twitter"]["access_token"]
        access_token_secret = config["twitter"]["access_token_secret"]

        auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        return api

    def export_activity(self):
        """Will be automatically called every time an instance is created and save the information in a JSON file.
        """

        path = f"{ROOT}/activity" 

        if not os.path.isdir(path):
            os.mkdir(path)

    def export_to_csv(self, dataframe):
        """Exports the dataframe given as parameter to a CSV file in 'data' directory which is located in the main directory. If 'data' doesn't exist it will create it first and then save the CSV file in it."""

        path = f"{ROOT}/data"

        if not os.path.isdir(path):
            os.mkdir(path)

        dataframe.to_csv(f"{ROOT}/data/{self.query}_data.csv", index=False, encoding="UTF-8")
