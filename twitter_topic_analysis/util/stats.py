"""
include utility function for computing data statistics
include streaming statistical computation
@author: Bolun Huang
"""

class histogram:
    def __init__(self):
        self.bucket = []
        self._max = 0.0;
        self._min = 0.0;
        self._mean = 0.0;
        self._count = 0;
        
    def add(self, val):
        if self._count == 0:
            self._max = val
            self._min = val
            self._mean = val
            self._count = 1
        else:
            if val > self._max:
                self._max = val
            if val < self._min:
                self._min = val
            self._mean = (self._mean*self._count + val)/float(self._count+1)
            self._count += 1
        self.bucket.append(val)
    
    def min(self):
        return self._min

    def max(self):
        return self._max

    def avg(self):
        return self._mean

    def var(self):
        if self._count < 2:
            return 0.0
        return self._var / float(self._count -1)

    def std(self):
        return self.var() ** 0.5

    def total(self):
        return self._mean * self._count

    def count(self):
        return self._count

    def __str__(self):
        return "avg=%.2f, min=%d, max=%d, std=%.2f, count=%d" % (self.avg(), self.min(), self.max(), self.std(), self._count)
    
    """ return the percentile, so if argument is 90, then will return the bucket where the 90%ile falls """
    def get_percentile(self, percentile=90.0):
        count = 0
        for x in sorted(self.bucket): # sort by increasing values of the buckets
            count += float(x)/self._count
            if float(count*100.0) >= float(percentile):
                break
        return x
