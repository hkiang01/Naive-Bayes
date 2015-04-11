import sys, getopt
from Digit import *

debug_small = True
debug_large = False
number_to_test = 1000
threshold = 70

masterList = [] # full list of Digits from given problem
digitDB = [] # groups of digits (grouped by similartiy)
testLabels = []

def parseLabels(filename):
	f = open(filename, "r")
	for i in xrange (0, 1000):
		curr_line = f.readline()
		testLabels.append(int(curr_line))

def parse(filename):
	f = open(filename, "r") #opens trainingimages
	
	# parsing
	for i in xrange (0, 1000):    
		currList = [] #the array of lines for each digit
		curr_digit = Digit() 
		for i in xrange(28):
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


def train():
	def appendToDB(dig):
		#Add a digit as its own group
		digitDB.append([])
		digitDB[len(digitDB)-1].append(dig)
	
	#For each given Digit in the problem,
	counter = 0
	for digit in masterList:
		print "Counter: ", counter
		maxSimilarity = -1
		maxGroupID = -1
		
		#Edge Case, first digit we ever looked at
		if len(digitDB)==0:
			appendToDB(digit)
			continue
			
		#Iteratively take a group and compare it
		groupIdx = 0
		for group in digitDB:
			curAvg = 0
			#Take the average similarity from a single group
			for element in group:
				curAvg += digit.calcSimilarityHeuristic(element)
			curAvg /= len(group)
			
			if curAvg>maxSimilarity:
				maxSimilarity = curAvg
				maxGroupID=groupIdx
			groupIdx += 1

		if maxSimilarity < threshold:
			appendToDB(digit)
		else:
			digitDB[maxGroupID].append(digit)
		counter+=1

def trainWithLabels():

	def initDB():
		for i in xrange (0, 10):
			temp = []
			digitDB.append(temp)

	initDB()
	#For each given Digit in the problem,
	counter = 0
	for digit in masterList:
		print "Counter: ", counter
		index = testLabels[counter]
		print index
		digitDB[index].append(digit)
		counter+=1

def printDB():
	for group in digitDB:
		for digit in group:
			digit.printNumber

def main():
	parse("testimages")
	parseLabels("testlabels")
	trainWithLabels()
	printDB()
	print "\nend of main"

if __name__ == '__main__':
	main()
