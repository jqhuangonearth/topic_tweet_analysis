"""

"""
import nltk
import cjson
import csv

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

TOPIC = 'texas'

class topic:
    def __init__(self):
        self.user_dic = {}
        self.timeInterval = {}
        
    def read_user_list(self, filename):
        matplotlib.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        f = open(filename, "r")
        countMonth = 0
        countDay = 0
        for line in f:
           countMonth+=1
           data = cjson.decode(line)
           time = data["created_at"].split(" ")
           date = time[2]
           hour = time[3].split(":") 
           key = date,hour[0]
           if not self.timeInterval.has_key(key):
               self.timeInterval.update({key: 1})
           else:
                self.timeInterval[key] += 1
               
        f.close()
#        print countMonth
        plotPoints = [0 for h in range(31)]
        for element in self.timeInterval:
            x = int(element[0])
            plotPoints[x] = int(self.timeInterval[element])+plotPoints[x]
        del plotPoints[0]
#        print plotPoints
        totalInDay = 0
  
        for i in range(30):
            plotPoints[i] = float(plotPoints[i])/countMonth
        xz = range(1,31)        
        ax.plot(xz,plotPoints)
        ax.set_title('Time Interval')
        plt.xlabel("Date")
        plt.ylabel("Percentage")
        plt.savefig('./'+TOPIC+'/'+TOPIC+'-'+'month.png')
#        plt.show()
def main():
    mytopic = topic()
    mytopic.read_user_list("/Users/zhijiaoliu/Documents/PythonZL/test/texas.json")
    print "Done!"
    
    
if __name__ == "__main__":
    main()
