# THIS IS AN UPDATED COMMENT TO MAKE SURE GIT WORKS CORRECTLY
# Python script that gathers data for a specified user and returns data in CSV format
import os
import csv
import tweepy
import pandas as pd
from pathlib import Path
from tqdm import tqdm

def set_path():
    '''
    Function that gets the current working directory, sets a path variable, and allows us to more easily store data 
    in correct location.
    
    IMPORTANT NOTE: please create a folder named 'data' as the first step before gathering any data.
    '''
    return Path(os.getcwd())

def load_env():
    '''
    Load in Twitter API keys & tokens via os environment variables.
    '''
    API_KEY = os.environ.get("API_KEY")
    API_SECRET_KEY = os.environ.get("API_SECRET_KEY")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
    return API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

def get_user(key, secret_key, token, token_secret):
    '''
    Gathers input for Twitter username, ensures that it is a valid account, and returns username as string.
    '''
    # Tweepy authorization
    auth = tweepy.OAuthHandler(key, secret_key)
    
    # set Tweepy access token's
    auth.set_access_token(token, token_secret)
    
    # call Twitter API
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    # ask for input
    while True:
        user_input = str(input("Please enter username of Verified Twitter User: "))
        try:
            if api.get_user(user_input):
                return user_input
        except:
            print("Please enter valid username.")


def is_retweet(tweet):
    '''
    Returns True/False if Tweet is a retweet.
    '''
    if "RT @" in tweet.full_text:
        return True
    else:
        return False


def get_tweets(path, user, key, secret_key, token, token_secret):
    '''
    Function that gathers input user's Tweets and outputs them to a CSV file.
    '''
    # open new CSV file into data folder of current directory
    csv_file = open(path/f"csv-data/{user}.csv", "a")
    # create CSV writer
    csv_writer = csv.writer(csv_file)
    
    # write a single row with the headers of the columns
    csv_writer.writerow(
        [
            "id_str",
            "screen_name",
            "created_at",
            "lang",
            "source",
            "retweet_count",
            "favorite_count",
            "is_retweet",
            "full_text"
        ]
    )
    
    # Tweepy authorization
    auth = tweepy.OAuthHandler(key, secret_key)
    
    # set Tweepy access token's
    auth.set_access_token(token, token_secret)
    
    # call Twitter API
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    # get Tweets
    for tweet in tqdm(tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items()):
        csv_writer.writerow(
            [
                tweet.id_str,
                tweet.user.screen_name,
                tweet.created_at,
                tweet.lang,
                tweet.source,
                tweet.retweet_count,
                tweet.favorite_count,
                is_retweet(tweet),
                tweet.full_text
            ]
        )
            
    # close csv file
    csv_file.close()


def main():
    '''
    Main program for gathering data from Twitter.
    '''
    # set path variable
    path = set_path()
    
    # load in environment variables to access Twitter API
    API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = load_env()
    
    # get username
    user = get_user(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    # get user's Tweets via Tweepy
    get_tweets(path=path, user=user, key=API_KEY, secret_key=API_SECRET_KEY, token=ACCESS_TOKEN, token_secret=ACCESS_TOKEN_SECRET)
    
    # get length of CSV file (i.e. # of tweets gathered)
    length = len(pd.read_csv(path/f"csv-data/{user}.csv"))
    
    # print out length of CSV
    print("Successfully gathered {} from {}.".format(length, user))
    
    
if __name__ == "__main__":
    main()