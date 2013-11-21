"""

"""
import nltk
import cjson
import csv

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import os

TOPIC = 'texas'

class topic:
    def __init__(self):
        self.user_dic = {}
        self.timeInterval = {}
        
    def read_user_list(self, filename):
        os.mkdir('./'+TOPIC)

        f = open(filename, "r")
        countMonth = 0
       
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
        #print countMonth
                
        plotPoints = [[0 for d in range(24)] for h in range(31)]
        for element in self.timeInterval:
            x = int(element[0])
            y = int(element[1])
            plotPoints[x][y] = int(self.timeInterval[element])
        #print plotPoints
        
        for DATESELECT in range(1,31):
            matplotlib.rcParams['axes.unicode_minus'] = False
            fig, ax = plt.subplots()
            countDay = 0
            for i in range(24):
                countDay = countDay + plotPoints[DATESELECT][i]
            #print countDay
        
            for i in range(24):
                plotPoints[DATESELECT][i] = float(plotPoints[DATESELECT][i])/countDay
            ax.plot(plotPoints[DATESELECT]) 
            ax.set_title('Time Interval')
            plt.xlabel("Hour")
            plt.ylabel("Percentage")
 
            plt.savefig('./'+TOPIC+'/'+TOPIC+'-'+str(DATESELECT)+'.png')
 #           plt.show()        


def main():
    mytopic = topic()
    mytopic.read_user_list("/Users/zhijiaoliu/Documents/PythonZL/test/"+TOPIC+".json")
    print "Done!"
    
if __name__ == "__main__":
    main()
