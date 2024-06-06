import kcores 
import dsd
import networkx as nx
import utility as u  

def main():
    # path = 'moreno_propro/out.moreno_propro_propro'
    # G = u.parser(path)
    # ds = dsd.densest_subg(G, G.number_of_edges(), G.number_of_nodes())
    # u.dsd_to_csv(ds, G.nodes() , 'dsd')
    # u.edges_to_csv(path, 'edges')

    path = '../dataset/moreno_propro/out.moreno_propro_propro'
    G = u.parser(path)
    # deg = kcores.find_coreness(G)
    deg = kcores.get_degree(G)
    count_dict = { 1: 0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    for elem in deg:
        if elem in count_dict:
            count_dict[elem] += 1
        else:
            count_dict[elem] = 1
    print(count_dict)
    # u.coreness_to_csv(deg, 'coreness')
    # u.edges_to_csv(path, 'edges')
    
if __name__ == "__main__":
    main()
