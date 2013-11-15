#coding=gbk
import threading, time, random, cjson
count = 0

f = open("../social_graph/user_friends_09.json", "r")
dic = {}
for line in f:
    data = cjson.decode(line)
    for key in data:
        dic.update({key : data[key]})
print len(dic)
f.close()


exit(0)

class Counter(threading.Thread):
    def __init__(self, lock, threadName):
        '''@summary:
        
        @param lock:
        @param threadName:
        '''
        super(Counter, self).__init__(name = threadName) 
        self.lock = lock
    
    def run(self):
        '''@summary: 
        '''
        self.lock.acquire()
        for i in xrange(10000):
            f = open("test.txt","a")
            f.write(str(i)+"\n")
            f.close()
        self.lock.release()

lock = threading.Lock()
for i in range(5): 
    Counter(lock, "thread-" + str(i)).start()
time.sleep(2) 
print count