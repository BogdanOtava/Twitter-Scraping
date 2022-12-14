from scraper.scraper import Scraper
from config import USER_ACTIVITY_PATH, BROWSER_PATH
from logger import logger
import pandas as pd
import webbrowser as wb
import tweepy
import sys

class UserProfileScraper(Scraper):
    """Class used for scraping information about a particular Twitter account, such as tweets, replies, account details, etc. It inherits the Scraper class along with its attributes and methods. If the query is not a valid Twitter account, it will return an error.
    
    Parameters:
        * query(str): the twitter handle/tag of the account that will be scraped. Example: "twitter".
        * count(int): the number of tweets, retweets and replies that will be retrieved.

    Methods:
        * print_user_info(): prints out the user information.
        * go_to_profile(): opens browser to the profile of the account.
        * search_user_activity(): returns a dataframe with tweets, retweets and replies of the account. Use with the method inherited from Scraper, export_to_csv(), to export and save the dataframe.
    """

    def __init__(self, query, count):
        super().__init__(query, count)
        self.check_name()

        super().export_activity(USER_ACTIVITY_PATH)

    def check_name(self):
        """Checks whether the login keys are correct, and if there is an account with the given query. It will stop the execution if one of these conditions are not correct.
        """

        try:
            self.query.lower() == self.get_api().get_user(screen_name=self.query).screen_name.lower()
        except tweepy.Unauthorized:
            logger.error("Could not authenticate to Twitter API. Make sure the keys are correct.", exc_info=True)
            sys.exit()
        except tweepy.NotFound:
            logger.error(f"Account {self.query} could not be found. Make sure the name is correctly written.", exc_info=True)
            sys.exit()
        except tweepy.Forbidden:
            logger.error(f"Account {self.query} has been suspended.", exc_info=True)
            sys.exit()
        else:
            logger.info(f"Created object from query '{self.query}'.")

    def print_user_info(self) -> str:
        """Prints information about the Twitter account.
        """

        scraped_info = super().get_api().get_user(screen_name=self.query)

        user_info = {
            "Name": scraped_info.name,
            "Tag": scraped_info.screen_name,
            "Location": scraped_info.location,
            "Tweets": scraped_info.statuses_count,
            "Followers": scraped_info.followers_count,
            "Friends": scraped_info.friends_count,
            "Account Creation": scraped_info.created_at.strftime("%d-%B-%Y"),
            "Account Description": scraped_info.description
        }

        for keys, values in user_info.items():
            print(f"{keys} - {values}")

    def go_to_profile(self):
        """Goes to the instantiated Twitter account.
        """

        try:
            wb.get(BROWSER_PATH).open_new(f"twitter.com/{self.query}")
        except wb.Error:
            logger.error("Could not open the browser because the path is incorrect.", exc_info=True)

    def search_user_activity(self) -> pd.DataFrame:
        """Returns a dataframe with tweets from the instantiated Twitter account. Use together with export_to_csv() to export and save the dataframe.
        """

        tweets = tweepy.Cursor(super().get_api().user_timeline, screen_name=self.query).items(self.count)
        attributes = []

        for tweet in tweets:
            attributes.append([tweet.created_at, tweet.source, tweet.geo, tweet.lang, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.in_reply_to_screen_name, tweet.in_reply_to_status_id])
            columns = ["creation_date", "source", "location", "language", "content", "likes", "retweets", "replied_to_user", "replied_to_tweet"]

        tweets_data = pd.DataFrame(attributes, columns=columns)

        logger.info(f"Retrieved the last {self.count} tweets for account '{self.query}'.")

        return tweets_data
