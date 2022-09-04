from configparser import ConfigParser
from logger import logger
import config as cfg
import pandas as pd
import requests
import sys
import os

def check_file(path):
    """It will check if the path parameter doesn't exist and it will create it if the condition is not met.
    """

    if not os.path.isdir(path):
        os.mkdir(path)

def parse_data(filename:str) -> pd.DataFrame:
    """Takes a CSV file from the 'raw_tweets' directory and parses it so it can be easier to work with. 

    Parameters:
        * filename(str): the name of the CSV file in 'raw_tweets' directory. Example: 'twitter_data'.
    """

    try:
        data = pd.read_csv(f"{cfg.RAW_TWEETS_PATH}/{filename}.csv")
    except FileNotFoundError:
        logger.error("Could not find the file. Make sure file exists and it's not given with the extension as a parameter.", exc_info=True)
        sys.exit()

    pd.set_option("display.max_colwidth", 1)
    pd.set_option("display.colheader_justify", "center")

    data.index += 1
    data[["tweet", "url"]] = data["content"].str.split("https://t.co/", expand=True, regex=False, n=1)
    data.drop(["url", "content"], axis=1, inplace=True)
    data.fillna("-", inplace=True)

    return data

def get_tweets_only(filename:str, count:int, export_as_csv=False) -> pd.DataFrame:
    """Returns or exports only the tweets made by the user.
    
    Parameters:
        * filename(str): the name of the CSV file in 'raw_tweets' directory. Example: 'twitter_data'.
        * count(int): the number of tweets that will be retrieved.
        * export_as_csv(bool): by default False; it will save the dataframe as a CSV file if True.
    """

    data = parse_data(filename=filename)

    tweets_only = data[data["replied_to_user"].isin(["-"]) & data["replied_to_tweet"].isin(["-"])]
    tweets_only = tweets_only.drop(tweets_only[tweets_only["tweet"].str.startswith("RT @")].index)
    tweets_only.reset_index(drop=True, inplace=True)
    tweets_only.index += 1
    tweets_only = tweets_only.drop(["replied_to_user", "replied_to_tweet"], axis=1)

    if count > len(tweets_only.index):
        count = len(tweets_only.index)
        logger.info(f"Count parameter exceeded total number of tweets and was automatically set to max amount, {len(tweets_only.index)}.")

    tweets_only = tweets_only.head(count)

    if export_as_csv:
        check_file(cfg.TWEETS_ONLY_PATH)
        tweets_only.to_csv(f"{cfg.TWEETS_ONLY_PATH}/{filename}.csv")
        logger.info("Export successful!")
    else:
        return tweets_only

def get_source_count(filename:str, count:int, tweets_only=True) -> dict:
    """Prints out in descending order the source of the tweets and the number.
    
    Parameters:
        * filename(str): the name of the CSV file in 'raw_tweets' directory. Example: 'twitter_data'.
        * count(int): the number of statuses that will be retrieved.
        * tweets_only(bool): by default True, will retrieve only the source for tweets, and not also for retweets and replies.
    """

    if tweets_only:
        data = get_tweets_only(filename=filename, count=count)
    else:
        data = parse_data(filename=filename)
        
    data = data.head(count)

    data = data["source"].value_counts().to_dict()

    for key, value in data.items():
        print(f"{key} - {value}")

def get_likes_count(filename:str, count:int, tweets_only=True) -> pd.DataFrame:
    """Prints out in descending order the number of likes for each tweet.
    
    Parameters:
        * filename(str): the name of the CSV file in 'raw_tweets' directory. Example: 'twitter_data'.
        * count(int): the number of statuses that will be retrieved.
        * tweets_only(bool): by default True, will retrieve only the likes for tweets, and not also for retweets and replies.
    """

    if tweets_only:
        data = get_tweets_only(filename=filename, count=count)
    else:
        data = parse_data(filename=filename)

    data = data.head(count)

    like_sort = data[["likes", "tweet"]].copy()
    like_sort.sort_values("likes", ascending=False, inplace=True, ignore_index=True)
    like_sort.index += 1

    print(like_sort)

def get_word_count(filename:str, count:int, tweets_only=True, export_as_csv=False) -> pd.DataFrame:
    """Prints out or exports the total number of each word used in all statuses.
    
    Parameters:
        * filename(str): the name of the CSV file in 'raw_tweets' directory. Example: 'twitter_data'.
        * count(int): the number of statuses that will be retrieved.
        * tweets_only(bool): by default True, will retrieve the words for tweets only; retweets and replies not included.
        * export_as_csv(bool): by default False; it will save the dataframe as a CSV file if True.
    """

    if tweets_only:
        data = get_tweets_only(filename=filename, count=count)
    else:
        data = parse_data(filename=filename)

    data = data.head(count)

    data["words"] = data["tweet"].str.lower().str.replace("[^\w\s]", "", regex=True)
    new_data = data["words"].str.split(expand=True).stack().value_counts().reset_index()

    new_data.columns = ["word_count", "apparitions"]
    new_data.index += 1

    if export_as_csv:
        check_file(cfg.WORDS_PATH)
        new_data.to_csv(f"{cfg.WORDS_PATH}/{filename}.csv", sep="|")
        logger.info("Export successful!")
    else:
        print(new_data)

def get_sentiment(filename:str, count:int, tweets_only=True, export_as_csv=False) -> pd.DataFrame:
    """Prints out or exports the dataframe which has a sentiment for each sentence in a tweet. The sentiment comes from Text Sentiment Analysis Method API. More information about this API: https://rapidapi.com/fyhao/api/text-sentiment-analysis-method.

    Parameters:
        * filename(str): the name of the CSV file in 'raw_tweets' directory. Example: 'twitter_data'.
        * count(int): the number of statuses that will be retrieved.
        * tweets_only(bool): by default True, will return only the sentiment for tweets, retweets and replies not included.
        * export_as_csv(bool): by default False; it will save the dataframe as a CSV file if True.
    """

    if tweets_only:
        data = get_tweets_only(filename=filename, count=count)
    else:
        data = parse_data(filename=filename)

    tweets_list = data["tweet"].tolist()

    config = ConfigParser()
    config.read(cfg.CONFIG)

    app_key = config["rapidapi"]["app_key"]

    url = "https://text-sentiment.p.rapidapi.com/analyze"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": f"{app_key}",
        "X-RapidAPI-Host": "text-sentiment.p.rapidapi.com"
    }

    tweets = []

    for tweet in tweets_list:
        payload = f"text={tweet}"

        response = requests.request("POST", url=url, data=payload.encode("UTF-8"), headers=headers)
        response = response.json()
        tweets.append(response)

    tweets_list = [[tweet["text"], tweet["pos_percent"], tweet["mid_percent"], tweet["neg_percent"]] for tweet in tweets]

    tweets_data = pd.DataFrame(tweets_list, columns=["tweet", "positive_sentiment", "average_sentiment", "negative_sentiment"])
    tweets_data.index += 1
    
    pd.set_option("display.max_colwidth", 50)

    tweets_data = tweets_data.head(count)

    if export_as_csv:            
        check_file(cfg.SENTIMENT_PATH)
        tweets_data.to_csv(f"{cfg.SENTIMENT_PATH}/{filename}.csv")
        logger.info("Export successful!")
    else:
        print(tweets_data)
