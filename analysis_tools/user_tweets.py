from config import ROOT
from shutil import ReadError
import pandas as pd

pd.set_option("display.max_colwidth", 1)
pd.set_option("display.colheader_justify", "center")

def parse_data(filename):
    """Returns a dataframe from the file that was given as parameter that was parsed so it can be easier to work with."""

    try:
        data = pd.read_csv(f"{ROOT}/data/{filename}")
    except ReadError as error:
        print(error)
    else:
        data.index += 1
        data[["tweet", "url"]] = data["content"].str.split("https://t.co/", expand=True, regex=False, n=1)
        data.drop(["url", "content"], axis=1, inplace=True)
        data.fillna("-", inplace=True)

    return data

def get_tweets_only(filename, count:int):
    """Returns only the tweets made by the user for the given dataframe."""

    data = parse_data(filename=filename)

    tweets_only = data[data["replied_to_user"].isin(["-"]) & data["replied_to_tweet"].isin(["-"])]
    tweets_only = tweets_only.drop(tweets_only[tweets_only["tweet"].str.startswith("RT @")].index)
    tweets_only.reset_index(drop=True, inplace=True)
    tweets_only.index += 1
    tweets_only = tweets_only.drop(["replied_to_user", "replied_to_tweet"], axis=1)

    if count < 1 or count > len(tweets_only.index):
        raise ValueError(f"count parameter cannot be less than 1 or bigger than the length of the dataframe, {len(tweets_only.index)}.")

    return tweets_only.head(count)

# def get_source_count(dataframe):
#     """Returns in descending order the source of the tweets and the number."""

#     source = dataframe["source"].value_counts()

#     return source

# def get_likes_count(dataframe):
#     """Returns in descending order the number of likes for each tweet."""

#     pd.set_option("display.max_colwidth", None)
#     pd.set_option("display.colheader_justify", "left")

#     like_sort = dataframe[["likes", "content"]].copy()
#     like_sort.sort_values("likes", ascending=False, inplace=True, ignore_index=True)
#     like_sort.index += 1

#     return like_sort

# print(get_likes_count(data))
# print(get_tweets_only(data, 10))