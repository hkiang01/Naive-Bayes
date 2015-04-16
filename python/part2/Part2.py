from operator import itemgetter

class Part2(object):

	#parsing
	masterTrainingEmailDictionaryList = [] # dictionaries use {} instead of []
	trainingEmailLabels = [] #each document is either spam or not spam, indexed in order 
	spamEmailsDictionary = {} # dictionaries use {} instead of []
	normalEmailsDictionary = {} # dictionaries use {} instead of []

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

	def printTrainingEmailDictionary(self):
		counter = 1
		for dictionary in self.masterTrainingEmailDictionaryList:
			print "\n"
			print "Training email", counter,
			if(self.trainingEmailLabels[counter-1]==0):
				print "Normal Email"
			else:
				print "Spam Email"
			for entry in dictionary:
				print entry, dictionary[entry]
			counter += 1

	# creates 2 dictionaries of unique words for normal and spam learning sets
	def createSpamAndNormalDictionaries(self):
		counter = 0
		for dictionary in self.masterTrainingEmailDictionaryList:
			for word in dictionary:
				key = word #the word
				value = dictionary.get(key) #the frequency
				spam = self.trainingEmailLabels[counter]
				#print key, value, spam,
				if(spam):
					#print "spam"
					repeatedEntry = self.spamEmailsDictionary.get(key)
					if(repeatedEntry != None): #if there is an existing entry for the key (the word)
						value += self.spamEmailsDictionary.get(key) #increase the value (frequency) by the existing entry's value
					self.spamEmailsDictionary[key] = value #update the entry
				else:
					#print "normal"
					repeatedEntry = self.normalEmailsDictionary.get(key)
					if(repeatedEntry != None): #if there is an existing entry for the key (the word)
						value += self.normalEmailsDictionary.get(key) #increase the value (frequency) by the existing entry's value
					self.normalEmailsDictionary[key] = value #update the entry
				break
			counter += 1

	def printSpamAndNormalDictionaries(self):
		print "\n",
		print "printing unique entries in spam set"
		for word in sorted(self.spamEmailsDictionary):
			print word, self.spamEmailsDictionary.get(word)
		print "\n",
		print "printing unique entries in normal set"
		for word in sorted(self.normalEmailsDictionary):
			print word, self.normalEmailsDictionary.get(word)

	def __init__(self, filename_email_training):
		self.parseTrainingEmails(filename_email_training)
		#self.printTrainingEmailLabels()
		#self.printTrainingEmailDictionary()
		self.createSpamAndNormalDictionaries()
		self.printSpamAndNormalDictionaries()

