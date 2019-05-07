import argparse
from gensim.models import KeyedVectors
from gensim.models.doc2vec import Doc2Vec
from src.data.pheme_dataloader_pagerank import load_data
from src.utils import graph_utils
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from src.utils import config, text_utils
from sklearn.feature_extraction.text import TfidfVectorizer

parser = argparse.ArgumentParser()
parser.add_argument('--embed', default=True, action='store_false', help='type of embedding model')
parser.add_argument('--tfidf', default=True, action='store_false', help='use tfidf score to weight word vector')
opt = parser.parse_args()

w2v_model = opt.embed
use_tfidf = opt.tfidf
print(w2v_model, use_tfidf)

if w2v_model:
    embed_model = text_utils.load_pretrain_embedding(config.EMBEDDING_FILE)
else:
    embed_model = Doc2Vec.load(config.D2V_FILE)


def build_data():
    graph_list, y = load_data(config.DATA_PATH)
    if use_tfidf:
        tfidf = train_tfidf(graph_list)
    else:
        tfidf = None

    vector_list = []
    for i, graph in enumerate(graph_list):
        vector_list.append(get_graph_vector(graph, tfidf, w2v_model))

    X = np.vstack(vector_list)
    return X, y

def train_tfidf(graph_list):
    tokens_list = []
    for graph in graph_list:
        for node_name, node_content in graph.nodes(data=True):
            tokens = node_content['content']
            tokens_list.append(tokens)

    tfidf = TfidfVectorizer(analyzer=lambda x: x)
    tfidf.fit(tokens_list)
    return tfidf

def get_graph_vector(graph, tfidf, w2v):
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
    X, y = build_data()
    np.savez('../../../data/processed/train_data', x=X, y=y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
    clf = RandomForestClassifier(n_jobs=8, random_state=0)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Acc: {:.3f} P: {:.3f} R: {:.3f} F1: {:.3f}".format(accuracy_score(y_test, y_pred), precision_score(y_test, y_pred), recall_score(y_test, y_pred), f1_score(y_test, y_pred)))


