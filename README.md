## About The Project
This project was developed as my portofolio project for attending and graduating a five month long [Python Development course](https://www.itschool.ro/).

[Twitter](https://en.wikipedia.org/wiki/Twitter,_Inc.) is one of the best social media platforms to scrape data from. It's [API](https://developer.twitter.com/en) is quite permissive, easy to work with, and of course, free. The API enables access to core elements of Twitter, such as getting tweets or users information, tweeting from outsite Twitter, or even making bots.

What I wanted to accomplish with this project, was to scrape tweets in Python and get, in an easy to read way, information such as word count, most liked tweets, source of the tweets or AI sentiment.

## Getting Started
For the program to run smoothly, there are a few things needed.

### External dependencies & services
You will firstly need make an account or login with your Twitter account to the [Developer Platform](https://developer.twitter.com/en). Make a new APP and generate the api keys and access tokens. In the working directory, create a keys.ini file, copy the following information and add the generated keys.

While we're at it, you'll need an account on [RapidAPI](https://rapidapi.com/hub) as well, and put the key in the same keys.ini file. This is needed, because this [API](https://rapidapi.com/fyhao/api/text-sentiment-analysis-method/) was used to get the sentiment for the tweets.

```
[twitter]

api_key = 
api_key_secret = 
bearer_token = 
access_token = 
access_token_secret = 

[rapidapi]

app_key =
```

### Prerequisites
The following libraries and packages will be needed:
  * [tweepy](https://www.tweepy.org/) -> provides access to Twitter API within Python.
  
  `pip install tweepy`
  
  * [pandas](https://pandas.pydata.org/) -> data manipulation and analysis tool.
  
  `pip install pandas`
   
   * [requests](https://requests.readthedocs.io/en/latest/#) -> HTTP library that allows sending HTTP requests easily.

  `pip install requests`
  
## How To Use
After installing everything previously mentioned, the program should work without any problems. Because the Twitter API scrapes all the activity (tweets, retweets, replies), from now on, the activity will be refered to as __status__. Down below, there's a simple example of how to get the statuses of a user and save them locally. For more information about how the classes or function work, or other methods you can use, refer to their documentation.

### Retrieving data
First step is to actually get some information from twitter. Let's say we want to scrape the [GitHub Profile](https://twitter.com/github) and save the statuses in a CSV file. Write the code in *main.py*.

#### 1. Create the object. 
Takes the profile tag as first argument, and the number of statuses you want to retrieve as the second arguemnt.

`github = UserProfileScraper("github", 100)`

#### 2. Get data.
We'll store the statuses in a variable. These will be retrieved by the *search_user_activity()* method.

`github_data = github.search_user_activity()`

#### 3. Save data.
To save the scraped statuses locally, we'll use the *export_dataframe* method, passing as argument the previously created variable, *github_data*, where we stored the statuses.

`github.export_dataframe(github_data)`

The statuses are now saved in the current working directory, in *data/raw_tweets*.

### Analyze data
With the file saved, the next step is to actually get some relevant information about the retrieved statuses.

#### 1. See only the tweets.
From the 100 statuses previously scraped, we'll save only the tweets in another CSV file, in *data/tweets_only*. Another option is to directly print out the tweets in the console, without passing the *export_as_csv* argument.

`tweets.get_tweets_only("github_data", 100, export_as_csv=True)`

#### 2. See like & source count.
Prints out the likes count for each tweet in descending order, respectively the devices the tweets were posted from. Pass *tweets_only=False* as argument to one of the functions to see information about all statuses, not only tweets.

`tweets.get_likes_count("github_data", 100)`
`tweets.get_source_count("github_data", 100)`

#### 3. Get the word count.
For better visibility, we'll save this as CSV file in *data/word_count*. This CSV file will show each word and the number of times it was used in the last tweets from the 100 statuses. Pass *tweets_only=False* as argument to see the count for all statuses.

`tweets.get_word_count("github_data", 100, export_as_csv=True)`

#### 4. Get sentiment.
This uses [Text Sentiment Analysis API](https://rapidapi.com/fyhao/api/text-sentiment-analysis-method). You can either print them out or save as csv in *data/sentiment*.

`print(tweets.get_sentiment("github_data", 10))`

## To Be Added & Changed
 * Incorporate command line arguments with __Argparse Module__.
 * Improve the logger.
 * Create own *Sentiment Analysis* tool.
