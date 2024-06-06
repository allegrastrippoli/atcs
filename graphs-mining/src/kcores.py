import networkx as nx

# COUNTING SORT
# deg:   [] => the degree of node 0 is 1
# bins:  [] => 4 nodes have degree equal to 1
# bins:  [] => nodes with degree equal to 2, start at pos 4
# sort: [0, 2, 3, 5, 4, 1]  => node with id 3 has degree 1 and has position 2
# pos:  [0, 5, 1, 2, 4, 3] => sort: pos=2, id=3, pos: pos=3, id=2

def get_degree(graph: nx.Graph):
    deg = [0] * graph.number_of_nodes()
    for node in graph.nodes():
            deg[node] = graph.degree(node)
    return deg

def counting_sort(graph, deg):
    bins = [0] * (max(deg)+1)
    for elem in deg:
        bins[elem] += 1

    start = 0
    for degree in range(len(bins)):
        num = bins[degree]
        bins[degree] = start
        start += num

    sort = [0] * (graph.number_of_nodes())
    bins_tmp = bins.copy()
    for node in range(graph.number_of_nodes()):
        sort[bins_tmp[deg[node]]] = node
        bins_tmp[deg[node]] += 1

    pos = [0] * (len(sort))
    for i in range(len(sort)):
        pos[sort[i]] = i

    return bins, sort, pos


def decrease_degree(node, deg, bins, sort, pos):
    posNode = pos[node] 
    posFirstNodeWithSameDegree = bins[deg[node]] 
    if posFirstNodeWithSameDegree != node:
        nodef = sort[posFirstNodeWithSameDegree] 

        sort[posNode] = nodef 
        sort[posFirstNodeWithSameDegree] = node
        pos[node] = posFirstNodeWithSameDegree
        pos[nodef] = posNode

    if bins[deg[node]]+1 >= len(sort):
        bins = bins[:len(bins)-1]
    else:
        bins[deg[node]] += 1 

    deg[node] -= 1

    return deg, bins, sort, pos
    
def find_coreness(graph):
    deg = get_degree(graph)
    bins, sort, pos = counting_sort(graph, deg)
    for node in sort: 
        for neighbour in graph.neighbors(node):
            if deg[neighbour] > deg[node]:
                deg, bins, sort, pos = decrease_degree(neighbour, deg, bins, sort, pos)

    return deg



    
