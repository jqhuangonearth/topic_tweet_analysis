import networkx as nx
import matplotlib.pyplot as plt
import cjson
import gzip
import json

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
            auth_list = [auth.get(r[1]) for r in graph.out_edges(p)]
            #print auth_list
            hub[p] = sum(auth_list)

        hub = normalize(hub)

        delta = sum((abs(old_hub[k] - hub[k]) for k in hub))
        if delta <= min_delta:
            return (hub, auth)
    return (hub, auth)


def normalize(dictionary):
    length = len(dictionary)
    """ Normalize the values of a dictionary to sum up to 1. """
    norm = sum((dictionary[p] for p in dictionary))
    if norm!=0:
        return {k: (v / float(norm))*length for (k, v) in dictionary.items()}
    else:
        return {k: v for (k, v) in dictionary.items()}

def pre_process():
    """
    Dump user friends for whole month for September
    """
    user_friends = {}
    f = gzip.open("../social_graph/user_friends_09.json.gz", "r")
    for line in f:
        data = cjson.decode(line)
        for key in data:
            if not user_friends.has_key(key):
                user_friends.update({key : data[key]})
            else:
                pass
    f.close()
    f = gzip.open("../social_graph/user_friends_09_2.json.gz", "r")
    for line in f:
        data = cjson.decode(line)
        for key in data:
            if not user_friends.has_key(key):
                user_friends.update({key : data[key]})
            else:
                pass
    f.close()
    f = gzip.open("../social_graph/user_friends_09_total.json.gz","w")
    json.dump(user_friends, f)
    f.close()

def process_user_graph():
    f = open("../user_dic/user_dic_09_wids_2.json","r")
    user_dic = cjson.decode(f.readline())
    user_ids = set()
    for user in user_dic:
        user_ids.add(str(user_dic[user]["id"]))
    print len(user_dic)
    print len(user_ids)
    
    f.close()
    fo = open("../social_graph/graph_reduced.txt","w")
    fo.write("#nodes\n")
    #for user in user_dic:
    #    fo.write(str(user_dic[user]["id"])+"\n")
    for user in user_ids:
        fo.write(user+"\n")
    
    fo.write("#edges\n")
    f = gzip.open("../social_graph/user_friends_09_total.json.gz")
    user_friends = cjson.decode(f.readline())
    print len(user_friends)

    for user in user_friends:
        if user in user_ids:
            for friend in user_friends[user]:
                if str(friend) in user_ids:
                    fo.write(user+" "+str(friend)+"\n")
                else:
                    pass
    f.close()
    fo.close()
    

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
    #pre_process()
    #process_user_graph()
    #exit(0)
    ht = hits_test()
    G = nx.DiGraph()
    
    """
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
    """
    
    fg = open("../social_graph/graph_reduced.txt", "r")
    flag = 0
    node_list = []
    edge_list = []
    for line in fg:
        if flag == 1:
            try:
                node_list.append(str(int(line)))
            except:
                pass
        elif flag == 2:
            try:
                edge = line.split(" ")
                edge_list.append([str(int(edge[0])), str(int(edge[1]))])
            except:
                pass
        if line.startswith("#nodes"):
            flag = 1
        elif line.startswith("#edges"):
            flag = 2
    fg.close()
    print len(node_list), len(edge_list)
    ht.construct_graph(node_list, edge_list)
    hub_auth = ht.run_hits()
    auth_score = hub_auth[1]
    f = open("../social_graph/authorities.json","w")
    json.dump(auth_score, f)
    f.close()
    #print sorted(hub_auth[1].iteritems(), key=lambda asd:asd[1], reverse = False)
    #print "hub_scores ", hub_auth[0]
    #print "auth_scores", hub_auth[1]
    
    #draw_graph(G)
    
if __name__ == "__main__":
    main()