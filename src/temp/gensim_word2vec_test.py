import gensim
import os
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
import gensim.downloader as api
# os.environ['PYTHONHASHSEED'] = '0'
tweet_tokens = []

with open('/data/rumor_detection/rumor_detection/data/interim/source_tweets.txt', 'r') as file:
    for line in file:
        tweet_tokens.append(line.split(' '))

model = gensim.models.Word2Vec(tweet_tokens, size=300, window=10, min_count=5, iter=10, workers=1, seed=42)
model.wv.save_word2vec_format('./embed_2.txt', binary=False)
