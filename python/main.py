import sys, getopt
from Digit import *

debug_small = True
debug_large = False
number_to_test = 1000
threshold = 70

masterList = [] # full list of Digits from given problem
digitDB = [] # groups of digits (grouped by similartiy)

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
	for digit in masterList:
		maxSimilarity = -1
		maxGroupID = -1
		
		#Edge Case, first digit we ever looked at
		if len(digitDB)==0:
			appendToDB(digit)
			continue
			
		#Iteratively take a group and compare it
		for groupIdx, group in digitDB:
			curAvg = 0
			#Take the average similarity from a single group
			for element in group:
				curAvg += digit.calcSimilarityHeuristic(element)
			curAvg /= len(group)
			
			if curAvg>maxSimilarity:
				maxSimilarity = curAvg
				maxGroupID=groupIdx
		
		if maxSimilarity < threshold:
			appendToDB(digit)
		else:
			digitDB[groupID].append(digit)

def main():
	parse("testimages")
	train()
	print "\nend of main"

if __name__ == '__main__':
	main()
