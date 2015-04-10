from Digit import *

f = open("testimages", "r") #opens trainingimages

masterList = [] # a list of Digits

for i in range (0, 5000):    
    currList = [] #the array of lines for each digit
    curr_digit = Digit() 
    for i in range(0, 28):
        currline = f.readline()
        currList.append(currline)
    curr_digit.number = currList
    masterList.append(curr_digit)

for i in range(0,1):
    masterList[i].printNumber()


f.close()