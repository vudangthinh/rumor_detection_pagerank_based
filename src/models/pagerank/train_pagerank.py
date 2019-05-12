import argparse
from gensim.models import KeyedVectors
from gensim.models.doc2vec import Doc2Vec
from src.data.pheme_dataloader_pagerank import load_data
from src.utils import graph_utils
from src.models.w2v import train_w2v
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from src.utils import config, text_utils
from sklearn.feature_extraction.text import TfidfVectorizer

parser = argparse.ArgumentParser()
parser.add_argument('--data', default='v1', help='version of PHEME dataset')
parser.add_argument('--train_type', default='cv', help='type of training model: cross-validation or train-test-split')
parser.add_argument('--embed_type', default=True, action='store_false', help='type of embedding model: word2vec or doc2vec')
parser.add_argument('--embed_retrain', default=False, action='store_true', help='will retrain embedding model')
parser.add_argument('--embed_update', default=False, action='store_true', help='will retrain embedding model')
parser.add_argument('--embed_file', default=config.EMBEDDING_FILE, help='path to embedding file')
parser.add_argument('--tfidf', default=False, action='store_true', help='use tfidf score to weight word vector')
opt = parser.parse_args()

embed_type = opt.embed_type
use_tfidf = opt.tfidf
embed_retrain = opt.embed_retrain
embed_update = opt.embed_update
embed_file = opt.embed_file
data_version = opt.data
train_type = opt.train_type
print("Word2vec: {}\nTFIDF: {}\nEmbed File: {}\nEmbed Retrain: {}\nEmbed Update: {}\nData Version: {}\nTrain Type: {}"
      .format(embed_type, use_tfidf, embed_file, embed_retrain, embed_update, data_version, train_type))

if not embed_retrain:
    if embed_type :
        embed_model = text_utils.load_pretrain_embedding(embed_file)
    else:
        embed_model = Doc2Vec.load(config.D2V_FILE)


def process():
    scores = []
    graph_dict = load_data(config.DATA_PATH, data_version)

    if train_type == 'cv':
        topics = list(graph_dict.keys())
        kf = KFold(n_splits=5, random_state=42, shuffle=True)
        for train_index, test_index in kf.split(topics):
            print('------')
            train_graph_list = []
            test_graph_list = []
            y_train = []
            y_test = []

            for i in train_index:
                topic = topics[i]
                train_graph_list.extend([x for (x, _) in graph_dict[topic]])
                y_train.extend([y for (_, y) in graph_dict[topic]])

            for i in test_index:
                topic = topics[i]
                print(topic)
                test_graph_list.extend([x for (x, _) in graph_dict[topic]])
                y_test.extend([y for (_, y) in graph_dict[topic]])

            scores.append(train_model(train_graph_list, y_train, test_graph_list, y_test))

        print('CV Scores:', scores)
        acc = 0
        p = 0
        r = 0
        f1 = 0
        for x, y, z, t in scores:
            acc += x
            p += y
            r += z
            f1 += t
        acc, p, r, f1 = acc / len(scores), p / len(scores), r / len(scores), f1 / len(scores)

    else:
        graph_list = []
        y = []
        for key, value in graph_dict.items():
            graph_list.extend([x for (x, _) in value])
            y.extend([y for (_, y) in value])

        train_graph_list, test_graph_list, y_train, y_test = train_test_split(graph_list, y, test_size=0.3, random_state=config.RANDOM_STATE)
        acc, p, r, f1 = train_model(train_graph_list, y_train, test_graph_list, y_test)

    print("Acc: {:.3f} P: {:.3f} R: {:.3f} F1: {:.3f}".format(acc, p, r, f1))

def train_model(train_graph_list, y_train, test_graph_list, y_test):
    if use_tfidf:
        tfidf = train_tfidf(train_graph_list)
    else:
        tfidf = None

    if embed_retrain:
        tokens_list = graph_utils.extract_node_content(train_graph_list)
        embed_model_retrain = train_w2v.direct_train_w2v(tokens_list)

    train_vector_list = []
    for i, graph in enumerate(train_graph_list):
        if embed_retrain:
            train_vector_list.append(get_graph_vector(graph, tfidf, embed_type, embed_model_retrain))
        else:
            train_vector_list.append(get_graph_vector(graph, tfidf, embed_type, embed_model))

    X_train = np.vstack(train_vector_list)

    if embed_update:
        embed_model_update = train_w2v.update_model(embed_model_retrain, graph_utils.extract_node_content(test_graph_list))

    test_vector_list = []
    for i, graph in enumerate(test_graph_list):
        if embed_update:
            test_vector_list.append(get_graph_vector(graph, tfidf, embed_type, embed_model_update))
        else:
            test_vector_list.append(get_graph_vector(graph, tfidf, embed_type, embed_model))

    X_test = np.vstack(test_vector_list)

    clf = RandomForestClassifier(n_estimators=200, n_jobs=8, random_state=0)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    return (accuracy_score(y_test, y_pred), precision_score(y_test, y_pred), recall_score(y_test, y_pred), f1_score(y_test, y_pred))

def train_tfidf(graph_list):
    tokens_list = graph_utils.extract_node_content(graph_list)

    tfidf = TfidfVectorizer(analyzer=lambda x: x)
    tfidf.fit(tokens_list)
    return tfidf

def get_graph_vector(graph, tfidf, w2v, embed_model):
    graph_vector = np.zeros((embed_model.vector_size))
    page_rank = graph_utils.pageranks(graph)
    for node, rank in page_rank.items():
        tokens = graph.nodes[node]['content']

        if w2v:
            node_vector = np.zeros((embed_model.vector_size,))
            for token in tokens:
                if tfidf:
                    token_embedding = text_utils.get_embedding(embed_model, token) * tfidf.idf_[tfidf.vocabulary_[token]]
                else:
                    token_embedding = text_utils.get_embedding(embed_model, token)

                node_vector = node_vector + token_embedding

            if len(tokens) > 0:
                node_vector = node_vector / len(tokens)
        else:
            node_vector = embed_model.infer_vector(tokens)

        graph_vector += node_vector * rank

    return graph_vector

if __name__ == '__main__':
    process()
    # X, y = build_data()
    # np.savez('../../../data/processed/train_data', x=X, y=y)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=config.RANDOM_STATE)
    # clf = RandomForestClassifier(n_estimators=200, n_jobs=8, random_state=0)
    # clf.fit(X_train, y_train)
    # y_pred = clf.predict(X_test)
    # print("Acc: {:.3f} P: {:.3f} R: {:.3f} F1: {:.3f}".format(accuracy_score(y_test, y_pred), precision_score(y_test, y_pred), recall_score(y_test, y_pred), f1_score(y_test, y_pred)))


