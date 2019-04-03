import sys
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor

def get_twitter_auth():
    #setup twitter authentication
    #return: tweepy.OAuthHandler object
    #look on twitter_API_keys.txt to get consumer/access keys

    try:
        consumer_key = "XXXXX"
        consumer_secret = "XXXXX"  
        access_token = "XXXXX"
        access_secret = "XXXXX"
    except KeyError:
        sys.stderr.write("TWITTER_* env vars not set\n")
        sys.exit(1)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

def get_twitter_client():
    #setup twitter API client
    #return tweepy.API object
    auth = get_twitter_auth()
    client = API(auth)
    return client
