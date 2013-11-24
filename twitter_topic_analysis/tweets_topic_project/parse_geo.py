"""
This is a helper function that parse string geo so as to generate
a distribution of US states.
@author: Bolun Huang
"""
import cjson
import json
from pymongo import Connection
import numpy as np
    
state_code = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA",
              "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", 
              "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", 
              "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

class geo_histogram:
    def __init__(self):
        self.histogram_dic = {}
        self.histogram_dic = { key : 0 for key in state_code}
        
    @staticmethod
    def parser_string_geo(str1):
        location = str1.split(",")
        if len(location) == 2:
            return location[1].strip()
        else:
            return None
    
    def add(self, state):
        if state in self.histogram_dic:
            self.histogram_dic[state] += 1
        
    def histogram(self):
        return [[key, self.histogram_dic[key]] for key in state_code]
    
    def geo_vector(self):
        return [self.histogram_dic[key] for key in state_code]
    
    def mean(self):
        return np.mean([self.histogram_dic[key] for key in state_code])
    
    def std(self):
        return np.std([self.histogram_dic[key] for key in state_code])

def read_term_dic(filename):
    f = open(filename, "r")
    term_dic = cjson.decode(f.readline())
    f.close()
    return term_dic

def test():
    term_dic = read_term_dic("../term_dic/term_dic_09_1633.json")
    term_geo_dic = {}
    term_miu_std = {}
    DB_SERVER = "localhost"
    DB_PORT = 27017
    DB_NAME = "topicanalysis"
    COLLECTION_TV = "term_vectors"
    connection = Connection(DB_SERVER, DB_PORT)
    db = connection[DB_NAME]
    for term in term_dic:
        th = geo_histogram()
        it = db[COLLECTION_TV].find({"term_name" : term})
        for i in it:
            geo = i["footprint"]
            for t in geo:
                th.add(geo_histogram.parser_string_geo(t))
        term_geo_dic.update({term : th.geo_vector()})
        term_miu_std.update({term : {"avg" : th.mean(), "std" : th.std()}})
    
    f = open("../term_geo_tempo/term_geo_dic_09_1633.json", "w")
    json.dump(term_geo_dic, f)
    f.close()
    print "done 1"
    for term in term_geo_dic:
        summation = sum(term_geo_dic[term])
        if summation != 0:
            for i in range(len(term_geo_dic[term])):
                term_geo_dic[term][i] = (term_geo_dic[term][i] - term_miu_std[term]["avg"])/term_miu_std[term]["std"]
    f = open("../term_geo_tempo/term_geo_dic_09_1633_normalized.json", "w")
    json.dump(term_geo_dic, f)
    f.close()
    print "done 2"
    #print th.histogram()
    #print th.geo_vector()
    
if __name__ == "__main__":
    test()