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
    text_list = []
    y = []

    for f in listdir(data_path):
        topic_dir = join(data_path, f)
        if isdir(topic_dir):
            rumor_dir = join(topic_dir, 'rumours')
            non_rumor_dir = join(topic_dir, 'non-rumours')

            rumor_tree_list = read_topic_dir(rumor_dir)
            text_list.extend(rumor_tree_list)
            y.extend([1 for i in range(len(rumor_tree_list))])

            non_rumor_tree_list = read_topic_dir(non_rumor_dir)
            text_list.extend(non_rumor_tree_list)
            y.extend([0 for i in range(len(non_rumor_tree_list))])

    return (text_list, y)

def read_topic_dir(topic_dir):
    text_list = []
    for f in listdir(topic_dir):
        tweet_dir = join(topic_dir, f)
        if isdir(tweet_dir):

            tweet_file = join(tweet_dir, 'source-tweets', f + '.json')
            with open(tweet_file) as json_f:
                tweet_data = json.load(json_f)
                tweet_text = tweet_data['text']
                tokens = text_process(tweet_text)

                text_list.append(tokens)

    return text_list

def text_process(s):
    tokens = text_utils.process(text_processor, s)

    return tokens


if __name__ == '__main__':
    #test
    tree_list = read_topic_dir('/Users/thinhvu/Documents/projects/6392078/all-rnr-annotated-threads/gurlitt-all-rnr-threads/rumours')
    for tree in tree_list:
        tree.show()
        tree.show(data_property='user')
