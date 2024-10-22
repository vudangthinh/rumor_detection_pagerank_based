import networkx as nx
import matplotlib.pyplot as plt

DG = nx.DiGraph()
DG.add_nodes_from([552784600502915072, 552785249420447745, 552786761534144512, 552786954656710656, 552787979224092672, 552792580631457792, 552792981020086272, 552802466937327616, 552790305263849472, 552793401037320192, 552891302065737729, 552788534269341696, 552864675743158272])

DG.add_edges_from([(552785249420447745, 552784600502915072),
                   (552786761534144512, 552784600502915072),
                   (552786803884060672, 552784600502915072),
                   (552786954656710656, 552784600502915072),
                   (552787979224092672, 552784600502915072),
                   (552792580631457792, 552784600502915072),
                   (552792981020086272, 552784600502915072),
                   (552802466937327616, 552784600502915072),
                   (552790305263849472, 552786803884060672),
                   (552793401037320192, 552786803884060672),
                   (552891302065737729, 552786803884060672),
                   (552788534269341696, 552787979224092672),
                   (552864675743158272, 552792981020086272)])

DG.add_weighted_edges_from([(552784600502915072, 552784600502915072, 1)])
DG.add_weighted_edges_from([(552784600502915072, 552785249420447745, 0.3)])
DG.add_weighted_edges_from([(552784600502915072, 552786761534144512, 0.3)])
# print(nx.degree_centrality(DG))
print(DG)
pageranks = nx.pagerank(DG)
for k, v in pageranks.items():
    pageranks[k] = round(v, 2)

for node, rank in pageranks.items():
    DG.nodes[node]['rank'] = rank


# visualize graph
color_map = []
for node in DG:
    print(node)
    if node == 552784600502915072:
        color_map.append('red')
    else:
        color_map.append('green')
nx.draw(DG, labels=pageranks, node_color=color_map, font_size=8, font_weight='bold', node_size=[v * 5000 for v in pageranks.values()])
plt.show()