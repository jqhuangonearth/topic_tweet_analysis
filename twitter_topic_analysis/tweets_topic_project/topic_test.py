import cjson
#import util.stats as stats
import json

def find_size_of_common_sublist(list1, list2):
    """
    @return: how many common elements in two lists; list has no duplicates
    """
    comm = 0
    dist = {}
    for item in list1:
        if not dist.has_key(item):
            dist.update({item : 1})
        else:
            dist[item] += 1
    for item in dist:
        if dist[item] == 2:
            comm += 1
    return comm

"""
f = open("xx.json", "w")
f.write("[")
json.dump({"user": "xxxx", "count" : 12, "tweets" : []}, f)
f.write(", ")
json.dump({"user": "xxxx", "count" : 12, "tweets" : []}, f)
f.write("]")
f.close()

f = open("xx.json", "r")
for line in f:
    print line
    print cjson.decode(line)

exit(0)
"""
"""
def read_term_file(filename):
    term_list = []
    term_dic = {}
    term_dic_new = {}
    f = open(filename, "r")
    for line in f:
        term_dic = cjson.decode(line)
    f.close()
    
    hist = stats.histogram()
    
    for term in term_dic:
        if term_dic[term] > 100:
            term_dic_new.update({term:term_dic[term]})
    
    for term in term_dic_new:
        term_list.append([term, term_dic_new[term]])
        hist.add(term_dic_new[term])
    
    minc = min(term_dic_new.values())
    maxc = max(term_dic_new.values())
    
    print minc
    print maxc
    
    term_list = sorted(term_list, key =lambda x:x[1], reverse = True)
    write_file(term_list)
"""

def write_file(term_list):
    f = open("../term_dic/term_dic_09.txt","w")
    for i in range(len(term_list)):
        f.write(term_list[i][0]+"\t"+str(term_list[i][1])+"\n")
    f.close()
    
    
#read_term_file("../term_dic/term_dic_09.json")
import time
#import numpy as np
#print np.sqrt((([1,2,4,6,7,9,0] - [3,2,6,3,8,5,2]) ** 2).mean())
f = open("../results/node_list_09_603.txt","r")
dic = {}
for line in f:
    data = line.split()
    dic.update({data[0] : int(data[1])})
f.close()
print len(dic)

f = open("../results/term_09_labels_603_kmeans.json","r")
label = cjson.decode(f.readline())
#print label
print len(label)
for labels in label:
    f = open("../results/node_list_09_603.txt","r")
    dic = {}
    for line in f:
        data = line.split()
        dic.update({data[0] : int(data[1])})
    f.close()
    for term in dic:
        dic[term] = label[labels][dic[term]]

    sorted_dic = sorted(dic.iteritems(), key = lambda x : x[1], reverse = True)
    print labels,
    for i in sorted_dic:
        print i[0], i[1]
    print
    time.sleep(2)

f.close()
