"""
This program contains lots of utility functions to analyze the topic
for example, learn the distribution of topics, learn the temporal distribution
of topics, and learn the geo distribution of topics
@author: Bolun Huang
"""
import nltk
import cjson
import re
import os
import gzip
import json
import time
import shutil
#import util.stats as stats

TRUNK_SIZE = 3000
DIR_T = "/home/bolun/user_tweets09/"
DIR_O = "/home/bolun/terms_vector09/"
DIR_R = "/home/bolun/terms_vector09_reduced/"

class topic:
    def __init__(self):
        self.user_dic = {}
        self.term_dic = {}
    
    def generate_term_vector(self):
        term_tweets_features = ["text",
                                "created_at"]
        
        term_vector_features = ["created_at",
                                "geo_location",
                                "coordinates"]
        
        fileList = os.listdir(DIR_T)
        trunk_count = 0
        total_count = 0
        user_tweets = {}
        for fline in fileList:
            user_name = fline.split(".")[0]
            # 1,000 user_tweets file to the memory at a time
            if trunk_count < TRUNK_SIZE and user_name in self.user_dic:
                path = os.path.join(DIR_T, fline)
                tweets = []
                f = gzip.open(path, "r")
                for line in f:
                    tweet = {}
                    try:
                        data = cjson.decode(line)
                        tweet.update({key: data[key] for key in term_tweets_features})
                        geo_lo = self.get_location(data)
                        coordi = self.calculate_coordinate(data)
                        if geo_lo != None:
                            tweet.update({"geo_location" : geo_lo}) # else: no geo_location
                        else:
                            tweet.update({"geo_location" : "Unknown"}) # else: no geo_location
                        if coordi != None:
                            tweet.update({"coordinates" : coordi}) # else: no coordinates
                        else:
                            tweet.update({"coordinates" : [-1.0, -1.0]}) # else: no coordinates
                    except:
                        print "error: ", line
                        pass
                    tweets.append(tweet)
                f.close()
                user_tweets.update({user_name: {"id": self.user_dic[user_name] , "tweets": tweets}})
                trunk_count += 1
                total_count += 1
            
            if trunk_count == TRUNK_SIZE:
                trunk_count = 0
                print "generating terms: %d - %d ..." %(total_count - TRUNK_SIZE, total_count)
                # generate term vectors
                start = time.clock()
                terms_vector = {}
                for user in user_tweets:
                    for tweet in user_tweets[user]["tweets"]:
                        terms = self.process_sentence(tweet["text"])
                        for term in terms:
                            term_features = {}
                            term_features.update({"id": user_tweets[user]["id"]})
                            term_features.update({key: tweet[key] for key in term_vector_features})
                            if not term in terms_vector:
                                terms_vector.update({term : [term_features]})
                            else:
                                terms_vector[term].append(term_features)
                            if not term in self.term_dic:
                                self.term_dic.update({term:1})
                            else:
                                self.term_dic[term] += 1
                end = time.clock()
                print "...time elapsed: %.2f s" %(end - start)
                print "number to terms: ", len(terms_vector)
                
                # truncate the terms count so as to exclude some junk
                delete_list = []
                cc = 0
                minc = min(self.term_dic.values())
                for key in self.term_dic:
                        if self.term_dic[key] == minc:
                            try:
                                delete_list.append(key)
                                cc += 1
                            except:
                                pass
                        if cc > 8000:
                            break
                for item in delete_list:
                    self.term_dic.pop(item)
                    
                print "writing files..."
                # write the terms vectors to file
                start = time.clock()
                for term in terms_vector:
                    if self.term_dic.has_key(term):
                        try:
                            f = gzip.open(DIR_O+term+".json.gz", "a")
                            for vector in terms_vector[term]:
                                f.write(cjson.encode(vector) + "\n")
                        except:
                            pass
                        f.close()
                terms_vector = {}
                user_tweets = {}
                end = time.clock()
                print "...time elapsed: %.2f s" %(end - start)
                
        #ft = open("../term_dic/term_dic_09.json","w")
        #json.dump(self.term_dic, ft)
        #ft.close()
            
    """utility function to get the name of location
    """
    def get_location(self, jsonobj):
        if type(jsonobj) is dict:
            if "place" in jsonobj:
                try:
                    return jsonobj["place"]["full_name"]
                except:
                    return None
        return None
    
    """utility function to calculate coordinates [x, y] of a tweets
    notice that coordinates in geo tag is the reverse of that in
    coordinates tag and in place->coordinates tag
    """
    def calculate_coordinate(self, jsonobj):
        x = -1.0
        y = -1.0
        coord = []
        count = 0
        if not jsonobj == None and type(jsonobj) is dict:
            if "coordinates" in jsonobj:
                try:
                    coord = jsonobj["coordinates"]["coordinates"]
                    return coord
                except:
                    pass
            if "geo" in jsonobj:
                try:
                    coord = jsonobj["geo"]["coordinates"]
                    x = coord[1]
                    y = coord[0]
                    return [x, y]
                except:
                    pass
            if "place" in jsonobj:
                try:
                    if "bounding_box" in jsonobj["place"]:
                        for point in jsonobj["place"]["bounding_box"]["coordinates"]:
                            x += point[0]
                            y += point[1]
                            count += 1
                except:
                    return None
            return [x/float(count), y/float(count)]
        else:
            print "cannot calculate_coordinate() for non-dict type: ", jsonobj
        return None
    
    """
    process the sentence and return a list of lower case words/terms
    remove stopwords; remove url, '\'w'.
    """
    def process_sentence(self, text):
        try:
            # to lower case
            text = text.lower()
            # remove url
            text = re.sub(r'http:[\\/.a-z0-9]+\s?', '', text) 
            # rmove mentioned user names
            text = re.sub(r'(@\w+\s?)|(@\s+)', '', text) 
            # remove special characters
            text = re.sub(r'[\#\-\+\*\`\.\;\:\"\?\<\>\[\]\{\}\|\~\_\=\!\^\&\(\)]', '', text) 
            # remove retweet tag
            text = re.sub(r'rt\s?', '', text)
        except:
            print text
            pass
        try:
            text = nltk.word_tokenize(text)
        except:
            text = []
            pass
        words = []
        for i in range(len(text)):
            if "'" in text[i] or text[i] in nltk.corpus.stopwords.words('english'):
                pass
            else:
                words.append(text[i])
        return words
        
    def read_user_list(self, filename):
        f = open(filename, "r")
        self.user_dic = cjson.decode(f.read())
        f.close()
        
    def read_term_file(self, filename):
        term_list = []
        term_dic = {}
        term_dic_reduced = {}
        f = open(filename, "r")
        for line in f:
            term_dic = cjson.decode(line)
        f.close()
        
        #hist = stats.histogram()
        for term in term_dic:
            if term_dic[term] > 30 and term_dic[term] < 165500:
                term_dic_reduced.update({term:term_dic[term]})
        
        for term in term_dic_reduced:
            term_list.append([term, term_dic_reduced[term]])
            #hist.add(term_dic_reduced[term])
        
        minc = min(term_dic_reduced.values())
        maxc = max(term_dic_reduced.values())
        
        print minc
        print maxc
        
        term_list = sorted(term_list, key =lambda x:x[1], reverse = True)
        self.write_file(term_list, term_dic_reduced)
        
    def write_file(self, term_list = [], term_dic = {}):
        f = open("../term_dic/term_dic_09_reduced.txt","w")
        for i in range(len(term_list)):
            f.write(term_list[i][0]+"\t"+str(term_list[i][1])+"\n")
        f.close()
        f = open("../term_dic/term_dic_09_reduced.json","w")
        json.dump(term_dic, f)
        f.close()
        
    def cp_reduced_term_vector(self):
        f = open("../term_dic/term_dic_09_reduced.json","r")
        term_dic_reduced = cjson.decode(f.readline(), )
        f.close()
        count = 0
        failed_count = 0
        for term in term_dic_reduced:
            path = os.path.join(DIR_O, term+".json.gz")
            if (os.path.isfile(path)):
                shutil.copy2(path, DIR_R)
            else:
                print "file not found: ", term
                failed_count += 1
            count += 1
            if count%5000 == 0:
                print "%d copied..." %count
        print "total ", count
        print "failed", failed_count
        
def main():
    mytopic = topic()
    #mytopic.read_user_list("../user_dic/user_dic_09_wids.json")
    #print mytopic.process_sentence("#HonestyHour I'd rather not be around highly emotional people."
    #+" I didn't come from a family how wore their emotions on there's sleeves. @FredyGarcia10 "
    #+"@thatchick_macy http:\\/\\/t.co\\/DmFH97GNYy")
    #mytopic.generate_term_vector()
    #mytopic.read_term_file("../term_dic/term_dic_09.json")
    mytopic.cp_reduced_term_vector()
    
if __name__ == "__main__":
    main()