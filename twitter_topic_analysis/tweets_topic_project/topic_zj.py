"""

"""
import nltk
import cjson

state_code = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

class topic:
    def __init__(self):
        self.user_dic = {}
        self.state = {}
        
    def read_user_list(self, filename):
        f = open(filename, "r")
        for line in f:
           data = cjson.decode(line)
           location = data["geo_location"].split(",")
           state = location[len(location) - 1].strip()
           if not self.state.has_key(state):
               self.state.update({state: 1})
           else:
                self.state[state] += 1
        f.close()
        #print self.state
        delete_list = []
        for st in self.state:
            if not st in state_code:
                delete_list.append(st)
        for dl in delete_list:
            self.state.pop(dl)
        print self.state
        #print len(self.user_dic)
        #print nltk.corpus.stopwords.words("english")
        
def main():
    mytopic = topic()
    mytopic.read_user_list("/Users/zhijiaoliu/Documents/PythonZL/test/obama.json")
    
    
if __name__ == "__main__":
    main()
