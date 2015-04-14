from Digit import *
from math import log
import copy

k = 25
V = 2

#Class Part1
class Part1b(object):

	sample_size = 5000
	threshold = 0.55
	masterList = [] # full list of training Digits from given problem
	digitDB = [] # groups of digits (grouped by similartiy)
	testLabels = []

	# in order of digit classes (0-9)
	llhList = [] # likelihood arrays for each class
	classSizes = [] # size of each class
	classPriors = [] # priors for each class
	MAPDB = [[],[],[],[],[],[],[],[],[],[]]
	testlist = []

	def file_len(self, fname):
		return sum(1 for line in open(fname))

	def parse(self, filename):
		self.sample_size = self.file_len(filename) // NUM_ROWS
		f = open(filename, "r") #opens trainingimages

                retlist = []
		# parsing
		for i in xrange (0, self.sample_size):    
			currList = [] #the array of lines for each Digit
			curr_digit = Digit() 
			for i in xrange(NUM_ROWS):
			    currline = f.readline()
			    currList.append(currline)
			curr_digit.number = currList
			curr_digit.processFeatures()
			retlist.append(curr_digit)
		
		f.close()
		return retlist
		
	def printListOfNumbers(self):
	    for digit in self.masterList:
	        digit.printNumber()

	def parseLabels(self, filename):
		f = open(filename, "r")
		print self.sample_size
		for i in xrange (0, self.sample_size):
			curr_line = f.readline()
			self.testLabels.append(int(curr_line))

	def trainWithLabels(self):

		for i in xrange (0, 10):
			temp = []
			self.digitDB.append(temp)

		#For each given Digit in the problem,
		counter = 0
		for digit in self.masterList:
			print "Counter: ", counter
			index = self.testLabels[counter]
			print index
			digit.setProperClass(index)
			print digit.getProperClass()
			self.digitDB[index].append(digit)
			counter+=1

	def calculateLikelihood(self):
		def llhGraph(digitClass):
			ret = [[0 for y in xrange(NUM_ROWS)] for x in xrange(NUM_COLS)] 
			for digit in digitClass:
				#totalFeature = 0		
				for y in xrange(NUM_ROWS):
					for x in xrange(NUM_COLS):
						ret[y][x]+= (digit.features[y][x]+k/float(len(digitClass)))/float(len(digitClass)+k*V)
			return ret
			
		for digitClass in self.digitDB:
			self.llhList.append(llhGraph(digitClass))
		
		groupCounter =0
		for llhEntry in self.llhList:
			for row in llhEntry:
				for col in row:
					if col > self.threshold:
						print "=",#print "+.++",
					elif col > 2*(self.threshold)/3:
						print "-",
					else:
						print " ",#print ("%.2f" % col),
				print "\n"
			print "GroupID: ", groupCounter
			groupCounter+=1

	def printDB(self):
		for group in self.digitDB:
			for digit in group:
				digit.printNumber

	def calcClassSizes(self):
		for group in self.digitDB:
			self.classSizes.append(len(group))

	def printClassSizes(self):
		numElements = 0
		classCounter = 0
		for classID in self.classSizes:
			print "Size of class", classCounter, ":", self.classSizes[classCounter]
			numElements += self.classSizes[classCounter]
			classCounter += 1
		print "There are", numElements, "numbers"

	def calcPriors(self):
		classCounter = 0
		for classID in self.classSizes:
			self.classPriors.append(self.classSizes[classCounter]/float(self.sample_size))
			classCounter += 1

	def printPriors(self):
			priorID = 0
			for classID in self.classPriors:
				print "Prior for class", priorID, ":", self.classPriors[priorID]
				priorID += 1

	def mapClassification(self):
		
		print "MAPDB:"
		for digit in self.testlist:
		  temp = []
		  for i,llh in enumerate(self.llhList):
		      sum1 = log((self.classPriors[i]))
		      for y in xrange(NUM_ROWS):
		          for x in xrange(NUM_COLS):
		              case = digit.features[y][x]
		              if case==0:
		                  sum1 += float(log(1-llh[y][x]))
		              else:
		                  sum1 += float(log(llh[y][x]))

		      temp.append(sum1)
		  self.MAPDB[temp.index(max(temp))].append(digit)
		      #http://stackoverflow.com/questions/3989016/how-to-find-positions-of-the-list-maximum

	def printMap(self):
		for classID in self.MAPDB:
			for digit in classID:
				digit.printNumber()
				print counter

	def calcMAPAccuracy(self):
		accuracy = 0
		num_digits = 0
		i = 0
		for classID in self.MAPDB:
			for digit in classID:
				#print int(digit.getProperClass()), i
				if(int(digit.getProperClass()) == i):
					accuracy += 1
				num_digits += 1
			i += 1
		accuracy /= num_digits
		accuracy *= 100
		print "Accuracy:", accuracy, "%"
			
	
	def __init__(self, filename_images, filename_labels,filename_testimages):
		self.masterList = copy.deepcopy(self.parse(filename_images))
		self.parseLabels(filename_labels)
		self.trainWithLabels()
		self.calculateLikelihood()
		self.printDB()
		self.calcClassSizes()
		self.printClassSizes()
		self.calcPriors()
		self.printPriors()
		self.testlist = copy.deepcopy(self.parse(filename_testimages))
		self.mapClassification()
		self.printMap()
		#self.calcMAPAccuracy()
