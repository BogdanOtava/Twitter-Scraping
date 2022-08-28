from scraper.user_profile_scraper import UserProfileScraper
from scraper.status_scraper import StatusScraper
import analysis_tools.user_tweets as user

mkbhd = UserProfileScraper("mkbhd", 100)
# mkbhd.print_user_info()
# mkbhd.go_to_profile()

# export = mkbhd.search_user_activity()
# mkbhd.export_to_csv(export)

# user.get_likes_count("mkbhd_data.csv", 25)
# user.get_source_count("mkbhd_data.csv", 10)
print(user.get_tweets_only("mkbhd_data.csv", 10))