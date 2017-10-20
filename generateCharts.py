
# Import packages
import numpy as np
import matplotlib.pyplot as plt
import csv
import time



def importClass(fileName):
# Import class from .csv in project folder
# arg filename -- name of file
# return studentInfo -- list of dictionaries

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




def generateRandomSeatingChart(studentInfo, numGroups, groupSize):
# randomly generate seating chart for all students given number of groups and group size
# arg studentInfo -- list of dictionaries for each student
# arg numGroups -- int number of groups
# arg groupSize -- int size of groups
# return seatingChart -- numGroups x groupSize matrix of seating assignments

    # initialize empty seating chart
    seatingChart = np.zeros((numGroups,groupSize))

    # track which students have been assigned
    assigned = np.zeros(len(studentInfo), dtype = bool)

    # initialize seat/group counters
    groupNum = 0
    seatNum = 0

    # assign random seat to each student filling in seat 1 for every group, then seat 2, etc.
    for student in range(1, len(studentInfo)):
        while True:
            n = np.random.random_integers(1, len(studentInfo)-1)

            if (not assigned[n]):
                seatingChart[groupNum, seatNum] = n
                assigned[n] = True

                #debugging
                #print ("Student %d assigned to group %d, seat %d. " % (n, groupNum+1, seatNum+1))

                if(groupNum == (numGroups-1)):
                    seatNum += 1
                    groupNum = 0
                else:
                    groupNum += 1


                break


    return seatingChart


def evaluateSeatingChart(seatingChart, studentInfo, FMR):
# score seating chart based on student preferences
# arg seatingChart -- matrix of students in groups
# arg studentInfo -- list of dictionaries of student Info
# arg FMR -- dictionary of which tables in classroom are front, middle, reader
# return score -- int score of seatingChart (-1 is invalid; greater is better)

    score = 0

    for group in range(len(seatingChart)):
        negPairs = []
        for seat in range(len(seatingChart[0])):
            student = int(seatingChart[group][seat])
            negPairs.append(studentInfo[student]['NegativePairs'])

            # if any negative pair is in this group, return -1
            if student in negPairs:
                #debugging
                #print("Conflict check failed because Student %d shouldn't sit with " % student + str(studentInfo[student]['NegativePairs']) + " but their group is " + str(seatingChart[group]))
                return -1

            # if any positive pair is in this group, +1
            for pos in studentInfo[student]['PositivePairs']:
                if pos in seatingChart[group]:
                    score += 1

            # if student is sitting where they prefer, +1
            # if student is sitting the opposite of where they prefer, -2
            for loc in studentInfo[student]['LocationPref']:
                if (group+1) in FMR[loc]:
                    score += 1
                if ((loc == 'F') and ((group+1) in FMR['R'])) or ((loc == 'R') and ((group+1) in FMR['F'])):
                    score -= 2

    return score

def randomGen():
# execute and time random generation THEN conflict checking method of seating chart generation
    tStart = time.clock()
    studentInfo = importClass('StudentData.csv')
    numGroups = 6
    groupSize = 5
    classArrangement = {'F':[1,2], 'M':[3,4], 'R':[5,6]}

    seatingChart = generateRandomSeatingChart(studentInfo, numGroups, groupSize)
    score = evaluateSeatingChart(seatingChart, studentInfo, classArrangement)

    print(str(seatingChart))
    print ("Seating chart score: %d" % score)
    tEnd = time.clock()
    print(str(tEnd-tStart))

#def smartGen():


randomGen()

# To do:
# Create and comment the following functions:
#   generateValidSeatingChart
#   generateRandomSeatingChart -- DONE
#   evaluateSeatingChart -- DONE
#   exportClassesToCSV
