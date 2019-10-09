import tweepy
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np

# my auth credentials
import credentials

# my object models
import entry_model

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # TODO: process the statusses
        return True
        
    def on_error(self, status_code):
        print(status_code)

if __name__ == "__main__":

    litener = MyStreamListener()

    auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    
    api = tweepy.API(auth)