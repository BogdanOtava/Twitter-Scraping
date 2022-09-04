from scraper.user_profile_scraper import UserProfileScraper
from scraper.status_scraper import StatusScraper
import tools.tweets_parsing as tweets

# 1. Create object
# twitter = UserProfileScraper("twitter", 250)
# california = StatusScraper("#california", 100)

# 2. Get information about the user
# twitter.print_user_info()
# twitter.go_to_profile()

# 3. Print tweets or save them in a CSV file
# twitter_data = twitter.search_user_activity()
# twitter.export_dataframe(twitter_data)

# california_data = california.search_tweets()
# california.export_dataframe(california_data)

# 4. Analyze the retrieved data
# tweets.get_tweets_only("twitter_data", 250, export_as_csv=True)
# tweets.get_likes_count("twitter_data", 250)
# tweets.get_source_count("twitter_data", 250)
# tweets.get_word_count("twitter_data", 250, export_as_csv=True)
# tweets.get_sentiment("twitter_data", 250, export_as_csv=True)
