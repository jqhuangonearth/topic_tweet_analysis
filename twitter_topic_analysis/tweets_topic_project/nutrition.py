"""
This class wraps the nutrition vectors and calculate the nutrition vector
@author: Bolun Huang
"""

class nutrition:
    def __init__(self):
        self.nutrition_dic = {} # add-up the nutrition value
        self.count_dic = {} # record the count for each date
        for i in range(30):
            if i < 9:
                self.nutrition_dic.update({"0"+str(i+1) : 0.0})
            else:
                self.nutrition_dic.update({str(i+1) : 0.0})
        for i in range(30):
            if i < 9:
                self.count_dic.update({"0"+str(i+1) : 0})
            else:
                self.count_dic.update({str(i+1) : 0})
        
        
    def add(self, val, index):
        """
        @type val: float
        @param val: w_k,j * auth(uid)
        
        @type index: integer
        @param index: index-date
        """
        if self.nutrition_dic.has_key(index):
            self.nutrition_dic[index] += val
            self.count_dic[index] += 1
        
    def get_nutrition(self):
        """
        @type nutrition_vector: a dict
        @param nutrition_vector: a nutrition vector
        """
        for key in self.count_dic:
            if self.count_dic[key] == 0:
                self.nutrition_dic[key] = 0
            else:
                self.nutrition_dic[key] = self.nutrition_dic[key]/float(self.count_dic[key])
        
        return self.nutrition_dic