import matplotlib.pyplot as plt
import networkx as nx
import math

def draw(G):
    nx.draw(G)
    plt.show()

def graph_centrality(G, type):
    if type == 'pagerank':
        return pageranks(G)
    elif type == 'degree':
        return degree_centrality(G)
    elif type == 'closeness':
        return closeness_centrality(G)
    elif type == 'eigenvector':
        return eigenvector_centrality(G)
    elif type == 'betweenness':
        return betweenness_centrality(G)
    elif type == 'average':
        return average_centrality(G)
    elif type == 'voterank':
        return voterank_centrality(G)
    elif type == 'harmonic':
        return harmonic_centrality(G)
    elif type == 'secondorder':
        return second_order_centrality(G)
    elif type == 'percolation':
        return percolation_centrality(G)
    elif type == 'time':
        return time_centrality(G)

def average_centrality(G):
    centrality = {}
    for node, _ in G.nodes(data=True):
        centrality[node] = 1.0

    return normalize(centrality)

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

def degree_centrality(G):
    node_degree_centrality = nx.degree_centrality(G)
    return normalize(node_degree_centrality)

def closeness_centrality(G):
    return normalize(nx.closeness_centrality(G))

def eigenvector_centrality(G):
    return normalize(nx.eigenvector_centrality(G))

def betweenness_centrality(G):
    return nx.betweenness_centrality(G.to_undirected(), normalized=True)

def voterank_centrality(G):
    return normalize(nx.voterank(G))

def harmonic_centrality(G):
    return normalize(nx.harmonic_centrality(G))

def second_order_centrality(G):
    return nx.second_order_centrality(G.to_undirected())

def percolation_centrality(G):
    return nx.percolation_centrality(G)

def time_centrality(G):
    centrality = {}
    for node_name, node_content in G.nodes(data=True):
        if node_content['time'] <= math.e:
            centrality[node_name] = 1
        else:
            centrality[node_name] = 1/math.log(node_content['time'])

    return normalize(centrality)

def normalize(centrality):
    if len(centrality) == 1:
        return {key: 1.0 for key, _ in centrality.items()}

    total = 0
    for node, rank in centrality.items():
        total += rank

    normalize_centrality = {}
    for node, rank in centrality.items():
        normalize_centrality[node] = rank/total

    return normalize_centrality

def extract_node_content(graph_list):
    tokens_list = []
    for graph in graph_list:
        for node_name, node_content in graph.nodes(data=True):
            tokens = node_content['content']
            tokens_list.append(tokens)

    return tokens_list