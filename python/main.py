import sys, getopt
from Digit import *

debug_small = True
debug_large = False
number_to_test = 1000

f = open("testimages", "r") #opens trainingimages

masterList = [] # a list of Digits

for i in xrange (0, 1000):    
    currList = [] #the array of lines for each digit
    curr_digit = Digit() 
    for i in xrange(28):
        currline = f.readline()
        currList.append(currline)
    curr_digit.number = currList
    curr_digit.processFeatures()
    masterList.append(curr_digit)

if(debug_small):
	for digit in xrange(number_to_test-1,number_to_test):
	    masterList[digit].printNumber()
	    masterList[digit].printFeatures()

if(debug_large):
	counter = 0
	for digit in xrange(0, (len(masterList))-1):
		first = masterList[counter]
		second = masterList[counter+1]
		print first.calcSimilarityHeuristic(second)
		counter+=1
		print "Counter", counter


print "\nend of main"
f.close()