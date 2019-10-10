import tweepy
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import time

# my auth credentials
import credentials

# my object models
from entry_model import MyCsvEntryModel

class TweetStreamer():
    """
    Class for stream live tweets.
    """
    def stream_tweets(self, filename, tag_list, limit_entry):
        listener = SaveFileListener(filename, limit_entry)
        auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        stream = tweepy.Stream(auth = api.auth, listener = listener)
        stream.filter(track=tag_list)

class SaveFileListener(tweepy.StreamListener):
    """
    Basic streamer class which saves the results on an external.
    """
    def __init__(self, filename, limit_entry):
        super(SaveFileListener, self).__init__()
        self.filename = filename
        self.entry_count = 0
        self.limit_entry = limit_entry

    def on_status(self, status):
        entry = MyCsvEntryModel(status)
        if self.entry_count <= self.limit_entry:
            print('entry count: ' + str(self.entry_count) + ' | ' + str(entry.text[:80]))
            extension = '_' + str(int(self.entry_count / 10000)) + '.csv'
            
            try:
                data_store = self.filename + extension
                with open(data_store, 'a', encoding='utf-8') as io_data:
                    io_data.write(entry.to_entry() + '\n')
                self.entry_count = self.entry_count + 1
            except BaseException as e:
                print('Error on_status: %s' % str(e))
            return True
        else:
            return False
        
    def on_error(self, status_code):
        print(status_code)

if __name__ == "__main__":

    tag_list = []
    filename = 'target/'
    limit_entry = 200

    # print('Input tag to stream: ')
    tags = input('Input tag to stream: ').split(',')
    for tag in tags:
        tag_list.append(tag)
    
    name = input('Input file name to save result: ')
    filename = filename + name

    entry = input('Input limit tweets to stream: ')
    if entry != None:
        entry = int(entry)
        limit_entry = entry

    start_time = datetime.now()
    print('Stream started at: ' + start_time.strftime('%Y-%m-%d %H:%M:%S'))

    tweet_streamer = TweetStreamer()
    tweet_streamer.stream_tweets(filename, tag_list, limit_entry)

    end_time = datetime.now()
    duration = end_time - start_time

    print('Stream started at: ' + start_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('Stream ended at: ' + end_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('Stream done in: ' + str(duration))