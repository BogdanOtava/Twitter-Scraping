from scraper.scraper import Scraper
import tweepy
import pandas as pd

class StatusScraper(Scraper):
    scraped_queries = []

    def __init__(self, query, count):
        super().__init__(query, count)

        StatusScraper.scraped_queries.append(query)

    def search_tweets(self):
        """Returns a dataframe with tweets about the given query."""

        tweets = tweepy.Cursor(super().get_api().search_tweets, q=self.query).items(self.count)
        attributes = []

        for tweet in tweets:
            attributes.append([tweet.created_at, tweet.source, tweet.geo, tweet.lang, tweet.user.screen_name, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.in_reply_to_screen_name, tweet.in_reply_to_status_id])
            columns = ["creation_date", "source", "location", "language", "author", "content", "likes", "retweets", "replied_to_user", "replied_to_tweet"]

        tweets_data = pd.DataFrame(attributes, columns=columns)

        return tweets_data