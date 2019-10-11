import tweepy
from datetime import datetime, timedelta, date
import time
import sys

# my auth credentials
import credentials

# my object models
from entry_model import MyCsvEntryModel

class TweetStreamer():
    """
    Class for streaming live tweets.
    """
    def stream_tweets(self, filename, tag_list, limit_entry, max_retries=10):
        retry = 0

        listener = SaveFileListener(filename, limit_entry)
        auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        last_entry_count = listener.entry_count
        terminated_by_max_retries = True

        while retry < max_retries:
            listener.entry_count = last_entry_count
            try:
                stream = tweepy.Stream(auth = api.auth, listener = listener)
                completed = not stream.filter(track=tag_list)
                if completed:
                    terminated_by_max_retries = False
                    retry = max_retries
                
            except Exception as e:
                print('Error occured: %s' % str(e))
                last_entry_count = listener.entry_count
                retry = retry + 1
                print('Retry again in 5 seconds...')
                time.sleep(5)
            
        if terminated_by_max_retries:
            print('Maximum retries exceeded.')
        

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
            print('entry count: ' + str(self.entry_count) 
                + ' | ' + entry.text[:60] 
                + ' | length tweet: ' + str(len(entry.text)) 
                + ' | on: ' + str(entry.date)
                + ' | by: ' + str(entry.screen_name))
            
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
    max_retries = 10

    # print('Input tag to stream: ')
    tags = input('Input tag to stream: ')
    while not tags:
        print('Tag(s) field is required!')
        tags = input('Input tag to stream: ')
    for tag in tags.split(','):
            tag_list.append(tag)
    
    name = input('Input filename to save result: ')
    while not name:
        print('Filename field is required!')
        name = input('Input filename to save result: ')
    filename = filename + name

    entry = input('Input limit tweets to stream (leave blank for default=200): ')
    if entry != '':
        entry = int(entry)
        limit_entry = entry
    
    retries = input('Input maximum number of retry to attempt when error occured (leave blank for default=10): ')
    if retries != '':
        retries = int(retries)
        max_retries = retries

    start_time = datetime.now()
    print('Stream started at: ' + start_time.strftime('%Y-%m-%d %H:%M:%S'))

    tweet_streamer = TweetStreamer()
    tweet_streamer.stream_tweets(filename, tag_list, limit_entry)

    end_time = datetime.now()
    duration = end_time - start_time

    print('Stream started at: ' + start_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('Stream ended at: ' + end_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('Stream done in: ' + str(duration))