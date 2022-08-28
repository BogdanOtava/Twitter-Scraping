from configparser import ConfigParser
from config import CONFIG, ROOT
import pandas as pd
import requests

pd.set_option("display.max_colwidth", 1)
pd.set_option("display.colheader_justify", "center")

def parse_data(filename):
    """Returns a dataframe from the file that was given as parameter that was parsed so it can be easier to work with.
    
    Parameters:
        * filename: a CSV file from the data directory. Example: 'twitter_data.csv'.
    """

    try:
        data = pd.read_csv(f"{ROOT}/data/{filename}")
    except Exception as error:
        print(error)
    else:
        data.index += 1
        data[["tweet", "url"]] = data["content"].str.split("https://t.co/", expand=True, regex=False, n=1)
        data.drop(["url", "content"], axis=1, inplace=True)
        data.fillna("-", inplace=True)

    return data

def get_tweets_only(filename, count:int):
    """Returns only the tweets made by the user for the given dataframe.
    
    Parameters:
        * filename: a CSV file from the data directory. Example: 'twitter_data.csv'.
        * count(int): the number of tweets that will be retrieved.

    Raises:
        * ValueError: if 'count' is less than 1 or more than the length of the dataframe.
    """

    data = parse_data(filename=filename)

    tweets_only = data[data["replied_to_user"].isin(["-"]) & data["replied_to_tweet"].isin(["-"])]
    tweets_only = tweets_only.drop(tweets_only[tweets_only["tweet"].str.startswith("RT @")].index)
    tweets_only.reset_index(drop=True, inplace=True)
    tweets_only.index += 1
    tweets_only = tweets_only.drop(["replied_to_user", "replied_to_tweet"], axis=1)

    if count < 1 or count > len(tweets_only.index):
        raise ValueError(f"count parameter cannot be less than 1 or bigger than the length of the dataframe, {len(tweets_only.index)}.")

    return tweets_only.head(count)

def get_source_count(filename, count:int, tweets_only=True):
    """Prints in descending order the source of the tweets and the number.
    
    Parameters:
        * filename: a CSV file from the data directory. Example: 'twitter_data.csv'.
        * count(int): the number of statuses that will be retrieved.
        * tweets_only(bool): by default True, will retrieve only the source for tweets, and not also for retweets and replies.
    """

    if tweets_only == True:
        data = get_tweets_only(filename=filename, count=count)
    else:
        data = parse_data(filename=filename)
        
    data = data.head(count)

    data = data["source"].value_counts().to_dict()

    for key, value in data.items():
        print(f"{key} - {value}")

def get_likes_count(filename, count:int, tweets_only=True):
    """Prints in descending order the number of likes for each tweet.
    
    Parameters:
        * filename: a CSV file from the data directory. Example: 'twitter_data.csv'
        * count(int): the number of statuses that will be retrieved.
        * tweets_only(bool): by default True, will retrieve only the likes for tweets, and not also for retweets and replies.
    """

    if tweets_only == True:
        data = get_tweets_only(filename=filename, count=count)
    else:
        data = parse_data(filename=filename)

    data = data.head(count)

    like_sort = data[["likes", "tweet"]].copy()
    like_sort.sort_values("likes", ascending=False, inplace=True, ignore_index=True)
    like_sort.index += 1

    print(like_sort)

def get_word_count(filename, count:int, tweets_only=True):
    """Prints the total number of each word used in all statuses.
    
    Parameters:
        * filename: a CSV file from the data directory. Example: 'twitter_data.csv'.
        * count(int): the number of statuses that will be retrieved.
        * tweets_only(bool): by default True, will retrieve the words for tweets only; retweets and replies not included.
    """

    if tweets_only == True:
        data = get_tweets_only(filename=filename, count=count)
    else:
        data = parse_data(filename=filename)

    data = data.head(count)

    data["words"] = data["tweet"].str.lower().str.replace("[^\w\s]", "", regex=True)
    new_data = data["words"].str.split(expand=True).stack().value_counts().reset_index()

    new_data.columns = ["word_count", "apparitions"]
    new_data.index += 1

    print(new_data)

def get_sentiment(query:str):

    config = ConfigParser()
    config.read(CONFIG)

    app_key = config["rapidapi"]["app_key"]

    url = "https://text-sentiment.p.rapidapi.com/analyze"
    payload = f"text={query}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": f"{app_key}",
        "X-RapidAPI-Host": "text-sentiment.p.rapidapi.com"
    }

    response = requests.request("POST", url=url, data=payload, headers=headers)
    response = response.json()

    data = pd.DataFrame.from_dict([response])
    data["mean"] = data.iloc[:, 2:4].mean(axis=1)

    print(data.head())