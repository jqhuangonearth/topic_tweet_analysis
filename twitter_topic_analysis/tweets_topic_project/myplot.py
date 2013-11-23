"""
This program wraps functions to generate figures
@author: Bolun Huang
"""
import cjson
from pylab import rcParams
import matplotlib.pyplot as plt
import time

class myplot:
    def __init__(self):
        self.str = "myplot"
        self.nutrition_dic = {}
        self.term_dic = {}
    
    def read_term_dic(self, filename):
        f = open(filename, "r")
        term_dic = cjson.decode(f.readline())
        f.close()
        return term_dic
    
    def read_nutritions(self, filename):
        nutrition_dic = {}
        f = open(filename, "r")
        for line in f:
            data = cjson.decode(line)
            for key in data:
                if not nutrition_dic.has_key(key):
                    nutrition_dic.update({key : data[key]})
        f.close()
        return nutrition_dic
        
    
    def plot_nutrition_distribution(self, termfile, infile, outdir):
        """ 
        @param infile: input file
        @param outdir: output directory
        """
        self.term_dic = self.read_term_dic(termfile)
        self.nutrition_dic = self.read_nutritions(infile)
        term_list = [] # as a buffer
        count = 0
        start = time.clock()
        for term in self.nutrition_dic:
            if term in self.term_dic:
                nutrition_list = sorted(self.nutrition_dic[term].iteritems(), key=lambda asd:asd[0], reverse = False)
                #self.savfig_nutrition_distribution(term, nutrition_list, outdir)
                term_list.append([term, nutrition_list])
                count += 1
            if len(term_list) >= 2000:
                print "saving files..."
                for term in term_list:
                    #print term[0], term[1]
                    self.savfig_nutrition_distribution(term[0], term[1], outdir)
                term_list = [] # reset term list
                end = time.clock()
                print "done %d... %.2f s" %(count, end - start)
                start = time.clock()
                #break
        # save the last part in the list
        #exit(0)
        for term in term_list:
            self.savfig_nutrition_distribution(term[0], term[1], outdir)

    def savfig_nutrition_distribution(self, keyword, nutrition_list = [], outdir = ""):
        """
        @type nutrition_list: list
        @param nutrition_list: list of nutrition values
        """
        if nutrition_list == []:
            return False
        else:
            X = [i for i in range(len(nutrition_list))]
            y = [n[1]*100.0 for n in nutrition_list]
            X_ticks = [n[0] for n in nutrition_list]
            
            rcParams['figure.figsize'] = 12, 5
            plt.plot(y, marker="^", color="g", linewidth=2.0)
            plt.xticks(X, X_ticks)
            plt.xlim(0, 30)
            plt.grid(True)
            plt.xlabel("Date in September")
            plt.ylabel("Nutrition_Value (%)")
            plt.title("Nutrition Value Distribution - %s" %keyword)
            plt.savefig(outdir+"%s.png" %keyword,dpi=50)
            plt.clf()
        
def main():
    mplot = myplot()
    mplot.plot_nutrition_distribution("../term_dic/term_dic_09_reduced_filtered_truncated_without_0-9.json", "../term_nutrition/term_nutrition_vector_09.json", "../term_nutrition/figures/")

if __name__ == "__main__":
    main()