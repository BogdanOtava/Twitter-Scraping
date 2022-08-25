from config import CONFIG, ROOT
from configparser import ConfigParser
import tweepy

class Scraper:
    def __init__(self, query:str, count:int):
        self.query = query
        self.count = count

    def get_api(self):
        """Enables direct access to Twitter."""

        config = ConfigParser()
        config.read(CONFIG)

        api_key = config["twitter"]["api_key"]
        api_key_secret = config["twitter"]["api_key_secret"]
        access_token = config["twitter"]["access_token"]
        access_token_secret = config["twitter"]["access_token_secret"]

        auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        return api

    def export_to_csv(self, dataframe):
        """Exports given dataframe given as parameter to a CSV file."""

        dataframe.to_csv(f"{ROOT}/data/{self.query}_data.csv", index=False, encoding="UTF-8")