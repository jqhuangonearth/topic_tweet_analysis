"""
Process data and group them into user_profile and user_tweets
@note: keep read/write the disk is time heavy
@author: Bolun Huang
"""
import json
import cjson
import gzip
import os
import time

DIR = "/home/bolun/geotweets/"
DIR_P = "/home/bolun/user_profiles09/"
DIR_T = "/home/bolun/user_tweets09/"
USER_LIMIT_MONTH = 1000000
USER_LIMIT_DAILY = 10000

class process:
    
    def __init__(self):
        self.user_dic = {}
        self.user_features = ["id",
                              "name",
                              "screen_name",
                              "description",
                              "followers_count",
                              "friends_count",
                              "created_at",
                              "statuses_count",
                              "favourites_count",
                              "listed_count"]
        
        self.tweet_features = ["created_at",
                               "text",
                               "place",
                               "entities",
                               "geo",
                               "coordinates"]
    
    def get_user_id(self):
        f = open("../user_dic/user_dic_09.json","r")
        self.user_dic = cjson.decode(f.readline())
        f.close()
        poplist = []
        for user in self.user_dic:
            path = os.path.join(DIR_P, user+".json.gz")
            if os.path.isfile(path):
                try:
                    f = gzip.open(path,"r")
                    line = f.readline()
                    data = cjson.decode(line)
                    self.user_dic[user] = {"id" : data["id"], "tweets_count" : self.user_dic[user]}
                except Exception as e:
                    print user, e
                    pass
            else:
                poplist.append(user)
        for user in poplist:
            self.user_dic.pop(user)
        print len(self.user_dic)
        f = open("../user_dic/user_dic_09_wids.json","w")
        json.dump(self.user_dic, f)
        f.close()
        
    def process(self):
        folderList = os.listdir(DIR)
        for fold_entry in folderList:
            folder_path = os.path.join(DIR, fold_entry)
            folderList_sub = os.listdir(folder_path)
            print "folder", folder_path
            for dir_entry in folderList_sub:
                start = time.clock()
                print "start time: %.2f s" %start
                user_dic_local = {}
                user_profiles = {}
                user_tweets = {}
                dir_entry_path = os.path.join(folder_path, dir_entry)
                print "folder", dir_entry_path
                sub_folderList = os.listdir(dir_entry_path)
                file_c = 0
                for entry in sub_folderList:
                    t1 = time.clock()
                    sub_entry = os.path.join(dir_entry_path, entry)
                    if os.path.isfile(sub_entry):
                        # do something
                        f = gzip.open(sub_entry, "r")
                        for line in f:
                            try:
                                data = cjson.decode(line)
                                if "place" in data and not data["place"] == None:
                                    if "country_code" in data["place"] and not data["place"]["country_code"] == None:
                                        if data["place"]["country_code"] == "US":
                                            flag = 1
                                            profile_vector = {}
                                            tweet_vector = {}
                                            try:
                                                profile_vector = {key: data["user"][key] for key in self.user_features}
                                                tweet_vector = {key: data[key] for key in self.tweet_features}
                                            except Exception as e:
                                                print e
                                                print line
                                                flag = 0
                                                pass
                                            try:
                                                if flag == 1:
                                                    if not user_dic_local.has_key(data["user"]["screen_name"]): # new user, create user profile and user tweets dic
                                                        #self.user_dic.update({data["user"]["screen_name"]: 1})
                                                        user_dic_local.update({data["user"]["screen_name"]: 1}) # update user list
                                                        user_profiles.update({data["user"]["screen_name"]: profile_vector})
                                                        user_tweets.update({data["user"]["screen_name"]: [tweet_vector]})
                                                    else: # duplicated user, append to user tweets dic
                                                        #self.user_dic[data["user"]["screen_name"]] = self.user_dic[data["user"]["screen_name"]] + 1
                                                        user_dic_local[data["user"]["screen_name"]] = user_dic_local[data["user"]["screen_name"]] + 1 # update user list
                                                        user_tweets[data["user"]["screen_name"]].append(tweet_vector)
                                                        
                                            except Exception as e:
                                                print e
                                                pass
                            except Exception as e:
                                print "json decode error", e, line
                                pass
                            
                    # this code is to maintain a limited number of very active users
                    
                    while len(user_dic_local) > USER_LIMIT_DAILY:
                        delete_list = []
                        cc = 0
                        minc = min(user_dic_local.values())
                        for key in user_dic_local:
                            if user_dic_local[key] == minc:
                                try:
                                    user_profiles.pop(key)
                                    user_tweets.pop(key)
                                    delete_list.append(key)
                                    cc += 1
                                except:
                                    pass
                            if cc > 500:
                                break
                        for user in delete_list:
                            user_dic_local.pop(user)
                    
                    t2 = time.clock()
                    print "%.2fs" %(t2-t1), len(user_dic_local),
                
                    if len(self.user_dic) == 0: #empty
                        self.user_dic.update(user_dic_local)
                    else: # merge into global user dic
                        for user in user_dic_local:
                            if self.user_dic.has_key(user):
                                self.user_dic[user] = self.user_dic[user] + user_dic_local[user]
                            else:
                                self.user_dic.update({user : user_dic_local[user]})
                                
                    while len(self.user_dic) > USER_LIMIT_MONTH:
                        delete_list = []
                        cc = 0
                        minc = min(self.user_dic.values())
                        for key in self.user_dic:
                            if self.user_dic[key] == minc:
                                try:
                                    delete_list.append(key)
                                    cc += 1
                                except:
                                    pass
                            if cc > 10000:
                                break
                        for user in delete_list:
                            self.user_dic.pop(user)
                    file_c = file_c + 1
                    print file_c
                    
                # write to the file
                tw1 = time.clock()
                for user in user_dic_local:
                    path_p = os.path.join(DIR_P, user+".json.gz")
                    path_t = os.path.join(DIR_T, user+".json.gz")
                    if not os.path.isfile(path_p):
                        fp = gzip.open(path_p, "w")
                        jstr = cjson.encode(user_profiles[user])
                        fp.write(jstr+"\n")
                        fp.close()
                        ft = gzip.open(path_t, "a")
                        for tweet in user_tweets[user]:
                            jstr = cjson.encode(tweet)
                            ft.write(jstr+"\n")
                        ft.close()
                    else:
                        ft = gzip.open(path_t, "a")
                        for tweet in user_tweets[user]:
                            jstr = cjson.encode(tweet)
                            ft.write(jstr+"\n")
                        ft.close()
                print "time to write: %.fs" %(time.clock() - tw1)
                
                end = time.clock()
                print "end time: %.2f s" %end
                print "finish processing %.2f s" %(end - start)
                print len(self.user_dic)

        try:
            f = open("../user_dic/user_dic_0809.json", "w")
            json.dump(self.user_dic, f)
            f.close()
        except Exception as e:
            print e
            pass
        
def main():
    myprocess = process()
    #myprocess.process()
    myprocess.get_user_id()
    
if __name__ == "__main__":
    main()