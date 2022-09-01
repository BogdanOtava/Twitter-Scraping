from scraper.user_profile_scraper import UserProfileScraper
from scraper.status_scraper import StatusScraper
import analysis_tools.tweets_parsing as tweets

# twitter = UserProfileScraper("twitter", 25)
# casey = UserProfileScraper("casey", 10)

# iphone = StatusScraper("#iphone14", 250)
# goty = StatusScraper("#goty", 25)

# iphone_data = iphone.search_tweets()
# iphone.export_to_csv(iphone_data)

print(tweets.get_tweets_only("#iphone14_data.csv", 10))
tweets.get_source_count("#iphone14_data.csv", 10)
tweets.get_likes_count("#iphone14_data.csv", 10)
tweets.get_word_count("#iphone14_data.csv", 10)
tweets.get_sentiment("#iphone14_data.csv", 10)