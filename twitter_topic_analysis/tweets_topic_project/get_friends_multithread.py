import ata
import cjson
import json
import gzip
import threading

auth_keys = [["#", 
"#",
"1260900631-#",
"#",],

["#",
"#",
"1260900631-#",
"#"],

["#",
"#",
"1260900631-#",
"#"],

["#",
"#",
"1260900631-#",
"#"]]

class get_friends(threading.Thread):
    def __init__(self, users, auth, lock, threadName):
        self.users = users
        self.auth = auth
        self.lock = lock
        super(get_friends, self).__init__(name = threadName)
    
    def run(self):
        access_twitter_api = ata.Main(self.auth[0], self.auth[1])
        #f_failed = open("../social_graph/failed_trails/userList_crawlfriends.txt","w")
        # https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=sitestreams&count=5000
        URL = "https://api.twitter.com/1.1/friends/ids.json"
        for i in range(len(self.users)):
            print "%d: " %(i), self.users[i]
            list_friends = []
            dict_friends = {}
            cursor = -1
            while cursor != 0:
                params = "cursor=%s&user_id=%s&count=5000" %(str(cursor), str(self.users[i]))
                try:
                    content = access_twitter_api.request(URL,
                                                         params,
                                                         self.auth[2], self.auth[3],
                                                         sleep_rate_limit_exhausted=True)
                    if content:
                        content = cjson.decode(content)
                        list_friends.extend(content['ids'])
                        print "Crawled user friends with cursor %d: %d" %(cursor, self.users[i])
                        cursor = content['next_cursor']
                    else:
                        print content
                        break
                except:
                    print "Failed at crawling user friends: %d" %(self.users[i])
                    break
            if len(list_friends) != 0:
                self.lock.acquire()
                f_write = gzip.open("../social_graph/user_friends_09.json.gz","a")
                dict_friends.update({str(self.users[i]):list_friends})
                f_write.write(cjson.encode(dict_friends)+"\n")
                f_write.close()
                self.lock.release()

def read_user_ids(filename):
    in_file = open(filename, 'r')
    line = in_file.readline()
    in_file.close()
    user_ids = []
    data = cjson.decode(line)
    for user in data:
        user_ids.append(data[user]["id"])
    return user_ids

def main():
    users = read_user_ids("../user_dic/user_dic_09_wids.json")
    lock = threading.Lock()
    user_truncated1 = users[0:len(users)/4]
    user_truncated2 = users[len(users)/4:len(users)/2]
    user_truncated3 = users[len(users)/2:3*len(users)/4]
    user_truncated4 = users[3*len(users)/4:len(users)]

    get_friends(user_truncated1, auth_keys[0], lock, "thread-" + str(1)).start()
    get_friends(user_truncated2, auth_keys[1], lock, "thread-" + str(2)).start()
    get_friends(user_truncated3, auth_keys[2], lock, "thread-" + str(3)).start()
    get_friends(user_truncated4, auth_keys[3], lock, "thread-" + str(4)).start()
    
    #output_user_files(user_friends, "../user_data/user_friends.json") 

if __name__ == "__main__":
    main()