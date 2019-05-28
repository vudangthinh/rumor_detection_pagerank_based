import matplotlib.pyplot as plt
import networkx as nx

def draw(G):
    nx.draw(G)
    plt.show()

def pageranks(G):
    # personalization = {}
    # for node_name, node_content in G.nodes(data=True):
    #     personalization[node_name] = node_content['more_features'][8]
    #
    # total_count = sum(personalization.values())
    # personalization_normal = {}
    # for key, value in personalization.items():
    #     personalization_normal[key] = value/total_count

    pageranks = nx.pagerank(G, alpha=0.8)
    return pageranks

def extract_node_content(graph_list):
    tokens_list = []
    for graph in graph_list:
        for node_name, node_content in graph.nodes(data=True):
            tokens = node_content['content']
            tokens_list.append(tokens)

    return tokens_list