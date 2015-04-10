
#Class Digit
class Digit(object):
    #define class to store the digit
    def ___init___(self): #default constructor
        self.number = []
    # reference: http://www.kosbie.net/cmu/fall-11/15-112/handouts/notes-2d-lists.html
    def printNumber(self): #digit is implicit argument
        if (self.number==[]): # null check for empty list
        	print [] # prevents crashing on accessing number[0]
        	return
        rows = len(self.number)
        cols = len(self.number[0])
        #but all rows have 28 cols, so we don't really need maxItemLength()
        for row in xrange(rows): #xrange returns xrange object
        # xrange, see: https://wiki.python.org/moin/ForLoop
        # xrange is more efficient with memory than range
        	curr_line = ""
        	for col in xrange(cols): 
        		curr_line += self.number[row][col]
        	print curr_line,