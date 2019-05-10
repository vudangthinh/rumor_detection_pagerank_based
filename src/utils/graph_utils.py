import matplotlib.pyplot as plt
import networkx as nx

def draw(G):
    nx.draw(G)
    plt.show()

def pageranks(G):
    pageranks = nx.pagerank(G)
    return pageranks

def extract_node_content(graph_list):
    tokens_list = []
    for graph in graph_list:
        for node_name, node_content in graph.nodes(data=True):
            tokens = node_content['content']
            tokens_list.append(tokens)

    return tokens_list