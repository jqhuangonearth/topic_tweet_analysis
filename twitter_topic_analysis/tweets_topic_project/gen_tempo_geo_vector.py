"""
This file generate geo and temporal vector to be feeded into clustering model
@author: Bolun Huang
"""
import cjson
import json

class gen_geo_temp_vector:
    
    def __init__(self):
        self.X_train = {}
        
    def construct_vector(self):
        term_geo_dic = {}
        term_tempo_dic = {}
        f = open("../term_geo_tempo/term_geo_dic_09_1633_normalized.json")
        term_geo_dic = cjson.decode(f.readline())
        f.close()
        f = open("../term_geo_tempo/term_tempo_dic_09_1633_normalized.json")
        term_tempo_dic = cjson.decode(f.readline())
        f.close()
        
        for term in term_geo_dic:
            geo_tempo_vector = []
            for item in term_geo_dic[term]:
                geo_tempo_vector.append(item)
            for item in term_tempo_dic[term]:
                geo_tempo_vector.append(item)
            self.X_train.update({term : geo_tempo_vector})
        
        term_tempo_dic.clear()
        term_geo_dic.clear()
    
    def save_file(self):
        f = open("../term_geo_tempo/term_geo_tempo_vector.json","w")
        json.dump(self.X_train, f)
        f.close()
        
def main():
    ggtv = gen_geo_temp_vector()
    ggtv.construct_vector()
    ggtv.save_file()
    
if __name__ == "__main__":
    main()
        