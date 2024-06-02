import utility as u
import networkx as nx

#        COUNTING SORT
#         0  1  2  3  4  5
# deg:   [1, 4, 1, 1, 2, 1] => the degree of node 0 is 1
# bins:  [0, 4, 1, 0, 1]    => 4 nodes have degree equal to 1
# bins:  [0, 0, 4, 5, 5]    => nodes with degree equal to 2, start at pos 4
# sort: [0, 2, 3, 5, 4, 1]  => node with id 3 has degree 1 and has position 2
# pos:  [0, 5, 1, 2, 4, 3] => sort: pos=5, id=1, pos: pos=1, id=5

def get_degree(graph):
    deg = []
    for node in graph:
        deg.append(graph.degree(node))
    return deg

def counting_sort(graph, deg):
    bins = [0] * (graph.number_of_nodes())
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

# sort: [3, ., 0, ., ., .]
# pos:  [2, ., ., 0, ., .] node with id 3 has position 0, node with id 0 has position 2 

def decrease_degree(node, deg, bins, sort, pos):
    # node = 3
    posNode = pos[node] # 2
    posFirstNodeWithSameDegree = bins[deg[node]] # 0
    nodef = sort[posFirstNodeWithSameDegree] # 0

    sort[posNode] = nodef 
    sort[posFirstNodeWithSameDegree] = node
    pos[node] = posFirstNodeWithSameDegree
    pos[nodef] = posNode

    bins[deg[node]] += 1
    deg[node] -= 1

    return deg, bins, sort, pos
    

def get_k(list, k):
    """
    imagine that you have a graph with 3 values of coreness: deg:[k, k+1, k+2]
    maybe you're interested in the highest coreness, maybe not...
    you can choose which community you want to highlight picking your k paramenter
    """
    list.sort()
    return list[k]


def find_coreness(G):
    deg = get_degree(G)
    bins, sort, pos = counting_sort(G, deg)
    for node in sort: 
        for neighbour in G.neighbors(node):
            if deg[neighbour] > deg[node]:
                deg, bins, sort, pos = decrease_degree(neighbour, deg, bins, sort, pos)
    
    max_value = max(deg)

    V1 = set()
    for i in range(0, len(deg)):
        if deg[i] == max_value:
            V1.add(i)
        
    return V1


def main():
    G = u.parser('moreno_lesmis/out.moreno_lesmis_lesmis')
    V1 = find_coreness(G)
    u.draw_graph(G, V1, 'kcore2')

if __name__ == "__main__":
    main()
