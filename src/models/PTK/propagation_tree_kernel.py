import numpy as np

def node_similarity(v1, v2):
    c1, t1 = v1
    c2, t2 = v2

    t = abs(t1 - t2)
    content_similarity = len(set.intersection(c1, c2)) / len(set.union(c1, c2))
    return np.exp(-t) * content_similarity

def most_similarity_node(T1, T2):
    pass