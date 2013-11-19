import networkx as nx
import matplotlib.pyplot as plt

"""
Hyperlink-Included Topic Search implementation
@author: Bolun hbl080212(at)neo(dot)tamu(dot)edu
@reference: http://code.google.com/p/python-graph/issues/detail?id=113
@copyright: http://code.google.com/p/python-graph/issues/detail?id=113
@copyright: Free to use
"""
def hits(graph, root_set=[], max_iterations=100, min_delta=0.0001):
    """
    Compute and return the PageRank in an directed graph. We assume that the
    source node points to the target node according to the links.

    @type  graph: digraph
    @param graph: Digraph

    @type  root_set: list
    @param root_set: The most relevant pages to the search query

    @type  max_iterations: number
    @param max_iterations: Maximum number of iterations.

    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.

    @rtype: tuple of dictionaries
    @return: Two (hub, authority) dictionaries containing the corresponding
             scores for each node.
    """

    # extend root set by appending all the pages that point or are pointed
    # by the rott set
    base_set = []
    if not root_set:
        base_set = graph.nodes()
    else:
        base_set = []
        for node in root_set:
            for nod in graph.node_incidence[node]:
                base_set.append(nod)
        for node in root_set:
            for nod in graph.node_neighbors[node]:
                base_set.append(nod)
        base_set.extend(root_set)
        base_set = set(base_set)

    auth = dict.fromkeys(base_set, 1)
    hub = dict.fromkeys(base_set, 1)
    
    i = 0
    for i in range(max_iterations):
        for p in base_set:
            hub_list = [hub.get(q[0]) for q in graph.in_edges(p)]
            #print hub_list
            auth[p] = sum(hub_list)

        auth = normalize(auth)

        old_hub = dict()
        for p in base_set:
            old_hub[p] = hub[p]
            auth_list = [auth.get(r[0]) for r in graph.out_edges(p)]
            #print auth_list
            hub[p] = sum(auth_list)

        hub = normalize(hub)

        delta = sum((abs(old_hub[k] - hub[k]) for k in hub))
        if delta <= min_delta:
            return (hub, auth)

    return (hub, auth)


def normalize(dictionary):
    """ Normalize the values of a dictionary to sum up to 1. """
    norm = sum((dictionary[p] for p in dictionary))
    if norm!=0:
        return {k: (v / float(norm))*100000 for (k, v) in dictionary.items()}
    else:
        return {k: v for (k, v) in dictionary.items()}



def draw_graph(G):
    """
    @type G: DiGraph
    @param G: DiGraph
    """
    nx.draw(G, pos = nx.random_layout(G, dim = 2), randomcmap = plt.get_cmap('jet'), node_color = "blue", alpha = 0.5, width = 1, node_size = 400, with_labels=True)
    plt.show()


class hits_test():
    def __init__(self):
        self.G = nx.DiGraph() # internal graph
        
    def construct_graph(self, node_list, edge_list):
        """
        @type node_list: list
        @param node_list: list of uid of users
        
        @type edge_list: list of two tuple list
        @param edge_list: list of edges represented by [uid1, uid2]
        """
        for node in node_list:
            self.G.add_node(node)
        for edge in edge_list:
            self.G.add_edge(edge[0], edge[1])
        
    def run_hits(self):
        return hits(self.G)
        
def main():
    ht = hits_test()
    G = nx.DiGraph()
    
    '''
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_node(5)
    G.add_node(6)
    G.add_node(7)
    G.add_node(8)
    
    G.add_edge(1,4)
    G.add_edge(1,6)
    G.add_edge(1,2)
    G.add_edge(2,5)
    G.add_edge(2,3)
    G.add_edge(2,8)
    G.add_edge(3,1)
    G.add_edge(3,6)
    G.add_edge(4,6)
    G.add_edge(4,5)
    G.add_edge(4,2)
    G.add_edge(4,7)
    G.add_edge(4,8)
    G.add_edge(5,1)
    G.add_edge(5,3)
    G.add_edge(5,8)
    G.add_edge(6,2)
    G.add_edge(6,7)
    G.add_edge(6,8)
    G.add_edge(7,1)
    G.add_edge(7,3)
    G.add_edge(7,8)
    #G.add_edge(8,4)
    '''
    
    fr = open("D:\PythonWorkspace\user_id.txt", "r")
    fr2 = open("D:\PythonWorkspace\user_edge.txt", "r")
    
    for i in fr:
        G.add_node(int(i))
    
    for j in fr2:
        tmp = j.split(' ')
        G.add_edge(int(tmp[0]), int(tmp[1]))
    
    fr.close()
    fr2.close()
    
    
    #print G.nodes()
    
    #for i in G.in_degree_iter(2):
    #    print i
    #for o in G.out_degree_iter(2):
    #    print o
        
    #print G.in_edges(2)
    #print G.out_edges(2)
    
    ht.G = G
    hub_auth = ht.run_hits()
    print "hub_scores ", hub_auth[0]
    print "auth_scores", hub_auth[1]
    
    #draw_graph(G)
    
if __name__ == "__main__":
    main()