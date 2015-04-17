from operator import itemgetter

class Part2(object):

	#parsing emails
	masterTrainingEmailDictionaryList = [] # dictionaries use {} instead of []
	trainingEmailLabels = [] #each document is either spam or not spam, indexed in order 
	spamEmailsDictionary = {} # dictionaries use {} instead of []
	normalEmailsDictionary = {} # dictionaries use {} instead of []
	numSpamWords = 0
	numNormalWords = 0

	#parsing 8cat
	masterTraining8catDictionaryList = []
	training8catLabels = []
	master8catDictList = [{},{},{},{},{},{},{},{}] # list of dictionaries for each class (catetory)
	num8catWords = [0,0,0,0,0,0,0,0] # number of entries for each class (category)


	def parseTrainingEmails(self, filename):
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
		i = 1
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
			i += 1

	def printTrainingEmailLabels(self):
		for label in self.trainingEmailLabels:
			print label

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
			break

	# creates 2 dictionaries of unique words for normal and spam learning sets
	def createSpamAndNormalDictionaries(self):
		counter = 0
		for dictionary in self.masterTrainingEmailDictionaryList:
			spam = self.trainingEmailLabels[counter] # 1 if spam, 0 if normal
			for word in dictionary:
				key = word #the word
				value = dictionary.get(key) #the frequency
				#print key, value, spam,
				if(spam):
					#print "spam"
					value += self.spamEmailsDictionary.get(key, 0) #increase the value (frequency) by the existing entry's value, default is 0 if none is found
					self.spamEmailsDictionary[key] = value #update the entry
				else:
					#print "normal"
					value += self.normalEmailsDictionary.get(key, 0) #increase the value (frequency) by the existing entry's value, default is 0 if none is found
					self.normalEmailsDictionary[key] = value #update the entry
			counter += 1

	def printSpamAndNormalDictionaries(self):
		#print "\n",
		#print "printing unique entries in spam set"
		for word in sorted(self.spamEmailsDictionary):
			#print word, self.spamEmailsDictionary.get(word)
			self.numSpamWords += self.spamEmailsDictionary.get(word) # for calcProbabilityTables
		#print "\n",
		#print "printing unique entries in normal set"
		for word in sorted(self.normalEmailsDictionary):
			#print word, self.normalEmailsDictionary.get(word)
			self.numNormalWords += self.normalEmailsDictionary.get(word) # for calcProbabilityTables

	def calcEmailProbabilityTables(self):
		#print "\n",
		#print "printing unique entries in spam set"
		for word in sorted(self.spamEmailsDictionary):
			curr_value = []
			curr_value.append(self.spamEmailsDictionary.get(word))
			curr_value.append(curr_value[0]/float(self.numSpamWords))
			self.spamEmailsDictionary[word] = curr_value
			#print word, self.spamEmailsDictionary.get(word)
		#print "\n",
		#print "printing unique entries in normal set"
		for word in sorted(self.normalEmailsDictionary):
			curr_value = []
			curr_value.append(self.normalEmailsDictionary.get(word))
			curr_value.append(curr_value[0]/float(self.numNormalWords))
			self.normalEmailsDictionary[word] = curr_value
			#print word, self.normalEmailsDictionary.get(word)

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
		i = 1
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
			i += 1

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
	def createSpamAndNormalDictionaries(self):
		counter = 0
		for dictionary in self.masterTraining8catDictionaryList:
			category = self.training8catLabels[counter] # 1 if spam, 0 if normal
			for word in dictionary:
				key = word #the word
				value = dictionary.get(key) #the frequency
				#print key, value, spam,
				value += self.master8catDictList[category].get(key, 0) #increase the value (frequency) by the existing entry's value, default is 0 if none is found
				self.master8catDictList[category][key] = value #update the entry
			counter += 1

	def print8catDictionaries(self):
		counter = 0
		for dictionary in self.master8catDictList:
			for word in sorted(dictionary):
				print word, self.master8catDictList[counter].get(word)
				self.num8catWords[counter] += self.master8catDictList[counter].get(word, 0) # for calcProbabilityTables
			counter += 1

	def print8catNumWordsAll(self):
		print "\n"
		counter = 0
		for numWords in self.num8catWords:
			print self.getCat(counter), numWords
			counter +=1
		print "\n"

	def calc8catProbabilityTables(self):
		counter = 0
		for dictionary in self.master8catDictList:
			#print "\n",
			#print "printing unique entries in spam set"
			for word in sorted(dictionary):
				curr_value = []
				curr_value.append(self.master8catDictList[counter].get(word))
				curr_value.append(curr_value[0]/float(self.num8catWords[counter]))
				self.master8catDictList[counter][word] = curr_value
				print word, self.master8catDictList[counter].get(word)
			#break #first dictionary
			counter += 1

	def __init__(self, filename_email_training, filename_8cat_training):
		self.parseTrainingEmails(filename_email_training)
		#self.printTrainingEmailLabels()
		#self.printTrainingEmailDictionaries()
		self.createSpamAndNormalDictionaries()
		self.printSpamAndNormalDictionaries()
		print self.numSpamWords
		print self.numNormalWords
		self.calcEmailProbabilityTables()
		self.parseTraining8cat(filename_8cat_training)
		#self.printTraining8catLabels()
		self.printTraining8catDictionaries()
		self.createSpamAndNormalDictionaries()
		self.print8catDictionaries()
		self.print8catNumWordsAll()
		self.calc8catProbabilityTables()
