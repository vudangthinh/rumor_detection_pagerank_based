from os import listdir
from os.path import isdir, join
import json
from treelib import Tree
from src.data.Tweet import Tweet
from src.utils import text_utils, date_time_utils
import numpy as np
from nltk.util import ngrams

text_processor = text_utils.create_text_processor()

def load_data(data_path):
    tree_list = []
    y = []

    for f in listdir(data_path):
        topic_dir = join(data_path, f)
        if isdir(topic_dir):
            rumor_dir = join(topic_dir, 'rumours')
            non_rumor_dir = join(topic_dir, 'non-rumours')

            rumor_tree_list = read_topic_dir(rumor_dir)
            tree_list.extend(rumor_tree_list)
            y.extend([1 for i in range(len(rumor_tree_list))])

            non_rumor_tree_list = read_topic_dir(non_rumor_dir)
            tree_list.extend(non_rumor_tree_list)
            y.extend([0 for i in range(len(non_rumor_tree_list))])

    return (tree_list, y)

def read_topic_dir(topic_dir):
    tree_list = []
    for f in listdir(topic_dir):
        tweet_dir = join(topic_dir, f)
        if isdir(tweet_dir):
            tree = Tree()

            structure_file = join(tweet_dir, 'structure.json')
            with open(structure_file) as json_f:
                structure_tree = json.load(json_f)
                recursive_struc(structure_tree, tweet_dir, True, f, -1, tree)

                tree_list.append(tree)

    return tree_list

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
    # tokens = text_utils.process(text_processor, s)
    # return set.union(text_utils.convert_ngram(tokens, 1), text_utils.convert_ngram(tokens, 2))

    s = text_utils.lower_case(s)
    # s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    tokens = [token for token in s.split(" ") if token != ""]
    # n_grams = set.union(set(ngrams(tokens, 1)), set(ngrams(tokens, 2)))
    n_grams = set(ngrams(tokens, 1))
    return n_grams


if __name__ == '__main__':
    #test
    tree_list = read_topic_dir('/Users/thinhvu/Documents/projects/6392078/all-rnr-annotated-threads/gurlitt-all-rnr-threads/rumours')
    for tree in tree_list:
        tree.show()
        tree.show(data_property='user')
