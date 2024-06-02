import networkx as nx
import matplotlib.pyplot as plt

def parser(filepath):

    G = nx.Graph()

    with open(filepath) as f:
        next(f)
        next(f)
        for line in f:
            word1 = int(line.split()[0])-1
            word2 = int(line.split()[1])-1
            G.add_edge(word1, word2)

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


def draw_graph(G, V1, name):
    nodelst = list(set(G.nodes()) - V1)
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, nodelist=V1, node_color='#A9BEFC', edge_color='#A9BEFC', with_labels=True)
    nx.draw_networkx(G, pos, nodelist=nodelst, node_color='#EBEAE9', edge_color='#EBEAE9', with_labels=True)
    nx.draw_networkx_edges(G, pos)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.show()
    # plt.savefig(f'graph_{name}.png', dpi=300)



    
