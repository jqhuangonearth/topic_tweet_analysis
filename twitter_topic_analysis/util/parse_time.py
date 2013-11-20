"""
This is a helper function that parse string time like
"Fri Sep 19 06:12:43 +0000 2013". This function only consider
<Date> and return an integer of <Date>; the date is in 
the range of (1, 30)
@author: Bolun Huang
"""

class time_histogram:
    
    def __init__(self):
        self.histogram_dic = {}
        for i in range(30):
            if i < 9:
                self.histogram_dic.update({"0"+str(i+1) : 0})
            else:
                self.histogram_dic.update({str(i+1) : 0})
    
    @staticmethod
    def parser_string_time(str1):
        """
        @type str: String
        @param str: String repre. of time stamp
        
        @type date_hour: tuple
        @return date_hour: date and hour of the time; return -1 is unknown
        """
        return str1.split(" ")[2]
    
    def add(self, str1):
        if self.histogram_dic.has_key(str1):
            self.histogram_dic[str1] += 1
        else:
            pass
    
    def histogram(self):
        """
        @type histogram: list
        @return: histogram of days
        """
        histogram = sorted(self.histogram_dic.iteritems(), key=lambda asd:asd[0], reverse = False) # sort dic as list
        return histogram
    
def test():
    from pymongo import Connection
    DB_SERVER = "localhost"
    DB_PORT = 27017
    DB_NAME = "topicanalysis"
    COLLECTION_TV = "term_vectors"
    connection = Connection(DB_SERVER, DB_PORT)
    db = connection[DB_NAME]
    th = time_histogram()
    it = db[COLLECTION_TV].find({"term_name" : "obama"})
    for i in it:
        time_stamp = i["time_stamp"]
        for t in time_stamp:
            th.add(time_histogram.parser_string_time(t))
    print th.histogram()
    
if __name__ == "__main__":
    test()