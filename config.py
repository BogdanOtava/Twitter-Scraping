import pathlib

ROOT = pathlib.Path(__file__).parent
CONFIG = ROOT.joinpath("keys.ini")
BROWSER_PATH = f"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
LOGS_PATH = ROOT.joinpath("logs")

ACTIVITY_PATH = ROOT.joinpath("activity")
USER_ACTIVITY_PATH = ROOT.joinpath("activity/user_activity.json")
STATUS_ACTIVITY_PATH = ROOT.joinpath("activity/status_activity.json")

DATA_PATH = ROOT.joinpath("data")
RAW_TWEETS_PATH = ROOT.joinpath("data/raw_tweets")
TWEETS_ONLY_PATH = ROOT.joinpath("data/tweets_only")
WORDS_PATH = ROOT.joinpath("data/word_count")
SENTIMENT_PATH = ROOT.joinpath("data/sentiment")
