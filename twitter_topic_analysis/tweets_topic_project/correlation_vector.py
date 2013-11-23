"""
This program implements the item-item correlation vectors
@author: Bolun Huang
"""
import cjson
from pymongo import Connection
import json
import math
import time

DBSERVER = "localhost"
DBNAME = "topicanalysis"
DBPORT = 27017
COLLECTION_TV = "term_vectors" 
N = 40000 # number of users(roughly)

class correlation_vector:
    def __init__(self):
        self.term_dic = {}
        self.connection = Connection(DBSERVER, DBPORT)
        self.db = self.connection[DBNAME]
        self.term_user_list_dic = {}
        
    def get_user_list_dic(self):
        for term in self.term_dic:
            it1 = self.db[COLLECTION_TV].find({ "term_name" : term})
            user_list = []
            for i in it1:
                user_list = i["user_list"]
            self.term_user_list_dic.update({term : user_list})
        print "term_user_dic done..."
    
    def gen_correlation_vector(self):
        
        f = open("../term_graph/term_graph_09_3003.txt","a")
        f.write("#terms\n")
        for term in self.term_dic:
            f.write(term+"\n")
        f.write("#edges\n")
        f.close()
        
        print "terms done..."
        cv_list = []
        term_list = self.term_dic.keys()
        for t1 in range(len(term_list)):
            user_list_1 = self.term_user_list_dic[term_list[t1]]
            N_k = len(user_list_1)
            print "start %s ..." %term_list[t1]
            start = time.clock()
            for t2 in range(t1,len(term_list)):
                if not term_list[t1] == term_list[t2]:
                    user_list_2 = self.term_user_list_dic[term_list[t2]]
                    N_z = len(user_list_2)
                    R_kz = 0
                    R_kz = self.find_size_of_common_sublist(user_list_1, user_list_2)
                    
                    if R_kz == 0:
                        cv_list.append([term_list[t1], term_list[t2], float("-inf")])
                        cv_list.append([term_list[t2], term_list[t1], float("-inf")])
                    else:
                        try:
                            N_kz_1 = math.log((R_kz)/float(N_k - R_kz)/float(N_z - R_kz)*(N - N_z - N_k + R_kz))
                            N_kz_2 = math.fabs(R_kz/float(N_k)-(N_z - R_kz)/float(N - N_k))
                            N_zk_1 = math.log((R_kz)/float(N_z - R_kz)/float(N_k - R_kz)*(N - N_z - N_k + R_kz))
                            N_zk_2 = math.fabs(R_kz/float(N_z)-(N_k - R_kz)/float(N - N_z))
                            C_kz = N_kz_1*N_kz_2
                            C_zk = N_zk_1*N_zk_2
                            cv_list.append([term_list[t1], term_list[t2], C_kz])
                            cv_list.append([term_list[t2], term_list[t1], C_zk])
                        except:
                            cv_list.append([term_list[t1], term_list[t2], float("-inf")])
                            cv_list.append([term_list[t2], term_list[t1], float("-inf")])
                            pass
                    
            # for every term and other terms, dump to file
            end = time.clock()
            print "done %s ... %.2fs" %(term_list[t1], (end - start)) 
            f = open("../term_graph/term_graph_09_3003.txt","a")
            for cv in cv_list:
                f.write(cv[0]+" "+cv[1]+" "+str(cv[2])+"\n")
            f.close()
            cv_list = []

    
    def find_size_of_common_sublist(self, list1, list2):
        """
        @return: how many common elements in two lists; list has no duplicates
        """
        comm = 0
        dist = {}
        for item in list1:
            if not dist.has_key(item):
                dist.update({item : 1})
            else:
                dist[item] += 1
        for item in list2:
            if not dist.has_key(item):
                dist.update({item : 1})
            else:
                dist[item] += 1
        
        for item in dist:
            if dist[item] == 2:
                comm += 1
        return comm


    def find_size_of_common_sublist_2(self, list1, list2):
        """
        @return: how many common elements in two lists; list has no duplicates
        This is brute-force method
        """
        comm = 0
        for item1 in list1:
            for item2 in list2:
                if item1 == item2:
                    comm += 1
        return comm

    def read_term_dic(self, filename):
        f = open(filename, "r")
        self.term_dic = cjson.decode(f.readline())
        f.close()
        print len(self.term_dic)

    def reduce_term_dic(self, filename):
        """
        reduce the term_dic by only retaining the most frequently used
        ones. The threshold is 666.
        """
        f = open(filename, "r")
        self.term_dic = cjson.decode(f.readline())
        f.close()
        print len(self.term_dic)
        filtered_list = []
        for term in self.term_dic:
            if self.term_dic[term] < 1063:
                filtered_list.append(term)
        for term in filtered_list:
            self.term_dic.pop(term)
        print len(self.term_dic)
        f = open("../term_dic/term_dic_09_3003.json","w")
        json.dump(self.term_dic, f)
        f.close()        

def main():
    cv = correlation_vector()
    #cv.read_term_dic("../term_dic/term_dic_09_3003.json")
    #cv.reduce_term_dic("../term_dic/term_dic_09_4164.json")
    #cv.get_user_list_dic()
    #cv.gen_correlation_vector()
    
if __name__ == "__main__":
    main()