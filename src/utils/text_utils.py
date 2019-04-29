import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons
from gensim.models import KeyedVectors


def create_text_processor():
    text_processor = TextPreProcessor(
            normalize=['url', 'email', 'percent', 'money', 'phone', 'user',
                       'time', 'url', 'date', 'number'],
            fix_html=True,
            segmenter="twitter",
            corrector="twitter",

            unpack_hashtags=True,
            unpack_contractions=True,
            spell_correct_elong=True,

            # tokenizer=SocialTokenizer(lowercase=True).tokenize,
            tokenizer=RegexpTokenizer(r'\w+').tokenize,

            dicts=[emoticons]
        )

    return text_processor

def remove_stopword(tokens):
    stop_words = stopwords.words('english')
    return [word for word in tokens if word not in stop_words]

def lower_case(text):
    return text.lower()

def process(text_processor, text):
    text = text.replace("\/", '/')
    text = text.lower()

    tokens = text_processor.pre_process_doc(text)
    tokens = remove_stopword(tokens)
    return tokens

def convert_ngram(tokens, n=1):
    if n==1:
        return set(tokens)

    if n==2:
        n_grams = set()
        for i in range(len(tokens) - 1):
            s = tokens[i] + " " + tokens[i + 1]
            n_grams.add(s)

        return n_grams

def load_pretrain_embedding(path):
    word_vectors = KeyedVectors.load_word2vec_format(path, binary=False)
    return word_vectors

def get_embedding(word_vectors, token):
    if token in word_vectors:
        return word_vectors[token]
    else:
        return np.zeros((word_vectors.vector_size, ))


if __name__ == '__main__':
    text = '#WakeUpAmerica \nCo-pilot was a Muslim Convert \nhttp:\/\/t.co\/RYFQTVBYBL\n@seanhannity @greta @act4america \n@KrisParonto @JGilliam_SEAL Feb 18th'
    text = 'BREAKING: German Media Site   Says \tGermanwings Co-Pilot Was Muslim Convert http:\/\/t.co\/bTKvcLMN60 via @anyclinic'
    tokens = process(text)
    print(tokens)

    print(convert_ngram(tokens, 1))
    print(convert_ngram(tokens, 2))