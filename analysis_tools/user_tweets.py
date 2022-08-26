from config import ROOT
import pandas as pd

pd.set_option("display.max_colwidth", 1)
pd.set_option("display.colheader_justify", "center")

def parse_data(filename):
    """Returns a dataframe from the file that was given as parameter that was parsed so it can be easier to work with."""

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

def get_source_count(filename, count:int):
    """ in descending order the source of the tweets and the number."""

    data = parse_data(filename=filename)
    data = data.head(count)

    data = data["source"].value_counts().to_dict()

    for key, value in data.items():
        print(f"{key} - {value}")

def get_likes_count(filename, count:int):
    """Prints in descending order the number of likes for each tweet."""

    data = parse_data(filename=filename)
    data = data.head(count)

    like_sort = data[["likes", "tweet"]].copy()
    like_sort.sort_values("likes", ascending=False, inplace=True, ignore_index=True)
    like_sort.index += 1

    print(like_sort)

def get_word_count(filename, count:int):
    """Prints the total number of each word used in tweets."""

    data = parse_data(filename=filename)
    data = data.head(count)

    data["words"] = data["tweet"].str.lower().str.replace("[^\w\s]", "", regex=True)
    new_data = data["words"].str.split(expand=True).stack().value_counts().reset_index()

    new_data.columns = ["word_count", "apparitions"]
    new_data.index += 1

    print(new_data)
