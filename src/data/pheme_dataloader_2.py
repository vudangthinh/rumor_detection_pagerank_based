from os import listdir
from os.path import isdir, join
import json
import networkx as nx
from src.utils import text_utils, date_time_utils, graph_utils
import numpy as np
from nltk.util import ngrams

word_vectors = text_utils.load_pretrain_embedding('/data/glove.twitter/w2v.twitter.27B.100d.txt')
text_processor = text_utils.create_text_processor()

def load_data(data_path):
    graph_list = []
    y = []

    for f in listdir(data_path):
        topic_dir = join(data_path, f)
        if isdir(topic_dir):
            rumor_dir = join(topic_dir, 'rumours')
            non_rumor_dir = join(topic_dir, 'non-rumours')

            rumor_graph_list = read_topic_dir(rumor_dir)
            graph_list.extend(rumor_graph_list)
            y.extend([1 for i in range(len(rumor_graph_list))])

            non_rumor_graph_list = read_topic_dir(non_rumor_dir)
            graph_list.extend(non_rumor_graph_list)
            y.extend([0 for i in range(len(non_rumor_graph_list))])

    return (graph_list, y)

def read_topic_dir(topic_dir):
    graph_list = []
    for f in listdir(topic_dir):
        tweet_dir = join(topic_dir, f)
        if isdir(tweet_dir):
            DG = nx.DiGraph()

            structure_file = join(tweet_dir, 'structure.json')
            with open(structure_file) as json_f:
                structure_tree = json.load(json_f)
                recursive_struc(structure_tree, tweet_dir, True, f, -1, DG)

                graph_list.append(DG)

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
            text_vector = parse_tweet(file_path, True, source_time)
            DG.add_node(key, content=text_vector)
        else:
            file_path = join(tweet_dir, 'reactions', key + '.json')
            text_vector = parse_tweet(file_path, False, source_time)
            DG.add_node(key, content=text_vector)
            DG.add_edge(key, source_id)
    except FileNotFoundError as fnf_error:
        print(fnf_error)

    return source_time

def parse_tweet(file_path, is_source, source_time):
    with open(file_path) as file:
        data = json.load(file)
        text = data['text']
        text_vector = text_process(text)

        return text_vector

def text_process(s):
    tokens = text_utils.process(text_processor, s)

    s_embedding = np.zeros((word_vectors.vector_size, ))
    for token in tokens:
        token_embedding = text_utils.get_embedding(word_vectors, token)
        s_embedding = s_embedding + token_embedding

    if len(tokens) > 0:
        s_embedding = s_embedding / len(tokens)
    return s_embedding


if __name__ == '__main__':
    #test
    graph_list = read_topic_dir('/data/rumor_detection/data/pheme/pheme_v2_extend/all-rnr-annotated-threads/gurlitt-all-rnr-threads/rumours')
    for index, graph in enumerate(graph_list):
        for node in graph:
            print(node)
            break
        print(index, graph.size())
