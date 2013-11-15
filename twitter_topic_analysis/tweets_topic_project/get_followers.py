import ata
import cjson
import json
import gzip

APP_CONSUMER_KEY = "#"
APP_CONSUMER_SECRET = "#"
ACCESS_TOKEN = "1260900631-#"
ACCESS_SECRET = "#"


def read_user_ids(filename):
    in_file = open(filename, 'r')
    line = in_file.readline()
    in_file.close()
    user_ids = []
    data = cjson.decode(line)
    for user in data:
        user_ids.append(data[user]["id"])
    return user_ids

def get_user_followers(users, COUNT):
    access_twitter_api = ata.Main(APP_CONSUMER_KEY, APP_CONSUMER_SECRET)
    f_failed = open("../social_graph/failed_trails/userList_crawlfollowers.txt","w")
    # https://api.twitter.com/1.1/friends/ids.json?cursor=-1&screen_name=sitestreams&count=5000
    URL = "https://api.twitter.com/1.1/followers/ids.json"
    for i in range(len(users)):
        print "%d: " %(i+COUNT), users[i]
        dict_followers = {}
        list_followers = []
        cursor = -1
        f_write = gzip.open("../social_graph/user_followers.json.gz","a")
        while cursor != 0:
            params = "cursor=%s&user_id=%s&count=150" %(str(cursor), str(users[i]))
            try:
                content = access_twitter_api.request(URL,
                                                     params,
                                                     ACCESS_TOKEN, ACCESS_SECRET,
                                                     sleep_rate_limit_exhausted=True)
                if content:
                    content = cjson.decode(content)
                    list_followers.extend(content['ids'])
                    print "Crawled user followers with cursor %d: %d" %(cursor, users[i])
                    cursor = content['next_cursor']
                else:
                    print content
                    break
            except:
                print "Failed at crawling user followers: %d" %(users[i])
                f_failed.write(str(users[i])+"\n")
                break
        if len(list_followers) != 0:
            dict_followers.update({str(users[i]):list_followers})
            f_write.write(cjson.encode(dict_followers)+"\n")
        f_write.close()
    f_failed.close()
    #return user_tweets

def output_user_files(user_profiles, filename):
    out_file = open(filename, 'w')
    for user_profile in user_profiles:
        json.dump(user_profile, out_file)
        out_file.write("\n")
    out_file.close()

def main():
    users = read_user_ids("../user_dic/user_dic_09_wids.json")
    user_truncated = users[len(users)/2:len(users)]
    COUNT = len(users) - len(user_truncated)
    get_user_followers(user_truncated, COUNT)
    #output_user_files(user_followers, "../user_data/user_followers.json")
    
if __name__ == "__main__":
    main()