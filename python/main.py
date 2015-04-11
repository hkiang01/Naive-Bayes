import sys, getopt
from Digit import *

debug_small = False
debug_large = True

f = open("testimages", "r") #opens trainingimages

masterList = [] # a list of Digits

for i in xrange (0, 5000):    
    currList = [] #the array of lines for each digit
    curr_digit = Digit() 
    for i in xrange(0, 28):
        currline = f.readline()
        currList.append(currline)
    curr_digit.number = currList
    curr_digit.processFeatures()
    masterList.append(curr_digit)

if(debug_small):
	for digit in range(0,1):
	    masterList[digit].printNumber()
	    masterList[digit].printFeatures()

if(debug_large):
	counter = 0
	for digit in range(0, (len(masterList))):
		print masterList[counter].calcSimilarityHeuristic(masterList[counter+1])
		counter+=1
		print "Counter", counter


print "\nend of main"
f.close()