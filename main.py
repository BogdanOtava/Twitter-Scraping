from config import ROOT
from scraper.user_profile_scraper import UserProfileScraper
from scraper.status_scraper import StatusScraper
import analysis_tools.user_tweets as user

account_one = UserProfileScraper("samsheffer", 100)
# account_one.check_validity()
# account_one.print_user_info()
# account_one.go_to_profile()

# account_one_data = account_one.search_user_activity()
# account_one.export_to_csv(account_one_data)

# print(user.get_tweets_only("samsheffer_data.csv", 10))

# user.get_source_count("samsheffer_data.csv", 10)
# user.get_likes_count("samsheffer_data.csv", 10)
# user.get_word_count("samsheffer_data.csv", 25)

account_two = UserProfileScraper("twitter", 50)