from scraper.scraper import Scraper
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

        super().export_activity()

    def search_tweets(self):
        """Returns a dataframe with tweets, retweets and replies about the given query."""

        tweets = tweepy.Cursor(super().get_api().search_tweets, q=self.query).items(self.count)
        attributes = []

        for tweet in tweets:
            attributes.append([tweet.created_at, tweet.source, tweet.geo, tweet.lang, tweet.user.screen_name, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.in_reply_to_screen_name, tweet.in_reply_to_status_id])
            columns = ["creation_date", "source", "location", "language", "author", "content", "likes", "retweets", "replied_to_user", "replied_to_tweet"]

        tweets_data = pd.DataFrame(attributes, columns=columns)

        return tweets_data
