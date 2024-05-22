def getDegree(graph):
    deg = []
    for node in graph:
        deg.append(len(graph[node]))
    return deg

#        COUNTING SORT
#         0  1  2  3  4  5
# deg:   [1, 4, 1, 1, 2, 1] => the degree of node 0 is 1
# bins:  [0, 4, 1, 0, 1]    => 4 nodes have degree equal to 1
# bins:  [0, 0, 4, 5, 5]    => nodes with degree equal to 2, start at pos 4
# sort: [0, 2, 3, 5, 4, 1]  => node with id 3 has degree 1 and has position 2
# pos:  [0, 5, 1, 2, 4, 3] => sort: pos=5, id=1, pos: pos=1, id=5

def countingSort(graph, deg):
    bins = [0] * (len(graph))
    for elem in deg:
        bins[elem] += 1

    start = 0
    for degree in range(len(bins)):
        num = bins[degree]
        bins[degree] = start
        start += num

    sort = [0] * (len(graph))
    bins_tmp = bins.copy()
    for node in range(len(graph)):
        sort[bins_tmp[deg[node]]] = node
        bins_tmp[deg[node]] += 1

    pos = [0] * (len(sort))
    for i in range(len(sort)):
        pos[sort[i]] = i

    return bins, sort, pos

# sort: [3, ., 0, ., ., .]
# pos:  [2, ., ., 0, ., .] node with id 3 has position 0, node with id 0 has position 2 

def decreaseDeg(node, deg, bins, sort, pos):
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
    

def main():

    # graph = {0: [1],
    #       1: [0,2,3,4],
    #       2: [1],
    #       3: [1],
    #       4: [1,5],
    #       5: [4]}
    
    graph = {0: [1,2,3,4],
             1: [0,2,3,4],
             2: [0,1,3,4],
             3: [0,1,2,4],
             4: [0,1,2,3,5],
             5: [4],
             6: [7,8],
             7: [6,9],
             8: [6,9],
             9: [7,8]}
                 
    deg = getDegree(graph)
    print(deg)
    bins, sort, pos = countingSort(graph, deg)
    print(bins, sort, pos)
    for node in sort: 
        for neighbour in graph[node]:
            if deg[neighbour] > deg[node]:
                deg, bins, sort, pos = decreaseDeg(neighbour, deg, bins, sort, pos)

    print(deg)

if __name__ == "__main__":
    main()
