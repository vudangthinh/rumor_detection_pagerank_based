import nltk
from nltk.corpus import stopwords


def remove_stopword(tokens):
    stop_words = stopwords.words('english')
    return [word for word in tokens if word not in stop_words]


def process(text):
    pass