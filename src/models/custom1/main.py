from gensim.models import KeyedVectors


if __name__ == '__main__':
    word_vectors = KeyedVectors.load_word2vec_format('/data/glove.twitter/w2v.twitter.27B.100d.txt', binary=False)


