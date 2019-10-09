import tweepy
import pandas as pd
from datetime import datetime, timedelta, date

class MyEntryModel(status):
    """
    A Class Represents CSV Entry For Inserting to an External File
    """
    def __init__(self, status):
        user = status._json['user']
        location = user['location']
        location_city, location_province = '',''
        if location != '':
            location_split = location.split(', ')
            location_city = location_split[0]
            location_province = location_split[1]
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
        self.location_city = location_city
        self.location_province = location_province
        self.text = text.replace(';','')
    
    def to_entry(self):
        """
        Build a semicolon separated value string to be inserted to a csv file
        """
        return self.date + ';' + self.name + ';' + str(self.verified) + ';' + self.location_city + ';' + self.location_province + ';' + self.text

        

        