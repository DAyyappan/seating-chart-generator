
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


def importClassGroups(fileName):
# Import class from .csv in project folder
# arg filename -- name of file
# return studentInfo -- list of dictionaries

    #use csv to open file and skip header row
    f = open(fileName)
    csv_f = csv.reader(f)
    next(csv_f)

    #create empty dictionary
    studentInfo = [{'Name':'', 'PositivePairs':[], 'NegativePairs':[], 'AntiGroups':[], 'LocationPref':[]}]

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

        if not(row[4] == ""):
            AntiGroups = [int(pp) for pp in row[4].split(',')]
        else:
            AntiGroups = ""

        LocationPref = [lp.upper().strip() for lp in row[5].split(',')]
        newDict = {'Name':Name, 'PositivePairs':PositivePairs, 'NegativePairs':NegativePairs, 'AntiGroups':AntiGroups, 'LocationPref':LocationPref}
        studentInfo.append(newDict)

        #debugging
        #print("Student %d data: " % index + str(studentInfo[index]))

    return studentInfo


def evaluateSeatingChart(seatingChart, studentInfo, FMR):
# score seating chart based on student preferences
# arg seatingChart -- matrix of students in groups
# arg studentInfo -- list of dictionaries of student Info
# arg FMR -- dictionary of which tables in classroom are front, middle, reader
# return score -- int score of seatingChart (-1 is invalid; greater is better)

    score = 0

    for group in range(len(seatingChart)):
        negPairs = []
        # create negativePairs list for group
        for s in seatingChart[group]:
            for n in studentInfo[int(s)]['NegativePairs']:
                negPairs.append(int(n))

        # change score for each student
        for seat in range(len(seatingChart[0])):
            student = int(seatingChart[group][seat])


            if student in negPairs:
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


def generateSmartSeatingChart(studentInfo, numGroups, groupSize, FMR):
# smartly generate seating chart for all students given number of groups and group size
# arg studentInfo -- list of dictionaries for each student
# arg numGroups -- int number of groups
# arg groupSize -- int size of groups
# return score, seatingChart -- seating chart score, numGroups x groupSize matrix of VALID seating assignment

    success = False
    attempts = 0
    #assign students in order to groups until complete OR impossible
    while (success == False):
        attempts += 1
        success, seatingChart = assignSmartSeats(studentInfo, numGroups, groupSize)

    #convert chart from lists to 2-D array
    seatingChart = convertChartToMatrix(seatingChart, groupSize)

    #score chart
    score = scoreChart(studentInfo, seatingChart, FMR)
    #print("Attempt %d successful with score %d" % (attempts, score))

    return score, seatingChart

def convertChartToMatrix(seatingChart, groupSize):
# convert list of groups to 2-D array
# arg seatingChart -- list of groups
# return newSeatingChart -- numGroups x groupSize matrix

    newSeatingChart = np.zeros((len(seatingChart),groupSize))


    for group in range(len(seatingChart)):
        seat = 0
        for s in seatingChart[group]:
            newSeatingChart[group][seat] = int(s)
            seat += 1

    return newSeatingChart


def scoreChart(studentInfo, seatingChart, FMR):
# score seating chart based on student preferences and seats
# arg studentInfo -- list of dictionaries for each student
# arg seatingChart -- list of seating charts
# arg FMR -- dictionary of front/middle/rear tables
# return score -- seating chart score

    score = 0

    for group in range(len(seatingChart)):
        # change score for each student
        for seat in range(len(seatingChart[0])):
            student = int(seatingChart[group][seat])

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

def assignSmartSeats(studentInfo, numGroups, groupSize):
# smartly generate seating chart for all students given number of groups and group size
# arg studentInfo -- list of dictionaries for each student
# arg numGroups -- int number of groups
# arg groupSize -- int size of groups
# return seatingChart -- numGroups x groupSize matrix of VALID seating assignment

    numStudents = len(studentInfo)-1

    #get random seed
    student = np.random.random_integers(1, numStudents)

    # initialize empty seating chart
    seatingChart = []
    for l in range(numGroups):
        seatingChart.append(list(range(0)))

    # track which students have been assigned
    assigned = np.zeros(numStudents+1, dtype = bool)

    # initialize seat/group counters, success boolean
    groupNum = 0
    seatNum = 0
    checkGroupCounter = 0
    success = False
    negList = []
    for l in range(numGroups):
        negList.append(list(range(0)))

    while (np.sum(assigned) < numStudents):
        if (assigned[student] == False):
            if((student not in negList[groupNum]) and (len(seatingChart[groupNum]) < groupSize) and ((groupNum+1) not in studentInfo[student]['AntiGroups'])):
                seatingChart[groupNum].append(student)
                #print ("student %d assigned to group %d" % (student, groupNum))
                #print ("new seating chart = \n " + str(seatingChart))
                negList[groupNum] = appendNegs(negList[groupNum], studentInfo[int(student)]['NegativePairs'])
                groupNum, discard = stepGroups(groupNum, seatNum, numGroups)
                checkGroupCounter = 0
                assigned[student] = True
                student = np.random.random_integers(1, numStudents)
            else:
                if(checkGroupCounter == numGroups):
                    #print("failed to assign student %d" % student)
                    return success, seatingChart
                else:
                    groupNum, discard = stepGroups(groupNum, seatNum, numGroups)
                    checkGroupCounter += 1
        else:
            student = np.random.random_integers(1, numStudents)

    success = True
    return success, seatingChart


def appendNegs(negList, negativePairs):

    for n in negativePairs:
        negList.append(int(n))

    return negList

def stepGroups(groupNum, seatNum, numGroups):
    if(groupNum == (numGroups-1)):
        seatNum += 1
        groupNum = 0
    else:
        groupNum += 1

    return groupNum, seatNum

def smartGen(studentInfo):
# execute and time random generation THEN conflict checking method of seating chart generation
    numGroups = 6
    groupSize = 5
    classArrangement = {'F':[1,2], 'M':[3,4], 'R':[5,6]}

    score, seatingChart = generateSmartSeatingChart(studentInfo, numGroups, groupSize, classArrangement)

    return score, seatingChart

def appendChart(allSeatingCharts, allScores, newSeats, newScore):
# smartly generate seating chart for all students given number of groups and group size
# arg seatingCharts -- list of seating charts and scores
# arg newSeats -- new seats to be appended
# arg newScore -- score of new seating chart
# return seatingCharts -- array of seating charts and scores

    allSeatingCharts.append(newSeats)
    allScores.append(newScore)

    return allSeatingCharts, allScores



def exportToCSV(fileName, studentInfo, allSeatingCharts, allScores, top20):

    topCharts = []
    topScores = []

    for i in range(len(allScores)):
        lastChart = allSeatingCharts.pop()
        lastScore = allScores.pop()
        if (lastScore >= top20):
            topCharts.append(lastChart)
            topScores.append(lastScore)



    f = open(fileName, 'w')
    writer = csv.writer(f, delimiter = ',')

    for i in range(len(topScores)):
        writer.writerow(["Seating Chart # ", (i+1)])
        writeChart = topCharts.pop()
        writeScore = topScores.pop()
        writer.writerow(["Score = ", writeScore])
        for group in range(len(writeChart)):
            members = []
            for seat in range(len(writeChart[group])):
                student = int(writeChart[group][seat])
                if (student == 0):
                    break
                members.append(studentInfo[student]['Name'])
            writer.writerow(["Group %d: " % (group+1), members])

        writer.writerow("\n")

    f.close()




def execute():
    studentInfo = importClass('StudentData.csv')
    studentInfoGroups = importClassGroups('StudentData-wGroups.csv')
    numCharts = 100

    #smartGen
    tStart = time.clock()
    maxScore = 0
    bestSeats = []
    allSeatingCharts = []
    allScores = []
    plotx = []
    ploty = []

    for n in range(numCharts):
        score = 0
        while (score <= 0):
            score, seatingChart = smartGen(studentInfoGroups)
        if (score > maxScore):
            bestSeats = seatingChart
            maxScore = score
        if (n > 20):
            plotx.append(n)
            top20 = sorted(allScores,reverse=True)[20]
            ploty.append(top20)
        allSeatingCharts, allScores = appendChart(allSeatingCharts, allScores, seatingChart, score)

    tEnd = time.clock()
    totalTime = tEnd - tStart
    print("Best score = %d after %f seconds " % (maxScore, totalTime))
    print("Best Seating Chart:" )
    print(str(bestSeats))

    top20 = sorted(allScores,reverse=True)[20]
    print ("The top 20 charts all have scores above %d " %top20)

    plt.plot(plotx, ploty)
    plt.show()

    exportToCSV('testWrite.csv', studentInfo, allSeatingCharts, allScores, top20)


def testPythonStuff():
    testList = []
    for l in range(5):
        testList.append(list(range(0)))

    testList[1].append(2)
    print(str(testList))

execute()

# To do:
# -- Record successful seating charts
# -- Export successful charts to csv
# -- (optional) evaluate similarity of seating charts to provide variety
