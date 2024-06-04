import networkx as nx
import matplotlib.pyplot as plt
import re

def parser(filepath):

    G = nx.Graph()

    with open(filepath) as f:
        next(f)
        next(f)
        for line in f:
            n1 = int(line.split()[0])-1
            n2 = int(line.split()[1])-1
            G.add_edge(n1, n2)

    return G

def test_graph():
    graph = {0: [1,2,3,4],
             1: [0,2,3,4],
             2: [0,1,3,4],
             3: [0,1,2,4],
             4: [0,1,2,3,5],
             5: [4,6],
             6: [5,7,8],
             7: [6,9],
             8: [6,9],
             9: [7,8]}
                 
    return nx.Graph(graph)



def draw_graph(G, V1, name, color):
    sub = nx.subgraph(G,V1)
    pos = nx.spring_layout(G)
    nx.draw_networkx(sub, pos, node_color=color, width=2, with_labels=True)
    nx.draw_networkx_edges(sub, pos, edge_color=color, width=2)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(f'{name}plot.png', dpi=300)




