"""
generate the TFIDF score for each term;
in this model, a user is a document and our user set is a corpus
@author: Bolun Huang
"""
import cjson
from pymongo import Connection
import topic
import math
import time
import json

class tfidf:
    DB_SERVER = "localhost"
    DB_PORT = 27017
    DB_NAME = "topicanalysis"
    COLLECTION_TV = "term_vectors"
    COLLECTION_UV = "user_vectors"
    def __init__(self):
        self.term_dic = {}
        self.user_dic = {}
        self.USER_COUNT = 0
        self.connection = Connection(self.DB_SERVER, self.DB_PORT)
        self.db = self.connection[self.DB_NAME]
    
    def cal_tf_toDB(self):
        self.read_user_dic("../user_dic/user_dic_09_wids_2.json")
        count = 0
        start = time.clock()
        for user in self.user_dic:
            tweets = []
            it = self.db[self.COLLECTION_UV].find({"screen_name" : user})
            for i in it:
                for tweet in i["tweets"]:
                    tweets.append(tweet["text"])
            tweet_content = " ".join(tweets)
            mytopic = topic.topic()
            word_bag = mytopic.process_sentence(tweet_content)
            count_total = len(word_bag)
            word_map = {} # to store TF score
            word_map_2 = {}
            for word in word_bag:
                if not word in word_map:
                    word_map.update({word : 1})
                else:
                    word_map[word] += 1
            for word in word_map:
                word_map[word] = word_map[word]/float(count_total)
            
            """ in order to avoid special characters as key, append 'term-' to every term """
            for word in word_map:
                word_map_2.update({"term-"+word: word_map[word]})
            
            #print "term-kind"[5:]
            #print word_map["term-kind"[5:]]
            #break
            it = self.db[self.COLLECTION_UV].find({'screen_name': user})
            for i in it:
                i.update({"tf_score" : word_map_2})
                self.db[self.COLLECTION_UV].update({"screen_name": user}, i) # add tf_score
            count += 1
            if count%500 == 0:
                end = time.clock()
                print "%d users done... %.2f s.." %(count, (end - start))
                start = time.clock()
    
    def tfidf(self):
        self.read_term_dic("../term_dic/term_dic_09_reduced.json")
        start = time.clock()
        count = 0
        term_tfidf = []
        for term in self.term_dic:
            tfidf_score = {} # tfidf dicts
            it = self.db[self.COLLECTION_TV].find({"term_name" : term})
            for i in it:
                user_names = i["user_names"] # list of users
                idf = math.log(46932/float(len(user_names) + 1)) # idf
                for user in user_names:
                    iu = self.db[self.COLLECTION_UV].find({"screen_name" : user})
                    for j in iu:
                        tf_score_map = j["tf_score"]
                        if "term-"+term in tf_score_map:
                            tfidf_score.update({user : tf_score_map["term-"+term]*float(idf)})
                        else:
                            tfidf_score.update({user : 0.0})
            term_tfidf.append({term : tfidf_score})
            #it = self.db[self.COLLECTION_TV].find({"term_name" : term})
            #for i in it:
            #    i.update({"tfidf_score" : tfidf_score})
            #    self.db[self.COLLECTION_TV].update({"term_name": term}, i) # add tfidf_score
            count += 1
            #if count == 1:
            if count%500 == 0:
                end = time.clock()
                print "%d done ... %.2f s" %(count, (end - start))
                start = time.clock()
                f = open("../term_dic/term_tfidf.json", "a")
                for term in term_tfidf:
                    json.dump(term, f)
                    f.write("\n")
                f.close()
                term_tfidf = []
    
    def read_term_dic(self, filename):
        f = open(filename, "r")
        self.term_dic = cjson.decode(f.readline())
        f.close()
    
    def read_user_dic(self, filename):
        f = open(filename, "r")
        for line in f:
            self.user_dic = cjson.decode(line)
        f.close()
        self.USER_COUNT = len(self.user_dic)
        
        
def main():
    myt = tfidf()
    #myt.tfidf("../term_dic/term_dic_09_reduced.json")
    #myt.cal_tf_toDB()
    myt.tfidf()
    
if __name__ == "__main__":
    main()