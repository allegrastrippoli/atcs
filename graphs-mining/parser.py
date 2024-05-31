import networkx as nx
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

    
