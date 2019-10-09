import tweepy
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np

# my auth credentials
import credentials

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # TODO: process the statusses
        return True
        
    def on_error(self, status_code):
        print(status_code)