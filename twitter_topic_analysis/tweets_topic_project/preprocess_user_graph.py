import json
import cjson

class prepro:
    def __init__(self):
        self.user_dic = {}
        self.user_id_set = set()

    def get_user_id(self):
        f = open("D:\PythonWorkspace\user_dic_09_wids_2.json", "r")
        fout = open("D:\PythonWorkspace\user_id.json", "w")
        self.user_dic = cjson.decode(f.readline())
        f.close()
        
        for user in self.user_dic:
            #print self.user_dic[user]["id"]
            self.user_id_set.add(self.user_dic[user]["id"])
            fout.write(str(self.user_dic[user]["id"]) + "\n")
            
        fout.close()
        
    def get_user_followship(self):
        f = open("D:\PythonWorkspace\user_friends_09.json", "r")
        fout = open("D:\PythonWorkspace\user_edge.json", "w")
        
        for line in f:
            adjList = {}
            adjList = cjson.decode(line)
            for id in adjList:
                for id2 in adjList[id]:
                   #print str(id) + " " + str(id2)
                   if id2 in self.user_id_set:
                       fout.write(str(id) + " " + str(id2) + "\n")
        f.close()


def test():
    s = json.loads('{"name":"test", "type":{"name":"seq", "parameter":["1", "2"]}}')
    print s
    print s.keys()
    print s["name"]
    print s["type"]["name"]
    print s["type"]["parameter"][1]

def main():
    myprepro = prepro()
    myprepro.get_user_id()
    myprepro.get_user_followship()
    
if __name__ == "__main__":
    main()
