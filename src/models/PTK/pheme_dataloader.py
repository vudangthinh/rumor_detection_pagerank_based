import os
from os import listdir
from os.path import isfile, isdir, join
import json
from treelib import Node, Tree
from src.models.PTK.utils import date_time_utils
from src.models.PTK.models.Tweet import Tweet
import numpy as np
import re
from nltk.util import ngrams

def read_data(data_path):

    for f in listdir(data_path):
        topic_dir = join(data_path, f)
        if isdir(topic_dir):
            rumor_dir = join(topic_dir, 'rumours')
            non_rumor_dir = join(topic_dir, 'non-rumours')
            read_topic_dir(rumor_dir, True)
            read_topic_dir(non_rumor_dir, False)


def read_topic_dir(topic_dir, is_rumor):
    for f in listdir(topic_dir):
        tweet_dir = join(topic_dir, f)
        if isdir(tweet_dir):
            tree = Tree()

            structure_file = join(tweet_dir, 'structure.json')
            with open(structure_file) as json_f:
                structure_tree = json.load(json_f)
                recursive_struc(structure_tree, tweet_dir, True, f, -1, tree)
                tree.show()

def recursive_struc(structure_tree, tweet_dir, source, source_id, source_time, tree):
    for key, value in structure_tree.items():
        if source and key != source_id:
            continue

        if type(value) is dict:
            # print(key, value)
            source_time = process_tweet(tweet_dir, key, source, source_time, source_id, tree)

            source_id_2 = key
            recursive_struc(value, tweet_dir, False, source_id_2, source_time, tree)
        else:
            process_tweet(tweet_dir, key, source, source_time, source_id, tree)

def process_tweet(tweet_dir, key, source, source_time, source_id, tree):
    try:
        if source:
            file_path = join(tweet_dir, 'source-tweets', key + '.json')
            ur, cr, source_time = parse_tweet(file_path, True, source_time)
            tr = 0
            tweet_obj = Tweet(ur, cr, tr, True)
            tree.create_node(key, key, data=tweet_obj)
        else:
            file_path = join(tweet_dir, 'reactions', key + '.json')
            uv, cv, tv = parse_tweet(file_path, False, source_time)
            tweet_obj = Tweet(uv, cv, tv, False)
            tree.create_node(key, key, parent=source_id, data=tweet_obj)
    except FileNotFoundError as fnf_error:
        print(fnf_error)

    return source_time

def parse_tweet(file_path, is_source, source_time):
    with open(file_path) as file:
        data = json.load(file)
        text = data['text']
        n_grams = text_process(text)

        user = data['user']
        verified = 1 if user['verified'] else 0
        followers_count = user['followers_count']
        friends_count = user['friends_count']
        statuses_count = user['statuses_count']

        user_vec = np.array([0 if friends_count == 0 else followers_count/friends_count, verified, statuses_count])

        created_at = data['created_at']
        timestamp = date_time_utils.convert_string_timestamp(created_at)
        if is_source:
            return (user_vec, n_grams, timestamp)
        else:
            time_dif = timestamp - source_time
            return (user_vec, n_grams, time_dif)

def text_process(s):
    s = s.lower()
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    tokens = [token for token in s.split(" ") if token != ""]
    n_grams = set.union(set(ngrams(tokens, 1)), set(ngrams(tokens, 2)))
    return n_grams


if __name__ == '__main__':
    #test
    read_topic_dir('/data/rumor_detection/data/pheme/pheme_v2_extend/all-rnr-annotated-threads/charliehebdo-all-rnr-threads/rumours', True)