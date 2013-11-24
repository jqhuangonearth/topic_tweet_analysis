import cjson
import numpy as np

class cf:
    def __init__(self):
        self.term_cv_vector = {}
        
    def read_term_cv_vector(self):
        f = open("../term_graph/term_CV_vectors_reduced_603_all1.json","r")
        self.term_cv_vector = cjson.decode(f.readline())
        f.close()
    
    def get_collaborative_rank(self, term):
        if term in self.term_cv_vector:
            rank = []
            for term2 in self.term_cv_vector:
                if term2 != term:
                    a1 = np.array(self.term_cv_vector[term])
                    a2 = np.array(self.term_cv_vector[term2])
                    temp = a1-a2
                    rank.append([term2, np.sqrt(np.sum(temp**2,0))])
            rank = sorted(rank, key = lambda x : x[1], reverse = False)
            print rank
        
def main():
    mycf = cf()
    mycf.read_term_cv_vector()
    mycf.get_collaborative_rank("obama")
    
if __name__ == "__main__":
    main()