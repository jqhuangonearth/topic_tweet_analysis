"""
Generate term vector
@author: Bolun Huang
"""
import cjson
import os
import gzip
import json

DIR_T = "/home/bolun/terms_vector09_reduced/"

class gen_term_vector:
    def __init__(self):
        self.term_dic = {}
        self.id_name_map = {}
        self.term_list = []
        
    def read_term_dic(self, filename):
        f = open(filename, "r")
        self.term_dic = cjson.decode(f.readline())
        f.close()
        
    def read_id_name_map(self, filename):
        f = open(filename, "r")
        self.id_name_map = cjson.decode(f.readline())
        f.close()
        
    def gen_term_vector(self, test = False):
        self.read_term_dic("../term_dic/term_dic_09_reduced.json") # read term dict
        print len(self.term_dic)
        self.read_id_name_map("../user_dic/id_name_map_09_wids_2.json") # read id map
        if test:
            self.test()
        if not test:
            count = 0
            for term in self.term_dic:
                path = os.path.join(DIR_T, term+".json.gz")
                if os.path.isfile(path):
                    user_list = []
                    user_names = []
                    time_stamp = []
                    geo_footprint = []
                    coordinates = []
                    try:
                        f = gzip.open(path, "r")
                        for line in f:
                            data = cjson.decode(line)
                            if data["id"]["id"] not in user_list:
                                user_list.append(data["id"]["id"])
                            time_stamp.append(data["created_at"])
                            geo_footprint.append(data["geo_location"])
                            coordinates.append(data["coordinates"])
                        user_names = [self.id_name_map[str(user_list[i])] for i in range(len(user_list))]
                        #print user_list
                        #print user_names
                        if len(user_names) != len(user_list):
                            print "error detected: len(user_name) and len(user_list) not matched"
                        
                        term_vector = {}
                        term_vector.update({"_id" : count,
                                            "term_name" : term,
                                            "user_list" : user_list,
                                            "user_names" : user_names,
                                            "time_stamp" : time_stamp,
                                            "footprint" : geo_footprint,
                                            "coordinates" : coordinates})
                        f.close()
                        self.term_list.append(term_vector)
                    except Exception as e:
                        print "error in gzip", path, e
                        pass
                else:
                    print "error: file not found", path
                count += 1
                if count%100 == 0: # write to file for every 5000 terms
                    print "count", count
                    ft = open("/home/bolun/term_vectors09/term_vectors.json", "a")
                    for item in self.term_list:
                        json.dump(item, ft)
                        ft.write("\n")
                    ft.close()
                    self.term_list = []

    def test(self):
        path = os.path.join(DIR_T, "obama.json.gz")
        if os.path.isfile(path):
            user_list = []
            time_stamp = []
            geo_footprint = []
            coordinates = []
                    
            f = gzip.open(path, "r")
            print f.readlines()
            for line in f:
                data = cjson.decode(line)
                if data["id"]["id"] not in user_list:
                    user_list.append(data["id"]["id"])
                time_stamp.append(data["created_at"])
                geo_footprint.append(data["geo_location"])
                coordinates.append(data["coordinates"])
            term_vector = {}
            term_vector.update({"user_list" : user_list,
                                "time_stamp" : time_stamp,
                                "footprint" : geo_footprint,
                                "coordinates" : coordinates})
            f.close()
            self.term_list.append(term_vector)
        else:
            print "error: file not found"
            pass

def gen_id_name_map():
    f = open("../user_dic/user_dic_09_wids_2.json", "r")
    for line in f:
        user_dic = cjson.decode(line)
    f.close()
    id_name_map = {}
    for user in user_dic:
        id_name_map.update({user_dic[user]["id"] : user})
    f = open("../user_dic/id_name_map_09_wids_2.json", "w")
    json.dump(id_name_map, f)
    f.close()
    

def main():
    #gen_id_name_map()
    myg = gen_term_vector()
    myg.gen_term_vector()

if __name__ == "__main__":
    main()