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
        Gd.add_edge(node, 't', capacity=(m+2*g-Gu.degree[node]))
        Gd.add_edge('s', node, capacity=m)

    return Gd
    
# Let D = |E|/|V| be the density of the desired subgraph
# g is the guess for D

def densest_subg(Gu, m, n): 
    min_density = 0  
    max_density = m  
    V1 = set()  
    while max_density-min_density >= 1/(n*(n-1)):
        # for O(logn) times, g is updated 
        g = (max_density+min_density)/2
        Gd = get_flow_network(Gu, m, g)
        _, partition = nx.minimum_cut(Gd, 's', 't')
        S, _ = partition
        if S == {'s'}: # g >= D
            max_density = g
        else:  
            min_density = g # g <= D
            S.remove('s')
            V1.update(S)
    return V1 
    

