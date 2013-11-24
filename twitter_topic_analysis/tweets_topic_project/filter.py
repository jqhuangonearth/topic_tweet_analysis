"""
This SCRIPT contains multiple functions to help us
filter out the keywords using TFIDF
if TFIDF < 0.001, ignore the term.
And it help us to generate term nutrition vectors
@author: Bolun Huang
"""
import cjson
import json
import os
import gzip
import nutrition
import time
import util.stats as stats
import math

def filter_tfidf():
    f = open("../term_nutrition/term_tfidf_dic_09_processed.json","r")
    term_tfidf_dic = cjson.decode(f.readline())
    f.close()
    f = open("../term_dic/term_dic_09_reduced.json","r")
    term_dic = cjson.decode(f.readline())
    delete_list = []
    for term in term_dic:
        if term not in term_tfidf_dic:
            delete_list.append(term)
    for term in delete_list:
        term_dic.pop(term)
    print len(term_dic), len(term_tfidf_dic)
    
    f.close()
    delete_list = []
    term_tfidf_list = []
    for term in term_tfidf_dic:
        sum1 = 0
        for item in term_tfidf_dic[term]:
            sum1 += term_tfidf_dic[term][item]
        if len(term_tfidf_dic[term]) == 0:
            delete_list.append(term)
            pass
        else:
            val = sum1/float(len(term_tfidf_dic[term]))
            if val > 0.001:
                term_tfidf_list.append([term, val])
            else:
                delete_list.append(term)
                pass
    for term in delete_list:
        term_tfidf_dic.pop(term)
        term_dic.pop(term)
    print len(term_dic), len(term_tfidf_dic)
        
    term_tfidf_list = sorted(term_tfidf_list, key = lambda x: x[1], reverse = True)
    f = open("../term_nutrition/term_tfidf_09_sorted_filtered.txt", "w")
    for term in term_tfidf_list:
        f.write(term[0]+" "+str(term[1])+"\n")
    f.close()
    
    f = open("../term_nutrition/term_tfidf_09_processed_filtered.json", "w")
    json.dump(term_tfidf_dic, f)
    f.close()
    
    f = open("../term_dic/term_dic_09_reduced_filtered.json", "w")
    json.dump(term_dic, f)
    f.close()


def read_term_dic(filename):
    f = open(filename, "r")
    term_dic = cjson.decode(f.readline())
    f.close()
    return term_dic

def read_term_tfidf_dic(filename):
    f = open(filename, "r")
    term_tfidf_dic = cjson.decode(f.readline())
    f.close()
    return term_tfidf_dic

def read_authority(filename):
    f = open(filename, "r")
    authorities = cjson.decode(f.readline())
    f.close()
    return authorities

def read_id_map(filename):
    f = open(filename, "r")
    id_name_map = cjson.decode(f.readline())
    f.close()
    return id_name_map


#filter_tfidf()


"""generate term nutrition vector divided by date"""
"""{ keyword : {nutrition_vector : [], }}"""

DIR_T = "/home/bolun/terms_vector09_reduced/"

def gen_term_nutrition_vector():
    """
    
    """
    term_dic = read_term_dic("../term_dic/term_dic_09_reduced_filtered.json")
    term_tfidf_dic = read_term_tfidf_dic("../term_nutrition/term_tfidf_09_processed_filtered.json")
    authorities = read_authority("../social_graph/authorities.json")
    id_name_map = read_id_map("../user_dic/id_name_map_09_wids_2.json")
    print len(term_dic), len(term_tfidf_dic), len(authorities), len(id_name_map)
    count = 0
    term_nutrition_vector = [] # buffer to store term_nutrition_vector
    start = time.clock()
    for term in term_dic:
        #print term
        nt = nutrition.nutrition()
        path = os.path.join(DIR_T, term+".json.gz")
        if os.path.isfile(path):
            #try:
                f = gzip.open(path, "r")
                for line in f:
                    tfidf = 0.0
                    data = cjson.decode(line)
                    date_index = parser_string_time(data["created_at"])
                    try:
                        tfidf = term_tfidf_dic[term][id_name_map[str(data["id"]["id"])]]
                        if str(data["id"]["id"]) in authorities:
                            auth = authorities[str(data["id"]["id"])]
                        else:
                            auth = 0.0
                    except Exception:
                        #print "ERROR", type(e), e # __str__ allows args to printed directly
                        pass
                    val = tfidf*auth
                    nt.add(val, date_index)
                f.close()
        else:
            #nt.get_nutrition() # get default vector
            pass
        term_nutrition_vector.append({term : nt.get_nutrition()})
        count += 1
        if count%5000 == 0:
            end = time.clock()
            print "%d done... %.2f s" %(count, (end - start))
            fo = open("../term_nutrition/term_nutrition_vector.json","a")
            for term in term_nutrition_vector:
                json.dump(term, fo)
                fo.write("\n")
            fo.close()
            term_nutrition_vector = []
            start = time.clock()
            
    fo = open("../term_nutrition/term_nutrition_vector.json","a") # add the last part
    for term in term_nutrition_vector:
        json.dump(term, fo)
        fo.write("\n")
    fo.close()

def read_nutrition_vector(filename):
    term_nutrition_dic = {}
    f = open(filename,"r")
    for line in f:
        data = cjson.decode(line)
        for key in data:
            if key not in term_nutrition_dic:
                term_nutrition_dic.update({key : data[key]})
    f.close()

    #print "texas", sorted(term_nutrition_dic["texas"].iteritems(), key=lambda asd:asd[0], reverse = False)
    #print "obama", sorted(term_nutrition_dic["obama"].iteritems(), key=lambda asd:asd[0], reverse = False)
    return term_nutrition_dic

def parser_string_time(str1):
        """
        @type str: String
        @param str: String repre. of time stamp
        
        @type date_hour: tuple
        @return date_hour: date and hour of the time; return -1 is unknown
        """
        return str1.split(" ")[2]

#gen_term_nutrition_vector()
#read_nutrition_vector("../term_nutrition/term_nutrition_vector.json")
"""
truncate term dic: delete those with symbols other than letters and numbers
save it as term_dic_09_reduced_filtered_truncated.json
a - z: 97 - 122
0 - 9: 48 - 57
"""
def truncate_term_dic(filename):
    f = open(filename, "r")
    term_dic = cjson.decode(f.readline())
    f.close()
    delete_list = []
    print len(term_dic)
    for term in term_dic:
        flag = 0
        for i in term:
            if (ord(i) >= 97 and ord(i) <= 122) or (ord(i) >= 48 and ord(i) <= 57):
                pass
            else:
                flag = 1 # invalid char detected!
                break
        if flag == 1:
            delete_list.append(term)
        
    for term in delete_list:
        term_dic.pop(term)
    print len(term_dic)
    f = open("../term_dic/term_dic_09_reduced_filtered_truncated.json", "w")
    json.dump(term_dic,f)
    f.close()
#truncate_term_dic("../term_dic/term_dic_09_reduced_filtered.json")
#exit(0)
"""
scale the nutrition vector to percentages, not absolute value
"""
def process_nutrition_term(filename):
    term_nutrition_dic = read_nutrition_vector(filename)
    for term in term_nutrition_dic:
        mystats = stats.histogram()
        for key in term_nutrition_dic[term]:
            mystats.add(term_nutrition_dic[term][key])
        for key in term_nutrition_dic[term]:
            if mystats.sum() == 0.0:
                term_nutrition_dic[term][key] = 0.0
            else:
                term_nutrition_dic[term][key] = term_nutrition_dic[term][key]/mystats.sum()
    f = open("../term_nutrition/term_nutrition_vector_09_2.json","w")
    json.dump(term_nutrition_dic,f)
    f.close()

def filter_emerging_term(filename):
    term_dic = read_term_dic("../term_dic/term_dic_09_reduced_filtered_truncated_without_0-9.json")
    term_nutrition_dic = read_nutrition_vector(filename)
    term_kurtosis_skewness_dic = {}
    count = 0
    for term in term_nutrition_dic:
        if term in term_dic:
            mystats = stats.histogram()
            for key in term_nutrition_dic[term]:
                mystats.add(term_nutrition_dic[term][key])
            kurtosis = mystats.kurtosis()
            skewness = mystats.skewness()
            if not kurtosis == None and not skewness == None and not mystats.sum() == 0.0:
                term_kurtosis_skewness_dic.update({term : {"mean" : mystats.avg(), "standard_dev": mystats.std(), "kurtosis" : kurtosis*mystats.max(), "skewness" : skewness*mystats.max()}})
                count += 1
    #print sorted(term_kurtosis_skewness_dic.iteritems(), key=lambda x:x[1]["kurtosis"], reverse = True)
    f = open("../term_nutrition/term_kurtosis_skewness_dic_09.json","w")
    json.dump(term_kurtosis_skewness_dic, f)
    f.close()
    print len(term_kurtosis_skewness_dic)
    f = open("../term_nutrition/term_kurtosis_skewness_09_sorted.txt","w")
    l = sorted(term_kurtosis_skewness_dic.iteritems(), key=lambda x:x[1]["mean"], reverse = True)
    f.write('{} '.format("user").ljust(15)+
            '{} '.format("mean").ljust(15)+
            '{} '.format("standard_dev").ljust(15)+
            '{} '.format("kurtosis").ljust(15)+
            '{} '.format("skewness").ljust(15)+'\n')
    for term in l:
        if not "\\" in term[0]:
            f.write('{} '.format(term[0]).ljust(15)+
                    '{} '.format(term[1]["mean"]).ljust(15)+
                    '{} '.format(term[1]["standard_dev"]).ljust(15)+
                    '{} '.format(term[1]["kurtosis"]).ljust(15)+
                    '{} '.format(term[1]["skewness"]).ljust(15)+'\n')
        else:
            term_kurtosis_skewness_dic.pop(term[0])
    print len(term_kurtosis_skewness_dic)
    f.close()
    
#process_nutrition_term("../term_nutrition/term_nutrition_vector_09.json")
#filter_emerging_term("../term_nutrition/term_nutrition_vector_09.json")

def filter_terms_using_tfidf(filename):
    f = open(filename, "r")
    term_dic = cjson.decode(f.readline())
    f.close()
    term_tfidf_dic = read_term_tfidf_dic("../term_nutrition/term_tfidf_dic_09_processed.json")
    term_tfidf_dic_new = {}
    for term in term_dic:
        try:
            term_tfidf_dic_new.update({term : term_tfidf_dic[term]})
        except:
            print "error ", term
            pass
    print len(term_dic), len(term_tfidf_dic_new)
    """f = open("../term_nutrition/term_tfidf_dic_09_3003.json", "w")
    json.dump(term_tfidf_dic_new, f)
    f.close()"""
    for term in term_tfidf_dic_new:
        count = len(term_tfidf_dic_new[term])
        summ = 0
        for item in term_tfidf_dic_new[term]:
            summ += term_tfidf_dic_new[term][item]
        term_tfidf_dic_new[term] = summ/float(count)
    f = open("../term_nutrition/term_tfidf_09_3003.txt","w")
    f.write('{} '.format("term").ljust(20)+
            '{} '.format("tfidf_score").ljust(15)+'\n')
    term_tfidf_list_new = sorted(term_tfidf_dic_new.iteritems(), key = lambda x : x[1], reverse = True)
    for term in term_tfidf_list_new:
        f.write('{} '.format(term[0]).ljust(20)+
                '{} '.format(term[1]).ljust(15)+'\n')
    f.close()    
    
#filter_terms_using_tfidf("../term_dic/term_dic_09_3003.json")

def filter_term_graph():
    f = open("../term_graph/term_graph_09_1633_truncated.txt", "r")
    flag = 0
    node_list = []
    edge_list = []
    for line in f:
        if flag == 1 and not line.startswith("#"):
            try:
                node_list.append(line)
            except:
                pass
        elif flag == 2 and not line.startswith("#"):
            try:
                edge = line.split(" ")
                edge_list.append([edge[0], edge[1], float(edge[2])])
            except:
                pass
        if line.startswith("#terms"):
            flag = 1
        elif line.startswith("#edges"):
            flag = 2

    f.close()
    print node_list
    print len(node_list), len(edge_list)
    tuple_list = [] # does not consider direction of edges
    for i in xrange(0,len(edge_list),2):
        avg = math.fsum([edge_list[i][2], edge_list[i+1][2]])/2.0 # take average of edges between two nodes
        tuple_list.append([edge_list[i][0], edge_list[i][1], avg])
    
    tuple_list = sorted(tuple_list, key = lambda x : x[2], reverse = True)
    f = open("../term_graph/tuple_list_09_1633_truncated_sorted.txt","w")
    for tup in tuple_list:
        f.write(tup[0]+" "+tup[1]+" "+str(tup[2])+"\n")
    f.close()
    print "done..tuple_list"
    edge_list = sorted(edge_list, key = lambda x : x[2], reverse = True)
    f = open("../term_graph/edge_list_09_1633_truncated_sorted.txt", "w")
    for edge in edge_list:
        f.write(edge[0]+" "+edge[1]+" "+str(edge[2])+"\n")
    f.close()

#print math.fsum([float("-inf"), float("-inf")])/2.0
#filter_term_graph()
def reduce_term_dic():
    term_dic = {} # reduced 
    f = open("../term_dic/term_list_09_1633_sorted_selected.txt","r")
    for line in f:
        data = line.split()
        term_dic.update({data[0] : int(data[1])})
    f.close()
    
    print len(term_dic)
    
    f = open("../term_dic/term_dic_09_1633.json","w")
    json.dump(term_dic, f)
    f.close()
    
#reduce_term_dic()
#exit(0)
def reduce_term_graph():
    term_dic_reduced = read_term_dic("../term_dic/term_dic_09_1633.json")
    f = open("../term_graph/term_graph_09_3003.txt", "r")
    flag = 0
    node_list = []
    edge_list = []
    for line in f:
        if flag == 1 and not line.startswith("#"):
            try:
                node_list.append(line)
            except:
                pass
        elif flag == 2 and not line.startswith("#"):
            try:
                edge = line.split(" ")
                edge_list.append([edge[0], edge[1], float(edge[2])])
            except:
                pass
        if line.startswith("#terms"):
            flag = 1
        elif line.startswith("#edges"):
            flag = 2

    f.close()
    print node_list
    print len(node_list), len(edge_list)
    edge_list_reduced = []
    for edge in edge_list:
        if edge[2] == float("-inf"):
            pass
        elif not edge[0] in term_dic_reduced or not edge[1] in term_dic_reduced:
            pass
        elif edge[2] < 0:
            pass
        elif edge[2] <= 0.5:
            pass
        else:
            edge_list_reduced.append(edge)
    print len(edge_list_reduced)
    
    f = open("../term_graph/term_graph_09_1633_truncated.txt","w")
    f.write("#terms\n")
    for term in term_dic_reduced:
        f.write(term+" "+str(term_dic_reduced[term])+"\n")
    f.write("#edges\n")
    for edge in edge_list_reduced:
        f.write(edge[0]+" "+edge[1]+" "+str(edge[2])+"\n")
    f.close()

#reduce_term_graph()
def gen_term_cv_vector():
    #term_dic = read_term_dic("../term_dic/term_dic_09_1633.json")
    term_index_dic = {} # universal index of terms
    term_cv_vector = {} # term_cv_vectors
    f = open("../term_graph/term_graph_09_1633_truncated.txt", "r")
    flag = 0
    node_list = []
    edge_list = []
    for line in f:
        if flag == 1 and not line.startswith("#"):
            try:
                data = line.split()
                node_list.append(data[0])
            except:
                pass
        elif flag == 2 and not line.startswith("#"):
            try:
                edge = line.split(" ")
                edge_list.append([edge[0], edge[1], float(edge[2])])
            except:
                pass
        if line.startswith("#terms"):
            flag = 1
        elif line.startswith("#edges"):
            flag = 2

    term_set = set()
    for edge in edge_list:
        term_set.add(edge[0])
        term_set.add(edge[1])
    print len(term_set)
    
    node_list_new = []
    for term in term_set:
        node_list_new.append(term)

    f.close()
    print node_list
    print len(node_list), len(node_list_new), len(edge_list)
    count = 0
    for node in node_list_new:
        term_index_dic.update({node:count})
        term_cv_vector.update({node:[0]*len(node_list_new)})
        count+=1
    
    for edge in edge_list:
        term_cv_vector[edge[0]][term_index_dic[edge[1]]] = edge[2]
    
    delete_list = []
    
    for term in term_cv_vector:
        term_cv_vector[term][term_index_dic[term]] = max(term_cv_vector[term])
        if max(term_cv_vector[term]) == 0:
            delete_list.append(term)
            
    for term in delete_list:
        term_cv_vector.pop(term)
    
    node_list_newer = []
    for term in term_cv_vector:
        node_list_newer.append(term)
    f = open("../results/node_list_09_603.txt", "w")
    count = 0
    for term in node_list_newer:
        f.write(term+" "+str(count)+"\n")
        count += 1
    f.close()
    print len
    
    term_cv_vector_newer = {}
    for node in node_list_newer:
        term_index_dic.update({node:count})
        term_cv_vector_newer.update({node:[0]*len(node_list_newer)})
        count+=1
    
    for edge in edge_list:
        term_cv_vector_newer[edge[0]][term_index_dic[edge[1]]] = edge[2]
    
    for term in term_cv_vector_newer:
        maximum = max(term_cv_vector_newer[term])
        if maximum != 0:
            for i in range(len(term_cv_vector_newer[term])):
                #term_cv_vector[term][i] = term_cv_vector[term][i]/maximum
                if term_cv_vector_newer[term][i] != 0:
                    term_cv_vector_newer[term][i] = 1
                print len(term_cv_vector_newer[term])
        
    f = open("../term_graph/term_CV_vectors_normalized_no0_all1_reduced.json","w")
    json.dump(term_cv_vector, f)
    f.close()

#gen_term_cv_vector()
def reduce_graph():
    node_list_603 = {}
    term_cv_vector = {}
    f = open("../results/node_list_09_603.txt", "r")
    count = 0
    for line in f:
        data = line.split()
        node_list_603.update({data[0] : count})
        term_cv_vector.update({data[0] : [0]*603})
        count += 1
    f.close()
    print len(node_list_603)
    #print node_list_603
    #print term_cv_vector
    
    #term_cv_vector = {} # term_cv_vectors
    f = open("../term_graph/term_graph_09_1633_truncated.txt", "r")
    flag = 0
    node_list = []
    edge_list = []
    for line in f:
        if flag == 1 and not line.startswith("#"):
            try:
                data = line.split()
                node_list.append(data[0])
            except:
                pass
        elif flag == 2 and not line.startswith("#"):
            try:
                edge = line.split(" ")
                edge_list.append([edge[0], edge[1], float(edge[2])])
            except:
                pass
        if line.startswith("#terms"):
            flag = 1
        elif line.startswith("#edges"):
            flag = 2
    # delete edges
    edge_list_new = []
    for i in range(len(edge_list)):
        if edge_list[i][0] not in node_list_603 or edge_list[i][1] not in node_list_603:
            pass
        else:
            edge_list_new.append(edge_list[i])
    print len(edge_list_new)
    
    for edge in edge_list_new:
        #print edge[0], edge[1]
        term_cv_vector[edge[0]][node_list_603[edge[1]]] = edge[2]
        term_cv_vector[edge[1]][node_list_603[edge[0]]] = edge[2]
    """
    for term in term_cv_vector:
        for i in range(len(term_cv_vector[term])):
            if term_cv_vector[term][i] > 0:
                term_cv_vector[term][i] = 1
    """
    f = open("../term_graph/term_CV_vectors_reduced_603_bidirectional.json","w")
    json.dump(term_cv_vector, f)
    f.close()
    
reduce_graph()
    
    
    