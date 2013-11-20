"""
This program calculates the nutrition value & energy value of each term
in time series as the feature vector to be feeded into machine learning 
model
@author: Bolun Huang
"""
import cjson
import time
import json

DIR_TN = "../term_nutrition/"

class term_nutrition:
    def __init__(self):
        self.term_dic = {}
        self.term_tfidf_dic = {}
    
    def read_term_dic(self, filename):
        f = open(filename, "r")
        self.term_dic = cjson.decode(f.readline())
        f.close()
    
    def read_term_tfidf(self, filename):
        self.read_term_dic("../term_dic/term_dic_09_reduced.json")
        start = time.clock()
        f = open(filename,"r")
        for line in f:
            data = cjson.decode(line)
            #print data
            self.term_tfidf_dic.update({key : data[key] for key in data})
        f.close()
        print "length of term_tfidf_dic: ", len(self.term_tfidf_dic)
        end = time.clock()
        print "time: %.2f s" %(end - start)
        
        delete_list = []
        for key in self.term_dic:
            if not self.term_tfidf_dic.has_key(key):
                delete_list.append(key)
        
        for key in delete_list:
            self.term_dic.pop(key)
        print len(self.term_tfidf_dic)
        print len(self.term_dic)
        
        f1 = open(DIR_TN+"term_dic_09_processed.json", "w")
        json.dump(self.term_dic, f1)
        f1.close()
        f2 = open(DIR_TN+"term_tfidf_dic_09_processed.json", "w")
        json.dump(self.term_tfidf_dic, f2)
        f2.close()
    
    def gen_nutrition(self):
        print "get nutrition"
        
        
def main():
    tn = term_nutrition()
    tn.read_term_tfidf("../term_dic/term_tfidf.json")
    
if __name__ == "__main__":
    main()