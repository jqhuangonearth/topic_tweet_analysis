"""
This program implement a clustering model to clustering topics
using correlation vector for each keyword
@author: Bolun Huang
"""
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error
import cjson
import json
import time

class kmeans_model:
    def __init__(self):
        self.train_vector = []
        self.cluster_labels = []
        self.rmse_vector = []
        self.test_results = {} # store results for each kmeans test
        
    def load_feature_vector(self, filename):
        f = open(filename, "r")
        self.train_vector = cjson.decode(f.readline())
        f.close()
        print len(self.train_vector)
        
    def run(self, k = 200):
        """
        run kmeans clustering models
        
        @type fold: int
        @param fold: number of iteration
        """
        self.load_feature_vector("../term_geo_tempo/term_geo_tempo_vector.json")
        X = []
        X_labels = []
        for term in self.train_vector:
            X.append(self.train_vector[term])
            X_labels.append(term)
        for i in range(1):
            start = time.clock()
            kmeans = KMeans(init='k-means++', n_clusters=k, n_init=10)
            kmeans.fit(X)
            kmeans_labels = kmeans.labels_
            #param = k_means.get_params(deep = True)
            #print param
            #print k_means_labels
            cluster_centers =  kmeans.cluster_centers_
            rmse = self.get_rmse(X, kmeans_labels, cluster_centers)
            self.rmse_vector.append([k, rmse])
            #print rmse
            #X_rmses.append([n, rmse])
            #print ward_labels
            print "done ... k = %d" %k
            end = time.clock()
            print "time ... %.2f s" %(end - start)
        
            result = []
            for i in range(len(X_labels)):
                result.append([X_labels[i], kmeans_labels[i]])
            result = sorted(result, key = lambda x : x[1])
            self.test_results.update({str(k) : result})

    def test_rmse(self):
        """
        return a vector of rmse for multiple tests
        """
        return self.rmse_vector
    
    def test_result(self):
        """
        return a dictionary of the results of multiple tests
        """
        return self.test_results
    
    def get_rmse(self, target, k_means_labels, cluster_centers):
        X_cluster = []
        for label in k_means_labels:
            X_cluster.append(cluster_centers[label])
        return mean_squared_error(target, X_cluster)
  
def save_result_to_csv(outdir = "", inobj = {}):
    if type(inobj) == dict:
        for key in inobj:
            f = open(outdir+"result_"+str(key)+".csv", "w")
            for iter in inobj[key]:
                f.write(iter[0]+","+str(iter[1])+"\n")
            f.close()
    else:
        print "ERROR: object not dict type"
    
def save_rmse_to_csv(outdir = "", filename = "", inobj = []):
    if type(inobj) == list:
        f = open(outdir+filename+".csv", "w")
        for i in range(len(inobj)):
            for j in range(len(inobj[i])):
                if j == len(inobj[i]) - 1:
                    f.write(str(inobj[i][j]) + "\n")
                else:
                    f.write(str(inobj[i][j]) + ",")
        f.close()
    else:
        print "ERROR: object not list type"

def main():
    cm = kmeans_model()
    for k in xrange(510,610,10):
        cm.run(k)
    rmse_vector = cm.test_rmse()
    result_dic = cm.test_result()
    print 
    save_result_to_csv("../results/", result_dic)
    save_rmse_to_csv("../results/", "result_rmse_09_1633", rmse_vector)
    
if __name__ == "__main__":
    main()
        
    