from gensim.models import KeyedVectors
from src.data.pheme_dataloader_2 import load_data
from src.utils import graph_utils
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from src.utils import config

def build_data():
    graph_list, y = load_data(config.DATA_PATH)

    vector_list = []
    for i, graph in enumerate(graph_list):
        page_rank = graph_utils.pageranks(graph)
        i = 0
        for node, rank in page_rank.items():
            if i == 0:
                graph_vector = graph.nodes[node]['content'] * rank
                i += 1
            else:
                graph_vector += graph.nodes[node]['content'] * rank

        vector_list.append(graph_vector)

    X = np.vstack(vector_list)
    return X, y

if __name__ == '__main__':
    X, y = build_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
    clf = RandomForestClassifier(n_jobs=8, random_state=0)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1:", f1_score(y_test, y_pred))


