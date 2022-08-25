from scraper.scraper import Scraper
import tweepy
import pandas as pd
import webbrowser as wb

class UserProfileScraper(Scraper):
    scraped_profiles = []

    def __init__(self, query, count):
        super().__init__(query, count)

        UserProfileScraper.scraped_profiles.append(query)

    def check_validity(self):
        """Checks and prints whether or not the instance parameter is a valid Twitter account."""

        user_name = super().get_api().get_user(screen_name=self.query)

        if user_name.screen_name.upper() == self.query.upper():
            print(f"{user_name.screen_name} is a valid Twitter account.")
        else:
            print(f"{user_name.screen_name} is not a valid Twitter account.")

    def print_user_info(self):
        """Prints some information about the Twitter account."""

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
        """Goes to the instantiated Twitter account."""

        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        wb.get(chrome_path).open_new(f"twitter.com/{self.query}")

    def search_user_activity(self):
        """Returns a dataframe with tweets from the instantiated Twitter account."""

        tweets = tweepy.Cursor(super().get_api().user_timeline, screen_name=self.query).items(self.count)
        attributes = []

        for tweet in tweets:
            attributes.append([tweet.created_at, tweet.source, tweet.geo, tweet.lang, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.in_reply_to_screen_name, tweet.in_reply_to_status_id])
            columns = ["creation_date", "source", "location", "language", "content", "likes", "retweets", "replied_to_user", "replied_to_tweet"]

        tweets_data = pd.DataFrame(attributes, columns=columns)

        return tweets_data