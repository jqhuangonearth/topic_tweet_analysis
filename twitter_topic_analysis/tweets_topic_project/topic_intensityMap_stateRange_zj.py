"""

"""
import nltk
import cjson
import csv

state_code = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]
map = { "AK":"Alaska", "AL":"Alabama", "AR":"Arkansas", "AZ":"Arizona", "CA":"California", "CO":"Colorado", "CT":"Connecticut", "DE":"Delaware", "FL":"Florida", "GA":"Georgia", "HI":"Hawaii", "IA":"Iowa", "ID":"Idaho", "IL":"Illinois", "IN":"Indiana", "KS":"Kansas", "KY":"Kentucky", "LA":"Louisiana", "MA":"Massachusetts", "MD":"Maryland", "ME":"Maine", "MI":"Michigan", "MN":"Minnesota", "MO":"Missouri", "MS":"Mississippi", "MT":"Montana", "NC":"North Carolina", "ND":"North Dakota", "NE":"Nebraska", "NH":"New Hampshire", "NJ":"New Jersey", "NM":"New Mexico", "NV":"Nevada", "NY":"New York", "OH":"Ohio", "OK":"Oklahoma", "OR":"Oregon", "PA":"Pennsylvania", "RI":"Rhode Island", "SC":"South Carolina", "SD":"South Dakota", "TN":"Tennessee", "TX":"Texas", "UT":"Utah", "VA":"Virginia", "VT":"Vermont", "WA":"Washington", "WI":"Wisconsin", "WV":"West Virginia", "WY":"Wyoming"}

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
        delete_list = []
        for st in self.state:
            if not st in state_code:
                delete_list.append(st)
        for dl in delete_list:
            self.state.pop(dl)
        print self.state
        
        for key in map:
            if key not in self.state:
                self.state.update({key:0})        
        with open('texas.csv', 'wb') as csvfile:
            for key in self.state:
                stateFullName = map[key]
                csvfile.write(stateFullName+","+str(self.state[key])+"\n")

        
def main():
    mytopic = topic()
    mytopic.read_user_list("/Users/zhijiaoliu/Documents/PythonZL/test/texas.json")
    
    
if __name__ == "__main__":
    main()
