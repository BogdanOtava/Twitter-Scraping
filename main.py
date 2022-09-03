from scraper.user_profile_scraper import UserProfileScraper
from scraper.status_scraper import StatusScraper
import tools.tweets_parsing as tweets

# 1. Create object
# mrbeast = UserProfileScraper("mrbeast", 250)
# iphone = StatusScraper("#iphone14", 100)

# 2. Object methods
# mrbeast.print_user_info()
# mrbeast.go_to_profile()
# mrbeast.search_user_activity()
# apple.search_tweets()

# 3. Save tweets to CSV file
# mrbeast_data = mrbeast.search_user_activity()
# iphone_data = iphone.search_tweets()

# mrbeast.export_dataframe(mrbeast_data)
# iphone.export_dataframe(iphone_data)

# 4. Analyze data
# tweets.get_tweets_only("mrbeast_data", 34, export_as_csv=True)
# tweets.get_source_count("mrbeast_data", 34)
# tweets.get_likes_count("mrbeast_data", 34)
# tweets.get_word_count("mrbeast_data", 34, export_as_csv=True)
tweets.get_sentiment("mrbeast_data", 34, export_as_csv=True)
