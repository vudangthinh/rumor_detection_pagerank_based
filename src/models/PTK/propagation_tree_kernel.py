import numpy as np
from treelib import Node, Tree

def node_similarity(node1, node2, alpha=0.5):
    u1, c1, t1 = node1.data.user, node1.data.content, node1.data.time_dif
    u2, c2, t2 = node2.data.user, node2.data.content, node2.data.time_dif

    t = abs(t1 - t2)
    user_similarity = np.linalg.norm(u1 - u2)
    content_similarity = len(set.intersection(c1, c2)) / len(set.union(c1, c2))
    return np.exp(-t) * (alpha * user_similarity + (1 - alpha) * content_similarity)

def most_similarity_nodes(T1, T2):
    node_pairs = {}

    for node1 in T1.all_nodes_itr():
        smallest_dist = -1
        similar_node = Node()
        for node2 in T2.all_nodes_itr():
            node_simil = node_similarity(node1, node2)
            if smallest_dist < 0 or smallest_dist > node_simil:
                smallest_dist = node_simil
                similar_node = node2

        node_pairs[node1] = similar_node

    return node_pairs

def similarity_sub_tree(subtree1, subtree2):
    root_similar = node_similarity(subtree1.root, subtree2.root)
    if subtree1.depth() == 0 and subtree2.depth() == 0:
        return root_similar
    else:
        nc1 = subtree1.size() - 1
        nc2 = subtree2.size() - 1
        nc_min = min(nc1, nc2)

        children1 = subtree1.children(subtree1.root)
        children2 = subtree2.children(subtree2.root)

        multiplication = 1
        for i in range(nc_min):
            child1 = children1[i]
            child2 = children2[i]
            child_tree1 = subtree1.subtree(child1.identifier)
            child_tree2 = subtree2.subtree(child2.identifier)

            child_similar = similarity_sub_tree(child_tree1, child_tree2)
            multiplication *= (1 + child_similar)

        return root_similar * multiplication


def propagation_tree_kernel_function(T1, T2):
    node_pairs_1 = most_similarity_nodes(T1, T2)

    tree_similarity = 0
    for node1, node2 in node_pairs_1.items():
        subtree1 = T1.subtree(node1.identifier)
        subtree2 = T2.subtree(node2.identifier)
        tree_similarity += similarity_sub_tree(subtree1, subtree2)

    node_pairs_2 = most_similarity_nodes(T2, T1)
    for node2, node1 in node_pairs_2.items():
        subtree1 = T1.subtree(node1.identifier)
        subtree2 = T2.subtree(node2.identifier)
        tree_similarity += similarity_sub_tree(subtree1, subtree2)

    return tree_similarity

def