from scraper.scraper import Scraper
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

        try:
            self.query.lower() == self.get_api().get_user(screen_name=self.query).screen_name.lower()
        except tweepy.Unauthorized:
            print("Could not authenticate to Twitter API. Make sure the keys are correct.")
            sys.exit()
        except tweepy.NotFound:
            print(f"Account {self.query} could not be found. Make sure the name is correctly written, without the @.")
            sys.exit()

        super().export_user_activity()

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

        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        wb.get(chrome_path).open_new(f"twitter.com/{self.query}")

    def search_user_activity(self) -> pd.DataFrame:
        """Returns a dataframe with tweets from the instantiated Twitter account. Use together with export_to_csv() to export and save the dataframe.
        """

        tweets = tweepy.Cursor(super().get_api().user_timeline, screen_name=self.query).items(self.count)
        attributes = []

        for tweet in tweets:
            attributes.append([tweet.created_at, tweet.source, tweet.geo, tweet.lang, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.in_reply_to_screen_name, tweet.in_reply_to_status_id])
            columns = ["creation_date", "source", "location", "language", "content", "likes", "retweets", "replied_to_user", "replied_to_tweet"]

        tweets_data = pd.DataFrame(attributes, columns=columns)

        return tweets_data
