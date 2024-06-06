import kcores 
import dsd
import networkx as nx
import utility as u  

def main():
    path = 'moreno_propro/out.moreno_propro_propro'
    G = u.parser(path)
    ds = dsd.densest_subg(G, G.number_of_edges(), G.number_of_nodes())
    u.dsd_to_csv(ds, G.nodes() , 'dsd')
    u.edges_to_csv(path, 'edges')

    deg = kcores.find_coreness(G)
    u.coreness_to_csv(deg, 'coreness')
    
if __name__ == "__main__":
    main()
