from datetime import datetime, timedelta, date
from streamer import TweetStreamer

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