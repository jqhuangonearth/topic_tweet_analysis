"""
This program contains lots of utility functions to analyze the topic
for example, learn the distribution of topics, learn the temporal distribution
of topics, and learn the geo distribution of topics
@author: Bolun Huang
"""

import cjson

class topic:
    def __init__(self):
        self.user_dic = {}
        
    def read_user_list(self, filename):
        f = open(filename, "r")
        self.user_dic = cjson.decode(f.read())
        f.close()
        print len(self.user_dic)
        
def main():
    mytopic = topic()
    mytopic.read_user_list("../user_dic/user_dic_09.json")
    
    
if __name__ == "__main__":
    main()