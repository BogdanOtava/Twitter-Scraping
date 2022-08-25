from scraper.user_profile_scraper import UserProfileScraper
from scraper.status_scraper import StatusScraper
from analysis_tools.user_tweets import get_tweets_only

user_1 = UserProfileScraper("mkbhd", 100)
# user_1.check_validity()
# user_1.print_user_info()
# user_1.go_to_profile()

# user_1_activity = user_1.search_user_activity()
# user_1.export_to_csv(user_1_activity)

print(get_tweets_only("mkbhd_data.csv", 10))