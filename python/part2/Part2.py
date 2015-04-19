from operator import itemgetter
from math import log
from operator import itemgetter

k = 1 #1 to 50
V = 2
V8 = 8

class Part2(object):

	##EMAILS
	#parsing emails
	masterTrainingEmailDictionaryList = [] # dictionaries use {} instead of []
	trainingEmailLabels = [] #each document is either spam or not spam, indexed in order

	masterTestEmailDictionaryList = [] #in order of the input
	testEmailLabels = []

	#unique keys (words) and their respective values (frequencies)
	spamEmailsDictionary = {} # dictionaries use {} instead of []
	normalEmailsDictionary = {} # dictionaries use {} instead of []
	#counters
	numSpamWords = 0
	numNormalWords = 0
	spamPrior = 0.0
	normalPrior = 0.0

	spamClassified = [] #indices for emails classified as spam
	normalClassified = [] #as normal

	MAPClassificationEmails = []
	top20WordsPerClassEmail = []
	confusionMatrixEmails = []

	##8CAT
	#parsing 8cat
	masterTraining8catDictionaryList = []
	training8catLabels = []

	masterTest8catDictionaryList = []
	test8catLabels = []

	master8catDictList = [{},{},{},{},{},{},{},{}] # list of dictionaries for each class (category)
	num8catWords = [0,0,0,0,0,0,0,0] # counters
	priors8cat = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	classified8cat = [[],[],[],[],[],[],[],[]] #indices for messages classified for each class (category)

	MAPClassification8cat = []
	confusionMatrix8cat = []


	#parse the training emails
	def parseTrainingEmails(self, filename):
		#each line is a document
		#each document: [label] [word1]:[count1] [word2]:[count2] ... [wordn]:[countn]
		#labels for email: 0 is normal, 1 is spam
		#labels for 8category: 0 is sci.space; 1 is comp.sys.ibm.pc.hardware;
		#2 is rec.sport.baseball; 3 is comp.windows.x; 4 is talk.politics.misc
		#5 is misc.forsale; 6 is rec.sport.hockey; 7 is comp.graphics

		# create dictionaries consisting of all UNIQUE words occurring in the training documents

		print "parsing training emails"
		f = open(filename, "r")
		content = f.readlines()
		f.close()
		for line in content: #for each email document
			curr_dict = {}
			# rsplit(sep[, maxsplit]]) Return a list of the words in the string, using sep as the delimiter string
			elements = line.rsplit(' ')
			curr_label = int(elements[0])
			#print "Counter:", i, "Label:",curr_label
			self.trainingEmailLabels.append(curr_label)

			#skip the first element
			#http://stackoverflow.com/questions/10079216/skip-first-entry-in-for-loop-in-python
			iterElements = iter(elements) #skip the first element
			next(iterElements) #the first element contains the label
			for elem in iterElements:
				#word:count
			    #print elem
			    temp = elem.rsplit(':')
			    key = temp[0]
			    value = int(temp[1])
			    #print "Key:", key, "Value:", value
			    curr_dict[key] = value #add entry into dictionary
			self.masterTrainingEmailDictionaryList.append(curr_dict)
		print "end of parsing training emails"

	# creates 2 dictionaries of unique words for normal and spam learning sets
	def createTrainingSpamAndNormalDictionaries(self):
		counter = 0
		for dictionary in self.masterTrainingEmailDictionaryList:
			spam = self.trainingEmailLabels[counter] # 1 if spam, 0 if normal
			for word in dictionary:
				key = word #the word
				value = dictionary.get(key) #the frequency
				print key, value, spam,
				if(spam):
					print "spam"
					value += self.spamEmailsDictionary.get(key, 0) #increase the value (frequency) by the existing entry's value, default is 0 if none is found
					self.spamEmailsDictionary[key] = value #update the entry
				else:
					print "normal"
					value += self.normalEmailsDictionary.get(key, 0) #increase the value (frequency) by the existing entry's value, default is 0 if none is found
					self.normalEmailsDictionary[key] = value #update the entry
			counter += 1

	#print the email labels
	def printTrainingEmailLabels(self):
		for label in self.trainingEmailLabels:
			print label

	#parse the test emails
	def parseTestEmails(self, filename):
		f = open(filename, "r")
		content = f.readlines()
		f.close()
		for line in content:
			curr_dict = {}
			elements = line.split(' ')
			self.testEmailLabels.append(int(elements[0]))
			iterElements = iter(elements)
			next(iterElements)
			for elem in iterElements:
				temp = elem.rsplit(':')
				key = temp[0]
				value = int(temp[1])
				curr_dict[key] = value
			self.masterTestEmailDictionaryList.append(curr_dict)

	def printTestEmailLabels(self):
		for label in self.testEmailLabels:
			print label

	#in order of input
	def printTrainingEmailDictionaries(self):
		counter = 1
		for dictionary in self.masterTrainingEmailDictionaryList:
			print "\n"
			print "Training email", counter,
			if(self.trainingEmailLabels[counter-1]==0):
				print "Normal Email"
			else:
				print "Spam Email"
			for entry in sorted(dictionary):
				print entry, dictionary[entry]
			counter += 1

	def printSpamAndNormalDictionaries(self):
		print "\n",
		print "printing unique entries in spam set"
		for word in sorted(self.spamEmailsDictionary):
			print word, self.spamEmailsDictionary.get(word)
			self.numSpamWords += self.spamEmailsDictionary.get(word) # for calcProbabilityTables
		print "\n",
		print "printing unique entries in normal set"
		for word in sorted(self.normalEmailsDictionary):
			print word, self.normalEmailsDictionary.get(word)
			self.numNormalWords += self.normalEmailsDictionary.get(word) # for calcProbabilityTables
		print "\n"

	def calcEmailProbabilityTables(self):
		print "\n",
		print "printing unique entries in spam set"
		for word in sorted(self.spamEmailsDictionary):
			curr_value = []
			curr_value.append(self.spamEmailsDictionary.get(word))
			curr_value.append((curr_value[0]+k)/float(self.numSpamWords+k*V))
			self.spamEmailsDictionary[word] = curr_value
			print word, self.spamEmailsDictionary.get(word)
		print "\n",
		print "printing unique entries in normal set"
		for word in sorted(self.normalEmailsDictionary):
			curr_value = []
			curr_value.append(self.normalEmailsDictionary.get(word))
			curr_value.append((curr_value[0]+k)/float(self.numNormalWords+k*V))
			self.normalEmailsDictionary[word] = curr_value
			print word, self.normalEmailsDictionary.get(word)

	def calcEmailPriors(self):
		self.spamPrior = self.numSpamWords / float(self.numSpamWords + self.numNormalWords)
		self.normalPrior = self.numNormalWords / float(self.numSpamWords + self.numNormalWords)
		print "Spam Prior:", self.spamPrior
		print "Normal Prior:", self.normalPrior

	def classifyTestEmails(self):
		messageIndex = 0
		for message in self.masterTestEmailDictionaryList:
			spamVal = log(self.spamPrior)
			normalVal = log(self.normalPrior)
			#P(spam|message) correlates to P(spam)*Product( P(w_i|spam) )
			for word in message:
				#print word,

				temp = self.spamEmailsDictionary.get(word)
				#print "spam", temp, type(temp),
				if(temp == None): #words not found in spam https://piazza.com/class/i56vzaj3akl4wf?cid=472
					#  1 / (the number of words in "spam" + k * V)
					#print "new word",
					#print k/float(self.numSpamWords + k*V)
					spamVal += log(k/float(self.numSpamWords + k*V)) #laplacian smoothing for new words
				else:
					spamVal += log(temp[1])
				
				temp = self.normalEmailsDictionary.get(word)
				print "normal", temp, type(temp)
				if(temp == None): #words not found in spam https://piazza.com/class/i56vzaj3akl4wf?cid=472
					#  1 / (the number of words in "spam" + k * V)
					#print "new word",
					#print k/float(self.numNormalWords + k*V)
					normalVal += log(k/float(self.numNormalWords + k*V)) #laplacian smoothing for new words
				else:
					normalVal += log(temp[1])

			bestCat = -1
			#the actual clasification
			if(spamVal > normalVal):
				self.spamClassified.append(messageIndex)
				bestCat = 1
			else:
				self.normalClassified.append(messageIndex)
				bestCat = 0

			#for confusion matrix
			testPrint = []
			testPrint.append(self.testEmailLabels[messageIndex])
			testPrint.append(bestCat)
			self.MAPClassificationEmails.append(testPrint)

			messageIndex += 1

	def printMAPClassificationEmails(self):
		print "Printing MAP Classification for emails"
		for entry in self.MAPClassificationEmails:
			print entry
		print "\n"

	def findTop20WordsPerClassEmail(self):
		print "Top 20 words in spam set with highest likelihood"
		# sorts spamEmailsDictionary by its values, greatest to least (instead of least to greatest)
		top20SpamWords = sorted(self.spamEmailsDictionary.items(), key=itemgetter(1), reverse=True)
		for topEntry in xrange(0, 20):
			print top20SpamWords[topEntry][0]
		print "\n",

		print "Top 20 in normal set with highest likelihood"
		top20NormalWords = sorted(self.normalEmailsDictionary.items(), key=itemgetter(1), reverse=True)
		for topEntry in xrange(0, 20):
			print top20NormalWords[topEntry][0]
		print "\n",
		
	def confusionMatrixEmails(self):
 		#a 2x2 matrix whose entry in row r and column c
 		#is the percentage of test images from class r
 		#that are classified as class c
 		localMatrix = []
 		for r in xrange(0,2):
 			row_entry = []
 			for c in xrange(0,2):
 				#the entry itself
 				r_count = 0
 				c_count = 0
 				for entry in self.MAPClassificationEmails:
 					if(entry[0]==r):
 						r_count += 1
 						if(entry[1]==c):
 							c_count += 1
 				val = c_count/float(r_count)
 				row_entry.append(val)
 			localMatrix.append(row_entry)
 		self.confusionMatrixEmails = localMatrix

 	def printConfusionMatrixEmails(self):
 		print "Confusion Matrix for Emails"
 		for row in self.confusionMatrixEmails:
 			for col in row:
				print ("%.6f" % col),
			print "\n",

	def calcEmailClassificationAccuracy(self):
		accuracy = 0.0
		for testIndex in self.spamClassified:
			if(self.testEmailLabels[testIndex] == 1):
				accuracy += 1
		for testIndex in self.normalClassified:
			if(self.testEmailLabels[testIndex] == 0):
				accuracy += 1
		accuracy /= len(self.masterTestEmailDictionaryList)
		accuracy *= float(100)
		print "Overall email accuracy:", accuracy, "%"

	def parseTraining8cat(self, filename):
		#each line is a document
		#each document: [label] [word1]:[count1] [word2]:[count2] ... [wordn]:[countn]
		#labels for email: 0 is normal, 1 is spam
		#labels for 8category: 0 is sci.space; 1 is comp.sys.ibm.pc.hardware;
		#2 is rec.sport.baseball; 3 is comp.windows.x; 4 is talk.politics.misc
		#5 is misc.forsale; 6 is rec.sport.hockey; 7 is comp.graphics

		# create dictionaries consisting of all UNIQUE words occurring in the training documents

		f = open(filename, "r")
		content = f.readlines()
		f.close()
		for line in content: #for each email document
			curr_dict = {}
			# rsplit(sep[, maxsplit]]) Return a list of the words in the string, using sep as the delimiter string
			elements = line.rsplit(' ')
			curr_label = int(elements[0])
			#print "Counter:", i, "Label:",curr_label
			self.training8catLabels.append(curr_label)

			#skip the first element
			#http://stackoverflow.com/questions/10079216/skip-first-entry-in-for-loop-in-python
			iterElements = iter(elements) #skip the first element
			next(iterElements) #the first element contains the label
			for elem in iterElements:
				#word:count
			    #print elem
			    temp = elem.rsplit(':')
			    key = temp[0]
			    value = int(temp[1])
			    #print "Key:", key, "Value:", value
			    curr_dict[key] = value #add entry into dictionary
			self.masterTraining8catDictionaryList.append(curr_dict)

	def getCat(self, x):
	    return {
	        0: "sci.space",
	        1: "comp.sys.ibm.pc.hardware",
	        2: "rec.sport.baseball",
	        3: "comp.windows.x",
	        4: "talk.politics.misc",
	        5: "misc.forsale",
	        6: "rec.sport.hockey",
	        7: "comp.graphics",
	    }.get(x, "unknown") # unknown is the default for an out of bounds class

	def printTraining8catLabels(self):
		for label in self.training8catLabels:
			print label

	def printTraining8catDictionaries(self):
		counter = 1
		for dictionary in self.masterTraining8catDictionaryList:
			print "\n"
			print "Training 8cat document", counter
			print self.getCat(self.training8catLabels[counter-1])
			for entry in sorted(dictionary):
				print entry, dictionary[entry]
			counter += 1

	# creates 8 dictionaries of unique words for each 8cat class
	def create8catDictionaries(self):
		counter = 0
		for dictionary in self.masterTraining8catDictionaryList:
			category = self.training8catLabels[counter]
			#print "Category", category, self.getCat(category)
			for word in dictionary:
				key = word #the word
				value = dictionary.get(key) #the frequency
				#print key, value, spam,
				value += self.master8catDictList[category].get(key, 0) #increase the value (frequency) by the existing entry's value, default is 0 if none is found
				self.master8catDictList[category][key] = value #update the entry
			counter += 1
			print ""

	def print8catDictionaries(self):
		category = 0
		for dictionary in self.master8catDictList:
			print "Printing Dictionary", category, self.getCat(category)
			for word in sorted(dictionary):
				#print word, self.master8catDictList[category].get(word)
				self.num8catWords[category] += self.master8catDictList[category].get(word, 0) # for calc8catProbabilityTables
			category += 1
			#print "\n|"

	def print8catNumWordsAll(self):
		print "\n"
		counter = 0
		for numWords in self.num8catWords:
			print self.getCat(counter), numWords
			counter +=1
		print "\n"

	def calc8catPriors(self):
		counter = 0
		total = 0
		for numCategoryWords in self.num8catWords:
			self.priors8cat[counter] = float(numCategoryWords)
			total += numCategoryWords
			counter += 1
		counter = 0
		print "total:", total
		for prior in self.priors8cat:
			prior /= total
			self.priors8cat[counter] = prior #whoops
			print "Prior for", self.getCat(counter), ":", prior
			counter += 1
		print self.priors8cat
		print "\n"

	def calc8catProbabilityTables(self):
		category = 0
		for dictionary in self.master8catDictList:
			#print "\n",
			#print "printing unique entries in spam set"
			for word in sorted(dictionary):
				curr_value = []
				curr_value.append(self.master8catDictList[category].get(word))
				curr_value.append((curr_value[0]+k)/float(self.num8catWords[category]+k*V8)) #laplacian smoothing
				self.master8catDictList[category][word] = curr_value
				#print word, self.master8catDictList[category].get(word)
			#break #first dictionary
			category += 1

	def parseTest8cat(self, filename):
		#each line is a document
		#each document: [label] [word1]:[count1] [word2]:[count2] ... [wordn]:[countn]
		#labels for email: 0 is normal, 1 is spam
		#labels for 8category: 0 is sci.space; 1 is comp.sys.ibm.pc.hardware;
		#2 is rec.sport.baseball; 3 is comp.windows.x; 4 is talk.politics.misc
		#5 is misc.forsale; 6 is rec.sport.hockey; 7 is comp.graphics

		# create dictionaries consisting of all UNIQUE words occurring in the training documents

		f = open(filename, "r")
		content = f.readlines()
		f.close()
		for line in content: #for each email document
			curr_dict = {}
			# rsplit(sep[, maxsplit]]) Return a list of the words in the string, using sep as the delimiter string
			elements = line.rsplit(' ')
			curr_label = int(elements[0])
			#print "Counter:", i, "Label:",curr_label
			self.test8catLabels.append(curr_label)

			#skip the first element
			#http://stackoverflow.com/questions/10079216/skip-first-entry-in-for-loop-in-python
			iterElements = iter(elements) #skip the first element
			next(iterElements) #the first element contains the label
			for elem in iterElements:
				#word:count
			    #print elem
			    temp = elem.rsplit(':')
			    key = temp[0]
			    value = int(temp[1])
			    #print "Key:", key, "Value:", value
			    curr_dict[key] = value #add entry into dictionary
			self.masterTest8catDictionaryList.append(curr_dict)

	def printTest8catLabels(self):
		for label in self.test8catLabels:
			print label

	def classifyTest8cat(self):
		accuracy = 0.0 #for accuracy calculation

		messageIndex = 0
		for message in self.masterTest8catDictionaryList:

			#local evaluation list for message initially filled with priors
			#print self.priors8cat
			testVals = []
			for prior in self.priors8cat: #fill local evaluation list with priors
				testVals.append(prior)
			#print "Priors:", testVals

			#iteration through each message's words
			for word in message: #iterate through each word in the message
				for category in xrange(len(self.master8catDictList)):
					temp = self.master8catDictList[category].get(word)
					if(temp==None):
						#print "New word prob:", log(k/float(self.num8catWords[category] + k*V8))
						testVals[category] += log(k/float(self.num8catWords[category] + k*V8)) #laplacian smoothing for "new" words
					else:
						#print "Trained word prob:", log(temp[1])
						testVals[category] += log(temp[1]) #
			

			#get the max testVal (best category) and classify accordingly
			bestCat = testVals.index(max(testVals))
			self.classified8cat[bestCat].append(messageIndex)

			#for confusion matrix
			testPrint = []
			testPrint.append(self.test8catLabels[messageIndex])
			testPrint.append(bestCat)
			self.MAPClassification8cat.append(testPrint)

			#debugging
			print testPrint,
			if(testPrint[0]==testPrint[1]):
				accuracy += 1
				print "correct classification"
			else:
				print ""

			messageIndex += 1

		#accuracy calculation
		accuracy /= float(messageIndex+1)
		accuracy *= float(100)
		print "Overall 8cat accuracy:", accuracy, "%"

	def printMAPClassification8cat(self):
		print "Printing MAP Classification for 8cat"
		for entry in self.MAPClassification8cat:
			print entry


	def confusionMatrix8cat(self):
 		#a 8x8 matrix whose entry in row r and column c
 		#is the percentage of test images from class r
 		#that are classified as class c
 		localMatrix = []
 		for r in xrange(0,8):
 			row_entry = []
 			for c in xrange(0,8):
 				#the entry itself
 				r_count = 0
 				c_count = 0
 				for entry in self.MAPClassification8cat:
 					if(entry[0]==r):
 						r_count += 1
 						if(entry[1]==c):
 							c_count += 1
 				val = c_count/float(r_count)
 				row_entry.append(val)
 			localMatrix.append(row_entry)
 		self.confusionMatrix8cat = localMatrix

 	def printConfusionMatrix8cat(self):
 		print "Confusion Matrix for 8cat"
 		for row in self.confusionMatrix8cat:
 			for col in row:
				print ("%.4f" % col),
			print "\n",


	def __init__(self, filename_email_training, filename_8cat_training, filename_email_test, filename_8cat_test):

		#EMAILS
		self.parseTrainingEmails(filename_email_training)
		self.createTrainingSpamAndNormalDictionaries()
		#self.printTrainingEmailLabels()
		#self.printTestEmailLabels()
		#self.printTrainingEmailDictionaries()
		self.printSpamAndNormalDictionaries()
		print "Spam words:", self.numSpamWords
		print "Normal words:",self.numNormalWords
		self.calcEmailProbabilityTables()
		self.calcEmailPriors()
		self.parseTestEmails(filename_email_test)
		#self.printTestEmailLabels()
		self.classifyTestEmails()
		self.calcEmailClassificationAccuracy()
		self.printMAPClassificationEmails()
		self.findTop20WordsPerClassEmail()
		self.confusionMatrixEmails()
		self.printConfusionMatrixEmails()

		# #8CAT
		# self.parseTraining8cat(filename_8cat_training)
		# #self.printTraining8catLabels()
		# #self.printTraining8catDictionaries()
		# self.create8catDictionaries()
		# self.print8catDictionaries()
		# #self.print8catNumWordsAll()
		# self.calc8catPriors()
		# self.calc8catProbabilityTables()
		# self.parseTest8cat(filename_8cat_test)
		# #self.printTest8catLabels()
		# self.classifyTest8cat()
		# self.printMAPClassification8cat()
		# self.confusionMatrix8cat()
		# self.printConfusionMatrix8cat()
