import nltk
from nltk.corpus import stopwords
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons



def remove_stopword(tokens):
    stop_words = stopwords.words('english')
    return [word for word in tokens if word not in stop_words]

def lower_case(text):
    return text.lower()

def process(text):
    text = lower_case(text)
