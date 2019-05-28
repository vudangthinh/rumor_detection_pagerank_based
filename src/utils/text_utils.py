import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons
from gensim.models import KeyedVectors, Word2Vec


pen_treebank_tagset = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'IN/that', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NP',
                       'NPS', 'PDT', 'POS', 'PP', 'PP$', 'RB', 'RBR', 'RBS', 'RP', 'SENT', 'SYM', 'TO', 'UH', 'VB', 'VBD',
                       'VBG', 'VBN', 'VBP', 'VBZ', 'VH', 'VHD', 'VHG', 'VHN', 'VHP', 'VHZ', 'VV', 'VVD', 'VVG', 'VVN',
                       'VVP', 'VVZ', 'WDT', 'WP', 'WP$', 'WRB', '#', '$', '“', '``', '(', ')', ',', ':']

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

def remove_last_url(tokens):
    if len(tokens) > 0 and tokens[-1] == 'url':
        return tokens[:-1]
    else:
        return tokens

def process(text_processor, text):
    text = text.replace("\/", '/')
    text = text.lower()

    tokens = text_processor.pre_process_doc(text)
    tokens = remove_stopword(tokens)
    # tokens = remove_last_url(tokens)
    return tokens

def convert_pos_tag(stanford_tagger, tokens):
    pos_vec = np.zeros((len(pen_treebank_tagset)))

    tag_list = stanford_tagger.tag(tokens)
    for token, tag in tag_list:
        if tag in pen_treebank_tagset:
            pos_vec[pen_treebank_tagset.index(tag)] += 1

    return pos_vec

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
    # word_vectors = Word2Vec.load(path)
    return word_vectors

def get_embedding(word_vectors, token):
    if token in word_vectors:
        return word_vectors[token]
    else:
        return np.zeros((word_vectors.vector_size, ))

def load_pos_tag(pos_tag_file):
    tweet_pos_tag_dict = {}
    with open(pos_tag_file, 'r') as file:
        for line in file:
            line_arr = line.split('\t')
            pos_tag = []
            for value in line_arr[1:len(line_arr)]:
                pos_tag.append(float(value))

            tweet_pos_tag_dict[line_arr[0]] = np.array(pos_tag)

    return tweet_pos_tag_dict

if __name__ == '__main__':
    text = '#WakeUpAmerica \nCo-pilot was a Muslim Convert \nhttp:\/\/t.co\/RYFQTVBYBL\n@seanhannity @greta @act4america \n@KrisParonto @JGilliam_SEAL Feb 18th'
    text = 'BREAKING: German Media Site   Says \tGermanwings Co-Pilot Was Muslim Convert http:\/\/t.co\/bTKvcLMN60 via @anyclinic'
    tokens = process(text)
    print(tokens)

    print(convert_ngram(tokens, 1))
    print(convert_ngram(tokens, 2))