import matplotlib.pyplot as plt
import networkx as nx

def draw(G):
    nx.draw(G)
    plt.show()

def pageranks(G):
    pageranks = nx.pagerank(G)
    return pageranks