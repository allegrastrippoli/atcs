import random as r
import utility as u
import networkx as nx

# Gu: undirected graph
# Gd: directed graph
def get_flow_network(Gu, m, g):

    Gd = nx.DiGraph()

    for node in Gu.nodes:
        Gd.add_node(node)
    for edge in Gu.edges:
        Gd.add_edge(edge[0], edge[1], capacity=1)
        Gd.add_edge(edge[1], edge[0], capacity=1)

    Gd.add_node('s')
    Gd.add_node('t')

    for node in Gu.nodes:
        Gd.add_edge(node, 't', capacity=(m+2*g-Gd.degree[node]))
        Gd.add_edge('s', node, capacity=m)

    return Gd
    

# The density of a graph is the ratio of the number of edges to the number of vertices of the graph. D = |E|/|V|

# Let D be the density of the desired subgraph
# g is the guess for D
# finché |V1| = 0 then g >= D
# if |V1| != 0 then g <= D
def densest_subg(Gu, m, n): 
    l = 0  
    u = m  
    V1 = set() 
    while u-l >= 1/(n*(n-1)):
        # for O(logn) times, g is updated 
        g = (u+l)/2
        Gd = get_flow_network(Gu, m, g)
        _, partition = nx.minimum_cut(Gd, 's', 't')
        S, T = partition
        if S == {'s'}:
            u = g
        else: 
            l = g
            S.remove('s')
            V1.update(S)
    return V1 
    

def main():
    G = u.parser('moreno_lesmis/out.moreno_lesmis_lesmis')
    V1 = densest_subg(G, G.number_of_edges(), G.number_of_nodes())
    u.draw_graph(G, V1, 'dsd2')
    
if __name__ == "__main__":
    main()
