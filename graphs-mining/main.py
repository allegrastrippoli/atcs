import kcores 
import dsd
import networkx as nx
import utility as u

def main():

    G = u.test_graph()
    V1 = dsd.densest_subg(G, G.number_of_edges(), G.number_of_nodes())
    u.draw_test_graph(G, V1, f'dsd_test_', '#A9BEFC')
    V1 = kcores.find_coreness(G)
    u.draw_test_graph(G, V1, f'kcore_test_', '#6AB67F')

    
    dataset_paths = ['dolphins/out.dolphins', 'moreno_zebra/out.moreno_zebra_zebra', 'moreno_lesmis/out.moreno_lesmis_lesmis', 'subelj_euroroad/out.subelj_euroroad_euroroad']

    i = 0
    for path in dataset_paths:
        G = u.parser(path)
        V1 = dsd.densest_subg(G, G.number_of_edges(), G.number_of_nodes())
        u.draw_graph(G, V1, f'{path.split('/')[0]}/dsd{i}', '#A9BEFC')
        V1 =kcores.find_coreness(G)
        V1 = nx.k_core(G)
        u.draw_graph(G, V1, f'{path.split('/')[0]}/kcore_truth{i}', '#B56969')
        u.draw_graph(G, G.nodes(), f'{path.split('/')[0]}/original{i}', '#E0D4C8')
        i = i+1
    
if __name__ == "__main__":
    main()
