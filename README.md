### WORK IN PROGRESS

# Twitter-Scraping

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
