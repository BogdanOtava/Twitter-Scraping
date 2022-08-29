from scraper.user_profile_scraper import UserProfileScraper
from scraper.status_scraper import StatusScraper
import analysis_tools.user_tweets as user

mkbhd = UserProfileScraper("mkbhd", 250)
casey = UserProfileScraper("casey", 100)
musk = UserProfileScraper("elonmusk", 50)