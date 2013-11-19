"""
This program contains lots of utility functions to analyze the topic
for example, learn the distribution of topics, learn the temporal distribution
of topics, and learn the geo distribution of topics
@author: Bolun Huang
"""
import nltk
import cjson

class topic:
    def __init__(self):
        self.user_dic = {}
        self.state = {}
        
    def read_user_list(self, filename):
        f = open(filename, "r")
        for line in f:
            data = cjson.decode(line)
            data["geo_"]
        f.close()
        print len(self.user_dic)
        print nltk.corpus.stopwords.words("english")
        
def main():
    mytopic = topic()
    mytopic.read_user_list("/Users/zhijiaoliu/Documents/PythonZL/test/obama.json")
    
    
if __name__ == "__main__":
PA'    main()
