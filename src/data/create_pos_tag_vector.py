import sys
sys.path.append('/data/rumor_detection/rumor_detection')
import json
from os import listdir
from os.path import isdir, join, isfile

from nltk.tag.stanford import StanfordPOSTagger

from src.utils import config
from src.utils import text_utils

text_processor = text_utils.create_text_processor()
stanford_tagger = StanfordPOSTagger(
            model_filename='../../libs/stanford_postagger/models/english-bidirectional-distsim.tagger',
            path_to_jar='../../libs/stanford_postagger/stanford-postagger.jar')
writer = open('../../data/interim/tweet_pos_tag.txt', 'w')

def load_data(data_path):

    for f in listdir(data_path):
        topic_dir = join(data_path, f)
        if isdir(topic_dir):
            rumor_dir = join(topic_dir, 'rumours')
            non_rumor_dir = join(topic_dir, 'non-rumours')

            read_topic_dir(rumor_dir)
            read_topic_dir(non_rumor_dir)


def read_topic_dir(topic_dir):
    for f in listdir(topic_dir):
        tweet_dir = join(topic_dir, f)
        if isdir(tweet_dir):

            tweet_file = join(tweet_dir, 'source-tweets', f + '.json')
            read_tweet(tweet_file, f)
            for f1 in listdir(join(tweet_dir, 'reactions')):
                if isfile(f1) and f1[0] != '.':
                    tweet_file = join(tweet_dir, 'reactions', f1)
                    read_tweet(tweet_file, f1.split('.')[0])

def read_tweet(tweet_file, id):
    with open(tweet_file) as json_f:
        tweet_data = json.load(json_f)
        tweet_text = tweet_data['text']
        tokens = text_process(tweet_text)

        pos_tags = text_utils.convert_pos_tag(stanford_tagger, tokens)
        output_str = str(id)
        for tag in pos_tags:
            output_str += '\t' + str(tag)
        writer.write(output_str + '\n')


def text_process(s):
    tokens = text_utils.process(text_processor, s)

    return tokens

if __name__ == '__main__':
    load_data(config.DATA_PATH)
    writer.close()
