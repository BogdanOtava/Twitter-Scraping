from scraper.scraper import Scraper
from config import STATUS_ACTIVITY_PATH
from logger import logger
import tweepy
import pandas as pd

class StatusScraper(Scraper):
    """Class used for scraping information about a particular word or hashtag. It inherits the Scraper class along with its attributes and methods. If the query is not a valid Twitter account, it will return an error.

    Parameters:
        * query(str): the word or hashtag that will be scraped. Examples: "Tesla" or "#iPhone14".
        * count(int): the number of tweets, retweets and replies that will be retrieved.

    Methods:
        * search_tweets(): returns a dataframe with tweets, retweets and replies about the given query.
    """

    def __init__(self, query, count):
        super().__init__(query, count)
        logger.info(f"Created object from query '{self.query}'.")

        super().export_activity(STATUS_ACTIVITY_PATH)

    def search_tweets(self) -> pd.DataFrame:
        """Returns a dataframe with tweets, retweets and replies about the given query.
        """

        tweets = tweepy.Cursor(super().get_api().search_tweets, q=self.query).items(self.count)
        attributes = []

        for tweet in tweets:
            attributes.append([tweet.created_at, tweet.source, tweet.geo, tweet.lang, tweet.user.screen_name, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.in_reply_to_screen_name, tweet.in_reply_to_status_id])
            columns = ["creation_date", "source", "location", "language", "author", "content", "likes", "retweets", "replied_to_user", "replied_to_tweet"]

        tweets_data = pd.DataFrame(attributes, columns=columns)

        logger.info(f"Retrieved the last {self.count} tweets for word '{self.query}'.")

        return tweets_data
