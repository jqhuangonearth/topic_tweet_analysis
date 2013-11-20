import gzip
import cjson
import util.stats as stats
import json

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

def write_file(term_list):
    f = open("../term_dic/term_dic_09.txt","w")
    for i in range(len(term_list)):
        f.write(term_list[i][0]+"\t"+str(term_list[i][1])+"\n")
    f.close()
    
    
read_term_file("../term_dic/term_dic_09.json")
    