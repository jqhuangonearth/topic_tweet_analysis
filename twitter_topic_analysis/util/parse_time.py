"""
This is a helper function that parse string time like
"Fri Sep 19 06:12:43 +0000 2013". This function only consider
<Date> and return an integer of <Date>; the date is in 
the range of (1, 30)
@author: Bolun Huang
"""
import cjson
from pymongo import Connection
import numpy as np
import json

class time_histogram:
    
    def __init__(self):
        self.histogram_dic = {}
        for i in range(30):
            if i < 9:
                self.histogram_dic.update({"0"+str(i+1) : 0})
            else:
                self.histogram_dic.update({str(i+1) : 0})
    
    @staticmethod
    def parser_string_time(str1):
        """
        @type str: String
        @param str: String repre. of time stamp
        
        @type date_hour: tuple
        @return date_hour: date and hour of the time; return -1 is unknown
        """
        return str1.split(" ")[2]
    
    def add(self, str1):
        if self.histogram_dic.has_key(str1):
            self.histogram_dic[str1] += 1
        else:
            pass
    
    def histogram(self):
        """
        @type histogram: list
        @return: histogram of days
        """
        histogram = sorted(self.histogram_dic.iteritems(), key=lambda asd:asd[0], reverse = False) # sort dic as list
        return histogram

    def tempo_vector(self):
        histogram = sorted(self.histogram_dic.iteritems(), key=lambda asd:asd[0], reverse = False) # sort dic as list
        tempo_vector = [x[1] for x in histogram]
        return tempo_vector

    def mean(self):
        return np.mean([self.histogram_dic[key] for key in self.histogram_dic])
    
    def std(self):
        return np.std([self.histogram_dic[key] for key in self.histogram_dic])


def read_term_dic(filename):
    f = open(filename, "r")
    term_dic = cjson.decode(f.readline())
    f.close()
    return term_dic

def test():
    term_dic = read_term_dic("../term_dic/term_dic_09_1633.json")
    term_tempo_dic = {}
    term_miu_std = {}
    DB_SERVER = "localhost"
    DB_PORT = 27017
    DB_NAME = "topicanalysis"
    COLLECTION_TV = "term_vectors"
    connection = Connection(DB_SERVER, DB_PORT)
    db = connection[DB_NAME]
    for term in term_dic:
        th = time_histogram()
        it = db[COLLECTION_TV].find({"term_name" : term})
        for i in it:
            time_stamp = i["time_stamp"]
            for t in time_stamp:
                th.add(time_histogram.parser_string_time(t))
        term_tempo_dic.update({term : th.tempo_vector()})
        term_miu_std.update({term : {"avg" : th.mean(), "std" : th.std()}})
    
    f = open("../term_geo_tempo/term_tempo_dic_09_1633.json", "w")
    json.dump(term_tempo_dic, f)
    f.close()
    print "done 1"
    for term in term_tempo_dic:
        summation = sum(term_tempo_dic[term])
        if summation != 0:
            for i in range(len(term_tempo_dic[term])):
                term_tempo_dic[term][i] = (term_tempo_dic[term][i] - term_miu_std[term]["avg"])/term_miu_std[term]["std"]
    f = open("../term_geo_tempo/term_tempo_dic_09_1633_normalized.json", "w")
    json.dump(term_tempo_dic, f)
    f.close()
    print "done 2"
    
if __name__ == "__main__":
    test()