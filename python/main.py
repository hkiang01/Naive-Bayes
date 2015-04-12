import sys, getopt
from Digit import *
from math import log

debug_small = True
debug_large = False
number_to_test = 1000
sample_size = 5000
test_size = 1000
threshold = 0.55

masterList = [] # full list of training Digits from given problem
testList = [] # full list of test Digits 
digitDB = [] # groups of digits (grouped by similartiy)
testLabels = []

# in order of digit classes (0-9)
llhList = [] # likelihood arrays for each class
classSizes = [] # size of each class
classPriors = [] # priors for each class
mapClassicication = []

V = 2
k = 25

def parse(filename):
	f = open(filename, "r") #opens trainingimages
	
	# parsing
	for i in xrange (0, sample_size):    
		currList = [] #the array of lines for each Digit
		curr_digit = Digit() 
		for i in xrange(NUM_ROWS):
		    currline = f.readline()
		    currList.append(currline)
		curr_digit.number = currList
		curr_digit.processFeatures()
		masterList.append(curr_digit)
	
	f.close()
	
	#debugging prints
	if(debug_small):
		for digit in xrange(number_to_test-1,number_to_test):
			masterList[digit].printNumber()
			masterList[digit].printFeatures()

	if(debug_large):
		counter = 0
		for digit in xrange(0, (len(masterList)-1)):
			print masterList[counter].calcSimilarityHeuristic(masterList[counter+1])
			counter+=1
			print "Counter", counter

def parseTestDigits(filename):
	f = open(filename, "r") #opens testimages
	for i in xrange(0, test_size):
		currList = [] # the array of lines for each Digit
		curr_digit = Digit()
		for i in xrange(NUM_ROWS):
			currline = f.readline()
			currList.append(currline)
		curr_digit.number= currList
		curr_digit.processFeatures()
		testList.append(curr_digit)
	f.close()

def printTestDigits():
	for digit in testList:
		digit.printNumber()

def parseLabels(filename):
	f = open(filename, "r")
	for i in xrange (0, sample_size):
		curr_line = f.readline()
		testLabels.append(int(curr_line))

def trainWithLabels():

	for i in xrange (0, 10):
		temp = []
		digitDB.append(temp)

	#For each given Digit in the problem,
	counter = 0
	for digit in masterList:
		print "Counter: ", counter
		index = testLabels[counter]
		print index
		digitDB[index].append(digit)
		counter+=1

def calculateLikelihood():
	def llhGraph(digitClass):
		ret = [[0 for y in xrange(NUM_ROWS)] for x in xrange(NUM_COLS)] 
		for digit in digitClass:
			totalFeature = 0		
			for y in xrange(NUM_ROWS):
				for x in xrange(NUM_COLS):
					ret[y][x]+= (digit.features[y][x]+k/float(len(digitClass)))/float(len(digitClass)+k*V)
		return ret
		
	for digitClass in digitDB:
		llhList.append(llhGraph(digitClass))
	
	groupCounter =0
	for llhEntry in llhList:
		for row in llhEntry:
			for col in row:
				if col > threshold:
					print "=",#print "+.++",
				elif col > 2*threshold/3:
					print "-",
				else:
					print " ",#print ("%.2f" % col),
			print "\n"
		print "GroupID: ", groupCounter
		groupCounter+=1

def printDB():
	for group in digitDB:
		for digit in group:
			digit.printNumber

def calcClassSizes():
	for group in digitDB:
		classSizes.append(len(group))

def printClassSizes():
	numElements = 0
	classCounter = 0
	for classID in classSizes:
		print "Size of class", classCounter, ":", classSizes[classCounter]
		numElements += classSizes[classCounter]
		classCounter += 1
	print "There are", numElements, "numbers"

def calcPriors():
	classCounter = 0
	for classID in classSizes:
		classPriors.append(classSizes[classCounter]/float(sample_size))
		classCounter += 1

def printPriors():
		priorID = 0
		for classID in classPriors:
			print "Prior for class", priorID, ":", classPriors[priorID]
			priorID += 1

def calcMAP():
	bestPrior = -1
	bestVal = 0



def main():
	parse("trainingimages")
	parseLabels("traininglabels")
	trainWithLabels()
	calculateLikelihood()
	printDB()
	calcClassSizes()
	printClassSizes()
	calcPriors()
	printPriors()
	parseTestDigits("testimages")
	printTestDigits()
	print "\nend of main"

if __name__ == '__main__':
	main()
