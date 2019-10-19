import tweepy
import time

# my auth credentials
import credentials

# my object models
from entry_model import MyCsvEntryModel

class TweetStreamer():
    """
    Class for streaming live tweets.
    """
    def stream_tweets(self, filename, tag_list, limit_entry, max_retries=1000):
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
        self.entry_count = 1
        self.limit_entry = limit_entry

    def on_status(self, status):
        entry = MyCsvEntryModel(status)

        if self.limit_entry == None:
            if (self.entry_count - 1) % 100 == 0:
                print('entry count: ' + str(self.entry_count) 
                    + ' | ' + entry.text[:60] 
                    + ' | length tweet: ' + str(len(entry.text)) 
                    + ' | on: ' + str(entry.date)
                    + ' | by: ' + str(entry.screen_name))
            
            extension = '_' + str(int(self.entry_count / 1000000)) + '.csv'
            
            try:
                data_store = self.filename + extension
                with open(data_store, 'a', encoding='utf-8') as io_data:
                    io_data.write(entry.to_entry() + '\n')
                self.entry_count = self.entry_count + 1
            except BaseException as e:
                print('Error on_status: %s' % str(e))
            return True

        elif self.entry_count <= self.limit_entry:
            print('entry count: ' + str(self.entry_count) 
                + ' | ' + entry.text[:60] 
                + ' | length tweet: ' + str(len(entry.text)) 
                + ' | on: ' + str(entry.date)
                + ' | by: ' + str(entry.screen_name))
            
            extension = '_' + str(int(self.entry_count / 1000000)) + '.csv'
            
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