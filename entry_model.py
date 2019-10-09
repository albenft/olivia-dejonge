import tweepy
import pandas as pd
from datetime import datetime, timedelta, date

class MyCsvEntryModel(tweepy.Status):
    """
    A Class Represents CSV Entry For Inserting to an External File
    """
    def __init__(self, status):
        user = status._json['user']
        location = user['location']
        string_time = status._json['created_at']
        date = datetime.strptime(string_time, '%a %b %d %H:%M:%S %z %Y')

        text = ''
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = status.retweeted_status.text
        else:
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text
        
        self.date = datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
        self.name = user['name']
        self.verified = 1 if user['verified'] == True else 0
        self.location = location if location != None else ''
        self.text = text.replace(';','').replace('\n',' ').replace('  ',' ')
    
    def to_entry(self):
        """
        Build a semicolon separated value string to be inserted to a csv file
        """
        return self.date + ';' + self.name + ';' + str(self.verified) + ';' + self.location + ';' + self.text

        

        