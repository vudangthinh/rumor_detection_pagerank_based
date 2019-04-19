import tweepy
from pprint import pprint
from os import listdir
from os.path import isfile, join

consumer_key = '9TvVKS8HRroMN4wQtBdzNA'
consumer_secret = 'BrmSzXi4sGzDiRdj7kbPHMRLQNMkbpHeDqtLhWPhU'
access_token = '1287392767-m7gcpy3wkpNpvMpywC9wwBTzIivWVXvLabhZMlA'
access_token_secret = 'RHNCzFoLOpUHZhLQu7mDkJGsgtA3xtpKm35596ZfuRY'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

data_dir = '/data/rumor_detection/data/rumor_acl/rumor_detection_acl2017/twitter15/tree'

def process():
    for f in listdir(data_dir):
        file_path = join(data_dir, f)
        if isfile(file_path):
            crawl_file(file_path)

def crawl_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            pass

if __name__ == '__main__':
    process()