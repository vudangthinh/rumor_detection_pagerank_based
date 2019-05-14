from os import listdir
from os.path import isdir, join
import json
import networkx as nx
from src.utils import text_utils, date_time_utils, graph_utils
import numpy as np
from nltk.util import ngrams
from src.utils import config

text_processor = text_utils.create_text_processor()

def load_data(data_path, data_version):
    graph_dict = {}

    pheme_v1_topics = ['charliehebdo-all-rnr-threads', 'ferguson-all-rnr-threads', 'germanwings-crash-all-rnr-threads', 'ottawashooting-all-rnr-threads', 'sydneysiege-all-rnr-threads']

    for f in listdir(data_path):
        if data_version == 'v2' or (data_version == 'v1' and f in pheme_v1_topics):
            topic_dir = join(data_path, f)
            if isdir(topic_dir):
                rumor_dir = join(topic_dir, 'rumours')
                non_rumor_dir = join(topic_dir, 'non-rumours')

                graph_list = read_topic_dir(rumor_dir, label=1)
                graph_list.extend(read_topic_dir(non_rumor_dir, label=0))
                graph_dict[f] = graph_list

    return graph_dict

def read_topic_dir(topic_dir, label):
    graph_list = []
    for f in listdir(topic_dir):
        tweet_dir = join(topic_dir, f)
        if isdir(tweet_dir):
            DG = nx.DiGraph()

            structure_file = join(tweet_dir, 'structure.json')
            with open(structure_file) as json_f:
                structure_tree = json.load(json_f)
                recursive_struc(structure_tree, tweet_dir, True, f, -1, DG)

                graph_list.append((DG, label))

    return graph_list

def recursive_struc(structure_tree, tweet_dir, source, source_id, source_time, DG):
    for key, value in structure_tree.items():
        if source and key != source_id:
            continue

        if type(value) is dict:
            source_time = process_tweet(tweet_dir, key, source, source_time, source_id, DG)

            source_id_2 = key
            recursive_struc(value, tweet_dir, False, source_id_2, source_time, DG)
        else:
            process_tweet(tweet_dir, key, source, source_time, source_id, DG)

def process_tweet(tweet_dir, key, source, source_time, source_id, DG):
    try:
        if source:
            file_path = join(tweet_dir, 'source-tweets', key + '.json')
            tokens, more_features = parse_tweet(file_path, True, source_time)
            DG.add_node(key, content=tokens, more_features=more_features)
        else:
            file_path = join(tweet_dir, 'reactions', key + '.json')
            tokens, more_features = parse_tweet(file_path, False, source_time)
            DG.add_node(key, content=tokens, more_features=more_features)
            DG.add_edge(key, source_id)
    except FileNotFoundError as fnf_error:
        print(fnf_error)

    return source_time

def parse_tweet(file_path, is_source, source_time):
    with open(file_path) as file:
        data = json.load(file)
        text = data['text']
        tokens = text_process(text)

        capital_ratio = len([c for c in text if c.isupper()]) / len(text)
        word_count = len(tokens)
        question_mark = 1 if "?" in text else 0
        exclamation_mark = 1 if "!" in text else 0
        period_mark = 1 if "." in text else 0
        favorite_count = data['favorite_count']
        retweet_count = data['retweet_count']
        more_features = np.array([capital_ratio, word_count, question_mark, exclamation_mark, period_mark, favorite_count, retweet_count])

        return tokens, more_features

def text_process(s):
    tokens = text_utils.process(text_processor, s)
    return tokens

if __name__ == '__main__':
    #test
    graph_list = read_topic_dir('/data/rumor_detection/data/pheme/pheme_v2_extend/all-rnr-annotated-threads/gurlitt-all-rnr-threads/rumours')
    for index, graph in enumerate(graph_list):
        for node in graph:
            print(node)
            break
        print(index, graph.size())
