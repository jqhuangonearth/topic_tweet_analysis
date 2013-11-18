"""
generate user vector json file for user_dic_09.json
@author: Bolun Huang
"""

import gzip
import cjson
import os
import json

DIR_P = "/home/bolun/user_profiles09/"
DIR_T = "/home/bolun/user_tweets09/"
DIR_O = "/home/bolun/user_vectors09/"

class gen_user_vectors():

    def __init__(self, filename):
        self.user_dic = {}
        self.user_vectors = [] # a list to be loaded into mongodb
        self.filename = filename

    def gen_user_vectors(self):
        self.read_user_list(self.filename)
        print len(self.user_dic)
        count = 1
        delete_list = []
        fv = open(DIR_O+"user_vectors_09.json", "w")
        for user in self.user_dic:
            #print user, self.user_dic[user],
            #break
            """ get user profiles """
            path = os.path.join(DIR_P+user+".json.gz")
            if os.path.isfile(path):
                f = gzip.open(path, "r")
                data = cjson.decode(f.readline())
                data.update({"_id": count, "tweets_count": self.user_dic[user]["tweets_count"], "tweets":[]})
                f.close()
                
                """ get user tweets """
                patht = os.path.join(DIR_T+user+".json.gz")
                if os.path.isfile(patht):
                    f = gzip.open(patht, "r")
                    datat = []
                    for line in f:
                        tweetobj = cjson.decode(line)
                        tweet = {}
                        try:
                            tweet.update({"text" : tweetobj["text"], "created_at" : tweetobj["created_at"]})
                            tweet.update({"place" : self.get_location(tweetobj)})
                            tweet.update({"coordinates" : self.calculate_coordinate(tweetobj)})
                            tweet.update({"entities" : self.get_entities(tweetobj)})
                            datat.append(tweet)
                        except:
                            print "error in gen_user_vectors(): fail to extract tweet infomation"
                            pass
                    #print datat
                    data.update({"tweets_count": len(datat), "tweets":datat})
                    self.user_dic[user]["tweets_count"] = len(datat)
                    #print data["screen_name"], len(data["tweets"]), data["tweets_count"], data
                    f.close()
                else:
                    pass
                count += 1
                self.user_vectors.append(data)
                if count%1000 == 0:
                    print count
                if count%5000 == 0: # for every 5000 user, dump to file
                    for u in self.user_vectors:
                        try:
                            json.dump(u, fv)
                            fv.write("\n")
                        except:
                            print "error in gen_user_vectors(): fail to dump"
                    self.user_vectors = [] # clear
                    print "done writing..."
                        
            else:
                print "error in gen_user_vectors(): %s%s.json.gz not found" %(DIR_P, user)
                delete_list.append(user)
                pass

        #fv.write("]")
        fv.close()
        for user in delete_list:
            self.user_dic.pop(user)
        print "total count", count
        f = open("../user_dic/user_dic_09_wids_2.json", "w")
        json.dump(self.user_dic, f)
        f.close()

    
    """utility function to get the name of location
    """
    def get_location(self, jsonobj):
        if not jsonobj == None and type(jsonobj) is dict:
            if "place" in jsonobj:
                try:
                    return jsonobj["place"]["full_name"]
                except:
                    return "Unknown"
        else:
            print "cannot get_location() for non-dict type: ", jsonobj
        return "Unknown"
    
    """utility function to calculate coordinates [x, y] of a tweets
    notice that coordinates in geo tag is the reverse of that in
    coordinates tag and in place->coordinates tag
    """
    def calculate_coordinate(self, jsonobj):
        x = 0.0
        y = 0.0
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
                    return [-1.0, -1.0]
            return [x/float(count), y/float(count)]
        else:
            print "cannot calculate_coordinate() for non-dict type: ", jsonobj
        return [-1.0, -1.0]
    
    """
    """
    def get_entities(self, jsonobj):
        entities = {"user_mentions" : [], "hashtags": [], "urls": []} # default entity object
        if not jsonobj == None and type(jsonobj) is dict:
            if "entities" in jsonobj:
                if "user_mentions" in jsonobj["entities"] and len(jsonobj["entities"]["user_mentions"]) > 0:
                    user_mentions = {}
                    for user in jsonobj["entities"]["user_mentions"]:
                        try:
                            user_mentions = {key : user[key] for key in ["id","creen_name"]}
                            entities["user_mentions"].append(user_mentions)
                        except:
                            pass

                if "hashtags" in jsonobj and len(jsonobj["entities"]["hashtags"]) > 0:
                    tag_list = []
                    for tag in jsonobj["entities"]["hashtags"]:
                        try:
                            tag_list.append(tag["text"])
                        except:
                            pass
                    entities["hashtags"] = tag_list
                if "urls" in jsonobj and len(jsonobj["entities"]["urls"]) > 0:
                    url_list = []
                    for tag in jsonobj["entities"]["urls"]:
                        try:
                            url_list.append(tag["text"])
                        except:
                            pass
                    entities["urls"] = url_list
        else:
            print "cannot get_entities() for non-dict type: ", jsonobj
        return entities
    
    def read_user_list(self, filename):
        f = open(filename, "r")
        self.user_dic = cjson.decode(f.read())
        f.close()
        
def main():
    gnv = gen_user_vectors("../user_dic/user_dic_09_wids.json")
    gnv.gen_user_vectors()
    
if __name__ == "__main__":
    main()