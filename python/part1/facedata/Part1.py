from Face import *
from math import log
from operator import itemgetter
import copy, Queue, sys
import pylab
import numpy as np
import matplotlib.pyplot as plt


k = 1
V = 2
oddsTolerance = 0.30

class Part1(object):

	sample_size = 451 #451 training faces
	threshold = 0.55
	masterList = [] # full list of training Digits from given problem
	digitDB = [] # groups of digits (grouped by similartiy)
	learnLabels = []
	testLabels = []

	# in order of digit classes (0-9)
	llhList = [] # likelihood arrays for each class
	classSizes = [] # size of each class
	classPriors = [] # priors for each class
	MAPDB = [[],[]]
	MLDB = [[],[]]

	testlist = [] # in order of the testimages
	MAPclassification = [] # each entry has 2 numbers, left is proper, right is classified
	MLclassification = []

	confusionMatrix = []
	oddsRatiosMatrices = []
	logOddsRatiosMatrices = []
	c1_list = []
	c2_list = []
	
	# in order of digit classes (0-9)
	oddsRatiosAllMatrices = []
	logOddsRatiosAllMatrices = []

	def printToHeatMap(self, data, fname):
		fig = plt.figure()

		ax = fig.add_subplot(111)

		cax = ax.matshow(data, interpolation='nearest')
		fig.colorbar(cax)
		
		#plt.show()
		plt.savefig('pictures/'+str(fname)+'.png')
		plt.close()	
		
	def file_len(self, fname):
		return sum(1 for line in open(fname))

	def parse(self, filename):
		self.sample_size = self.file_len(filename) // NUM_ROWS
		f = open(filename, "r") #opens trainingimages

        	retlist = []
		# parsing
		for i in xrange (0, self.sample_size):    
			currList = [] #the array of lines for each Digit
			curr_digit = Face() 
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
		print self.sample_size, "learning labels"
		for i in xrange (0, self.sample_size):
			curr_line = f.readline()
			self.learnLabels.append(int(curr_line))

	def parseMAPlabels(self, filename):
		f = open(filename, "r")
		print self.sample_size, "testing labels"
		for i in xrange(0, self.sample_size):
			curr_line = f.readline()
			self.testLabels.append(int(curr_line))

	def trainWithLabels(self):

		for i in xrange (0, NUM_CLASSES):
			temp = []
			self.digitDB.append(temp)

		#For each given Digit in the problem,
		counter = 0
		for digit in self.masterList:
			index = self.learnLabels[counter]
			digit.setProperClass(index)
			self.digitDB[index].append(digit)
			counter+=1

	def calculateLikelihood(self):
		def llhGraph(digitClass):
			ret = []
			for y in xrange(NUM_ROWS):
				curr_line = []
				for x in xrange(NUM_COLS):
					curr_line.append(0)
				ret.append(curr_line)

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
			print "GroupID: ", groupCounter
			for row in llhEntry:
				for col in row:
					# if col > self.threshold:
					# 	print "=",#print "+.++",
					# elif col > 2*(self.threshold)/3:
					# 	print "-",
					# else:
					# 	print " ",
					print ("%.2f" % col),
				print "\n"
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
		print "There are", numElements, "numbers in training set"

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
		index = 0
		for digit in self.testlist:
		  digit.setProperClass(self.testLabels[index])
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
		  index += 1
		      #http://stackoverflow.com/questions/3989016/how-to-find-positions-of-the-list-maximum
	
	def maxLikelihoodClassification(self):
		print "MLDB:"
		index = 0
		for digit in self.testlist:
		  digit.setProperClass(self.testLabels[index])
		  temp = []
		  for i,llh in enumerate(self.llhList):
		      sum1 = 0
		      for y in xrange(NUM_ROWS):
		          for x in xrange(NUM_COLS):
		              case = digit.features[y][x]
		              if case==0:
		                  sum1 += float(log(1-llh[y][x]))
		              else:
		                  sum1 += float(log(llh[y][x]))

		      temp.append(sum1)
		  self.MLDB[temp.index(max(temp))].append(digit)
		  index += 1
		  
	def printMap(self):
		#counter = 0
		for classID in self.MAPDB:
			#print "Size of MAP Class", counter, ":", len(self.MAPDB[counter])
			for digit in classID:
				digit.printNumber()
			#counter += 1
	
	def printML(self):
		#counter = 0
		for classID in self.MLDB:
			#print "Size of MAP Class", counter, ":", len(self.MAPDB[counter])
			for digit in classID:
				digit.printNumber()
			#counter += 1
			
	def calcMAPAccuracy(self):
		accuracy = 0
		num_digits = 0
		i = 0
		for classID in self.MAPDB:
			for digit in classID:
				#print int(digit.getProperClass()), i
				if(int(digit.getProperClass()) == int(i)):
					accuracy += 1
				num_digits += 1
	
				# for confusion matrix
				temp = []
				temp.append(int(digit.getProperClass()))
				temp.append(int(i))
				self.MAPclassification.append(temp)
				#print temp
				# each entry has 2 numbers, left is proper, right is classified

			i += 1
		accuracy /= float(num_digits)
		accuracy *= float(100)
		print "Overall accuracy:", accuracy, "%"
		
	def calcMLAccuracy(self):
		accuracy = 0
		num_digits = 0
		i = 0
		for classID in self.MLDB:
			for digit in classID:
				#print int(digit.getProperClass()), i
				if(int(digit.getProperClass()) == int(i)):
					accuracy += 1
				num_digits += 1
	
				# for confusion matrix
				temp = []
				temp.append(int(digit.getProperClass()))
				temp.append(int(i))
				self.MLclassification.append(temp)
				#print temp
				# each entry has 2 numbers, left is proper, right is classified

			i += 1
		accuracy /= float(num_digits)
		accuracy *= float(100)
		print "Overall accuracy (ML):", accuracy, "%"

	def confusionMatrix(self):
 		#a 10x10 matrix whose entry in row r and column c
 		#is the percentage of test images from class r
 		#that are classified as class c
		localMatrix = []
 		for r in xrange (0, NUM_CLASSES):
 			row_entry = []
 			for c in xrange (0, NUM_CLASSES):
 				r_count = 0
 				c_count = 0
				for entry in self.MAPclassification:
					if(entry[0] == r):
						r_count += 1
						if(entry[1] == c):
							c_count += 1
				val = c_count/float(r_count)
				#print ("%.2f" % val),
				row_entry.append(val)
			localMatrix.append(row_entry)
			#print "\n",
		self.confusionMatrix = localMatrix

	def printConfusionMatrix(self):
		print "Confusion Matrix:" 		
		for row in self.confusionMatrix:
			for col in row:
				print ("%.2f" % col),
			print "\n",
	
	def printAccuracyForEachClass(self):
		for classID in xrange(0, NUM_CLASSES):
			accuracy = self.confusionMatrix[classID][classID] # want diagonals of confusion matrix
			accuracy *= float(100)
			print "Accuracy for class", classID, ":", ("%.2f" % accuracy), "%"

	def oddsRatios(self):		
		#i and j are the respective row and column of a learned features
		#not dependent upon a test digit, but the 
		#c1 and c2 are numbers corresponding to the class
		def odds(i, j, c1, c2):
			#odds(Fij=1, c1, c2) = P(Fij=1 | c1) / P(Fij=1 | c2)
			llh_1 = self.llhList[c1]
			llh_2 = self.llhList[c2]
			numerator = float(llh_1[i][j])
			denominator = float(llh_2[i][j])
			return float(numerator / denominator) #the odds ratio

		def logodds(i, j, c1, c2):
			return float(log(odds(i, j, c1, c2)))

		#find four pairs of digits (rows, cols of confusion matrix)
		#that have the highest confusion rates
		highestFour = []
		for i in xrange(0, NUM_CLASSES):
			for j in xrange(0, NUM_CLASSES):
				highestFour.append([1-self.confusionMatrix[i][j], i, j])
				# 1 - because want highest values returned from sorted
				# sorted returns lowest values by default
		highestFour = sorted(highestFour, key=itemgetter(0))

		print "highestFour:",highestFour

		for i in xrange(0, 4):
			#print highestFour[i][1], highestFour[i][2]
			self.c1_list.append(highestFour[i][1])
			self.c2_list.append(highestFour[i][2])

		print "Highest four c1, c2 pairs"
		for i in xrange(0, 4):
			print self.c1_list[i], self.c2_list[i]
			self.printToHeatMap(self.llhList[self.c1_list[i]],"originalFirst"+str(i))
			self.printToHeatMap(self.llhList[self.c2_list[i]],"originalSecond"+str(i))
			#self.printToHeatMap(self.llhList[highestFour[i][1]],"originalFirst"+str(i))
			#self.printToHeatMap(self.llhList[highestFour[i][2]],"originalSecond"+str(i))

		#for c1 in self.c1_list:
		#	for c2 in self.c2_list:
		for idx in xrange(0,4):
			curr_matrix = []
			log_curr_matrix = []
			for i in xrange(0, NUM_ROWS):
				curr_line = []
				log_curr_line = []
				for j in xrange(0, NUM_COLS):
					#curr_line.append(odds(i, j, highestFour[idx][1], highestFour[idx][2]))
					#log_curr_line.append(logodds(i, j, highestFour[idx][1], highestFour[idx][2]))
					curr_line.append(odds(i, j, self.c1_list[idx], self.c2_list[idx]))
					log_curr_line.append(logodds(i, j, self.c1_list[idx], self.c2_list[idx]))
				curr_matrix.append(curr_line)
				log_curr_matrix.append(log_curr_line)
			self.oddsRatiosMatrices.append(curr_matrix)
			self.logOddsRatiosMatrices.append(log_curr_matrix)
		
		matrix_counter = 1
		for matrix in self.logOddsRatiosMatrices:
			self.printToHeatMap(matrix,"LogOdds"+str(self.c1_list[(matrix_counter-1)%4])+"over"+str(self.c2_list[(matrix_counter-1)%4]))
			matrix_counter+=1
			
		# all the matrices matrices (c1=c2=[0 through 9])
		for c1 in xrange(0, NUM_CLASSES):
			for c2 in xrange(0, NUM_CLASSES):
				curr_matrix = []
				log_curr_matrix = []
				for i in xrange(0, NUM_ROWS):
					curr_line = []
					log_curr_line = []
					for j in xrange(0, NUM_COLS):
						curr_line.append(odds(i, j, c1, c2))
						log_curr_line.append(logodds(i, j, c1, c2))
					curr_matrix.append(curr_line)
					log_curr_matrix.append(log_curr_line)
				self.oddsRatiosAllMatrices.append(curr_matrix)
				self.logOddsRatiosAllMatrices.append(log_curr_matrix)

	def printOddsRatiosMatrices(self):
		matrix_counter = 1
		for matrix in self.oddsRatiosMatrices:
			print "Matrix", matrix_counter, "comparing class", self.c1_list[(matrix_counter-1)//4], "with class", self.c2_list[(matrix_counter-1)%4]
			for row in matrix:
				for col in row:
					print ("%.2f" % col),
				print "\n",
			matrix_counter += 1
			print "\n"

	def printLogOddsRatiosMatrices(self):
		matrix_counter = 1
		for matrix in self.logOddsRatiosMatrices:
			print "Log Matrix", matrix_counter, "comparing class", self.c1_list[(matrix_counter-1)//4], "with class", self.c2_list[(matrix_counter-1)%4]
			for row in matrix:
				for col in row:
					print ("%.2f" % col),
				print "\n",
			matrix_counter += 1
			print "\n"

	def printLogOddsRatiosMatricesASCII(self):
		matrix_counter = 1
		
		for matrix in self.logOddsRatiosMatrices:
			print "Matrix", matrix_counter, "comparing class", self.c1_list[(matrix_counter-1)//4], "with class", self.c2_list[(matrix_counter-1)%4]
			output_string = ""
						
			for row in matrix:
				curr_line = ""
				for col in row:
					#print ("%.2f" % col),
					if(abs(1-col) < oddsTolerance):
						#close to 1
						curr_line += ' '
					elif(col<0):
						#negative log odds
						curr_line += '-'
					else:
						#positive log odds
						curr_line += '+'
				output_string += "\n"+curr_line
			matrix_counter += 1
			print output_string
			print "\n"





	def printLogOddsRatiosAllMatricesASCII(self):
		matrix_counter = 1
		for matrix in self.logOddsRatiosAllMatrices:
			print "Matrix", matrix_counter, "comparing class", (matrix_counter-1)//NUM_CLASSES, "with class",(matrix_counter-1)%NUM_CLASSES
			output_string = ""
			for row in matrix:
				curr_line = ""
				for col in row:
					#print ("%.2f" % col),
					if(abs(1-col) < oddsTolerance):
						#close to 1
						curr_line += ' '
					elif(col<0):
						#negative log odds
						curr_line += '-'
					else:
						#positive log odds
						curr_line += '+'
				output_string += "\n"+curr_line
			matrix_counter += 1
			print output_string
			print "\n"
	
	def printLogLikelihoodMapsASCII(self):
		matrix_counter = 0
		for llh_matrix in self.llhList: #for each class (0-9)
			print "Log likelihood map for", matrix_counter
			output_string = ""
			for row in llh_matrix:
				curr_line = ""
				for col in row:
					#print ("%.2f" % col),
					if(abs(1-col) < oddsTolerance):
						#close to 1
						curr_line += ' '
					elif(col<0):
						#negative log odds
						curr_line += '-'
					else:
						#positive log odds
						curr_line += '+'
				output_string += "\n"+curr_line
			matrix_counter += 1
			print output_string
		

	def __init__(self, filename_images, filename_labels,filename_testimages, filename_testlabels):
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
		self.parseMAPlabels(filename_testlabels)
		self.mapClassification()
		self.maxLikelihoodClassification()
		#self.printMap()
		#self.printML()
		self.calcMAPAccuracy()
		self.calcMLAccuracy()
		self.confusionMatrix()
		self.printConfusionMatrix()
		self.printAccuracyForEachClass()
		self.oddsRatios()
		self.printOddsRatiosMatrices()
		self.printLogOddsRatiosMatrices()
		self.printLogOddsRatiosMatricesASCII()
		#self.printLogOddsRatiosAllMatricesASCII()
		#self.printLogLikelihoodMapsASCII()
		
