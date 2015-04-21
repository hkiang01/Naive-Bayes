from Part1 import * 
import sys

if(len(sys.argv)!=2):
	print 'Please define the number of features (2 for binary, 3 for ternary): python main.py <NumFeatures>'
	exit(1)
first = Part1("trainingimages", "traininglabels","testimages", "testlabels",int(str(sys.argv[1])))
