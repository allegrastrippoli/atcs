import networkx as nx
import kcores 
import dsd
import matplotlib.pyplot as plt

def parser(filepath):

    G = nx.Graph()

    with open(filepath) as f:
        for line in f:
            n1 = int(line.split()[0])-1
            n2 = int(line.split()[1])-1
            G.add_edge(n1, n2)

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

def draw_full_graph(G :nx.Graph, V1, name, color):
    nodelist = list(set(G.nodes()) - V1)
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, nodelist=V1, node_color=color, width=2, with_labels=True)
    nx.draw_networkx(G, pos, nodelist=nodelist, node_color='#E0D4C8', width=2, with_labels=True)
    nx.draw_networkx_edges(G, pos, edge_color='#E0D4C8', width=2)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(f'plots/{name}plot.png', dpi=300)
    plt.close()
 
def draw_community_graph(G, V1, name, color):
    sub = nx.subgraph(G,V1)
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    nx.draw_networkx(sub, pos, node_color=color, width=2, with_labels=True)  
    nx.draw_networkx_edges(G, pos, edge_color='#E0D4C8', width=1)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(f'plots/{name}plot.png', dpi=300)
    plt.close()


def plot_everything():
    G = test_graph()
    V1 = dsd.densest_subg(G, G.number_of_edges(), G.number_of_nodes())
    draw_full_graph(G, V1, f'dsd_test_', '#A9BEFC')
    V1 = kcores.find_coreness(G)
    draw_full_graph(G, V1, f'kcore_test_', '#6AB67F')

    dataset_paths = ['dolphins/out.dolphins', 'moreno_zebra/out.moreno_zebra_zebra', 'moreno_lesmis/out.moreno_lesmis_lesmis', 'subelj_euroroad/out.subelj_euroroad_euroroad']

    i = 0
    for path in dataset_paths:
        G = parser(path)
        V1 = dsd.densest_subg(G, G.number_of_edges(), G.number_of_nodes())
        draw_community_graph(G, V1, f'{path.split('/')[0]}/dsd{i}', '#A9BEFC')
        V1 = kcores.find_coreness(G)
        draw_community_graph(G, V1, f'{path.split('/')[0]}/kcore{i}', '#6AB67F')
        # V1 = nx.k_core(G)
        # draw_community_graph(G, V1, f'{path.split('/')[0]}/kcore_truth{i}', '#B56969')
        # draw_community_graph(G, G.nodes(), f'{path.split('/')[0]}/original{i}', '#E0D4C8')
        i = i+1

def coreness_to_csv(labels, filename):
    
    with open(f'{filename}.csv', 'w') as file:
        file.write('Id,Label\n') 
        for i, label in enumerate(labels):
            file.write(f'{i},{label}\n')


def edges_to_csv(filer, filew):
    
    with open(f'{filew}.csv', 'w') as file:
        file.write('Source,Target\n') 

        with open(filer) as f:
            for line in f:
                n1 = int(line.split()[0])-1
                n2 = int(line.split()[1])-1
                file.write(f'{n1},{n2}\n') 

def dsd_to_csv(ds, nodes, filename):
    
    with open(f'{filename}.csv', 'w') as file:
        file.write('Id,Label\n') 
        for node in nodes:
            if node in ds:
                file.write(f'{node},1\n')
            else:
                file.write(f'{node},0\n')

