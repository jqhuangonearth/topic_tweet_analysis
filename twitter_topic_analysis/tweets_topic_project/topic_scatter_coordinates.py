"""

"""
import nltk
import cjson
import csv

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class topic:
    def __init__(self):
        self.user_dic = {}
        self.state = {}
        
    def read_user_list(self, filename):
        matplotlib.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        f = open(filename, "r")
        for line in f:
           data = cjson.decode(line)
           coordinates = data["coordinates"]
           if coordinates != [-1.0, -1.0]:
               ax.plot(coordinates[0],coordinates[1], 'b.')
           #print coordinates
        f.close()
        

        
        ax.set_title('Coordinates')
        plt.show()

        
def main():
    mytopic = topic()
    mytopic.read_user_list("/Users/zhijiaoliu/Documents/PythonZL/test/texas.json")

    
    
if __name__ == "__main__":
    main()
