
# Import packages
import numpy as np
import matplotlib.pyplot as plt
import csv
import time


# Import class from .csv in project folder
# arg filename -- name of file
# return studentInfo -- list of dictionaries
def importClass(fileName):
    #use csv to open file and skip header row
    f = open(fileName)
    csv_f = csv.reader(f)
    next(csv_f)

    #create empty dictionary
    studentInfo = [{'Name':'', 'PositivePairs':[], 'NegativePairs':[], 'LocationPref':[]}]

    #parse csv to add as dictionary to list studentInfo
    for row in csv_f:
        index = int(row[0])
        Name = row[1]
        if not(row[2] == ""):
            PositivePairs = [int(pp) for pp in row[2].split(',')]
        else:
            PositivePairs = ""

        if not(row[3] == ""):
            NegativePairs = [int(np) for np in row[3].split(',')]
        else:
            NegativePairs = ""

        LocationPref = [lp.upper().strip() for lp in row[4].split(',')]
        newDict = {'Name':Name, 'PositivePairs':PositivePairs, 'NegativePairs':NegativePairs, 'LocationPref':LocationPref}
        studentInfo.append(newDict)

        #debugging
        #print("Student %d data: " % index + str(studentInfo[index]))

    return studentInfo


def randomGen():
    tStart = time.clock()
    importClass('StudentData.csv')
    tEnd = time.clock()
    print(str(tEnd-tStart))

#def smartGen():


randomGen()

# To do:
# Create and comment the following functions:
#   generateValidSeatingChart
#   generateRandomSeatingChart
#   evaluateSeatingChart
#   exportClassesToCSV
