"""
Generate term vector
@author: Bolun Huang
"""
import cjson
import os
import gzip

DIR_T = "/home/bolun/terms_vector09/"

class gen_term_vector:
    def __init__(self):
        self.term_dic = {}
        self.term_list = []
        
    def read_term_dic(self, filename):
        f = open(filename, "r")
        self.term_dic = cjson.decode(f.readline())
        f.close()
        
    def gen_term_vector(self):
        for term in self.term_dic:
            path = os.path.join(DIR_T, term+".json.gz")
            if os.path.isfile(path):
                user_list = []
                time_stamp = []
                geo_footprint = []
                coordinates = []

                f = gzip.open(path, "r")
                for line in f:
                    data = cjson.decode(line)
                    if data["id"]["id"] not in user_list:
                        user_list.append(data["id"]["id"])
                    time_stamp.append(data["created_at"])
                    geo_footprint.append(data["geo_location"])
                    coordinates.append(data["coordinates"])
                term_vector = {}
                term_vector.update({"user_list" : user_list},
                                   {"time_stamp" : time_stamp},
                                   {"footprint" : geo_footprint},
                                   {"coordinates" : coordinates})
                f.close()