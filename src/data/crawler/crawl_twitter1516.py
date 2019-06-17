from os import listdir
from os.path import isfile, join
from src.data.crawler import twitter_crawler

data_dir_15 = '/data/rumor_detection/data/rumor_acl/rumor_detection_acl2017/twitter15/tree'
output_dir_15 = '/data/rumor_detection/data/rumor_acl/rumor_detection_acl2017/twitter15/tweet_contents.txt'
data_dir_16 = '/data/rumor_detection/data/rumor_acl/rumor_detection_acl2017/twitter16/tree'

api = twitter_crawler.create_api()
writer = open(output_dir_15, 'w')

def process(data_dir):
    for f in listdir(data_dir):
        file_path = join(data_dir, f)

        if isfile(file_path) and '.txt' in file_path:
            crawl_file(file_path)

def crawl_file(file_path):
    tweet_ids = set()
    with open(file_path, 'r') as file:
        for line in file:
            line_arr = line.split("'")
            user1 = line_arr[1]
            tweet1 = line_arr[3]
            user2 = line_arr[7]
            tweet2 = line_arr[9]

            tweet_ids.add(tweet1)
            tweet_ids.add(tweet2)

    result = twitter_crawler.get_tweet_content(api, tweet_ids)
    for id, text in result:
        text = " ".join(text.split())
        writer.write(id + '\t' + text + '\n')


if __name__ == '__main__':
    process(data_dir_15)
    writer.close()