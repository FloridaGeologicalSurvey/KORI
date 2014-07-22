# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 10:22:01 2014

@author: Bassett_S
"""
def buildRawDict(header):
    rawDict = {}
    del rawHeader[6]
    for a in sorted(range(len(rawHeader))):
        rawDict[a]= rawHeader[a].lower()
    rawDict[21] = 'sv1'
    rawDict[5] = 'date_time'
    return rawDict
def buildRawDictB(header):
    rawDict = {}
    del header[6]
    for a in sorted(range(len(rawHeader))):
        rawDict[a]= rawHeader[a].lower()
    rawDict[5] = 'date_time'
    rawDict[10] = 'sv2'
    rawDict[23] = 'sv1'
    return rawDict
def invertDictionary(dictionary):
    inverse = {v:k for k,v in dictionary.items()}
    return inverse
    
import falmouth, os, datetime
falmouthWorkspace = r"C:\GISData\WKP Data\Flat Data\Original Sensor Data\Falmouth_Sorted_Sanitized_03-21-2014"
#falmouthWorkspace = r'C:\GISData\WKP Data\Flat Data\Original Sensor Data\Falmouth_import_Run_20140428'

outputWorkspace = r"C:\PythonWorkspace\falmouthCheck"
pw = raw_input("Enter Password: ")
alice = ["FGS-27951g1","wkp_hrdb","post_root",pw]
timeRange = [datetime.datetime(2005, 1, 1, 0, 0, 0), datetime.datetime(2014, 1, 1, 0, 0, 0)]

falmouthFiles = os.listdir(falmouthWorkspace)
falmouthPaths = [os.path.join(falmouthWorkspace, i) for i in falmouthFiles]

print "Classifying Raw Files"
classedFalmouth = falmouth.classifyFalmouth(falmouthPaths)
aFalmouth = classedFalmouth[0]
bFalmouth = classedFalmouth [1]
uFalmouth = classedFalmouth[2]
del classedFalmouth


#deployTableInfo = falmouth.retrieveColumnInfo(deploySQLquery, alice)
#deployTableHeader = falmouth.retrieveColumnNames(deploySQLquery, alice)
deploySQLquery = falmouth.buildSQLquery("*", "deploy_info", "NONE")
deployTable = falmouth.retrieveRows(deploySQLquery, alice)
deployTable2 = []
for i in deployTable:
    newRow = []
    for v, j in enumerate(i):
        if v == 3 or v==4:
            newRow.append(j.replace(tzinfo=None))
        else:
            newRow.append(j)
    deployTable2.append(newRow)

deployTable = deployTable2
del deployTable2
           

sqlQuery = falmouth.buildSQLquery("*", "falmouth", "NONE")
dbHeader = falmouth.retrieveColumnNames(sqlQuery, alice)

dbDict = {}
for i in range(len(dbHeader)):
    dbDict[i] = dbHeader[i]
dbInvDict = {v:k for k, v in dbDict.items()}

print "-"*30
print "Starting List A"
mismatchListA = []
for i in aFalmouth:
    rawData = falmouth.parse(i, 'data')
    rawHeader = falmouth.parse(i, 'data header')
    rawDict = buildRawDict(rawHeader)
    rawInvDict = invertDictionary(rawDict)
    rawStartEndDate = falmouth.parseDates(rawData)
    rawStartEndTimestamp = falmouth.parseTimestamps(rawData)
    rawSerial = falmouth.parse(i, "header")[0]
    utcTimestamp = [falmouth.est2utc(w) for w in rawStartEndTimestamp]
    rawDeployInfo = [rawSerial, utcTimestamp[0], utcTimestamp[1]]
    for j in deployTable:
        if rawDeployInfo[0] == j[2] and rawDeployInfo[1] >= j[3] and rawDeployInfo[2] <= j[4]:
            deployKey = j[1]
        else:
            pass
    rawData = falmouth.cast(rawData)
    dbData = falmouth.retrieveRange(utcTimestamp, deployKey, alice )
    if len(rawData)==len(dbData):
        print "Lengths match, proceeding"        
    else: print "WARNING: Lengths do not match", os.path.split(i)[1]

    for j,x in zip(rawData, dbData):
        mismatchRow = []        
        for v, k in enumerate(j):
            colName = rawDict[v]
            dbPosition = dbInvDict[colName]
            if type(k) == float and k == float(x[dbPosition]):
                pass
            elif type(k) == datetime.datetime and falmouth.est2utc(k) == x[dbPosition].replace(tzinfo=None):
                pass
            else:
                mismatchRow.append(colName)
        mismatchRow = list(set(mismatchRow))
    mismatchListA.append([i, [item for item in mismatchRow]])
    
print "-"*30
print "Starting List B"
mismatchListB = []
for i in bFalmouth:
    rawData = falmouth.parse(i, 'data')
    rawHeader = falmouth.parse(i, 'data header')
    rawDict = buildRawDictB(rawHeader)
    rawInvDict = invertDictionary(rawDict)
    rawStartEndDate = falmouth.parseDates(rawData)
    rawStartEndTimestamp = falmouth.parseTimestamps(rawData)
    rawSerial = falmouth.parse(i, "header")[0]
    utcTimestamp = [falmouth.est2utc(w) for w in rawStartEndTimestamp]
    rawDeployInfo = [rawSerial, utcTimestamp[0], utcTimestamp[1]]
    for j in deployTable:
        if rawDeployInfo[0] == j[2] and rawDeployInfo[1] >= j[3] and rawDeployInfo[2] <= j[4]:
            deployKey = j[1]
        else:
            pass
    rawData = falmouth.cast(rawData)
    dbData = falmouth.retrieveRange(utcTimestamp, deployKey, alice )
    dbData = sorted(dbData, key = lambda datetime: datetime[2])
    if len(rawData)==len(dbData):
        print "Lengths match, proceeding"
    else: print "WARNING: Lengths do not match", os.path.split(i)[1]


    for j,x in zip(rawData, dbData):
        mismatchRow = []        
        for v, k in enumerate(j):
            colName = rawDict[v]
            dbPosition = dbInvDict[colName]
            if type(k) == float and k == float(x[dbPosition]):
                pass
            elif type(k) == datetime.datetime and falmouth.est2utc(k) == x[dbPosition].replace(tzinfo=None):
                pass
            else:
                mismatchRow.append(colName)
        mismatchRow = list(set(mismatchRow))
    mismatchListB.append([i, [item for item in mismatchRow]])

for i in mismatchListA:
    if len(i[1]) > 0:
        print i[0], "\n", i[1]
for i in mismatchListB:
    if len(i[1]) > 0:
        print i[0], "\n", i[1]
##########################################
"""
mismatchListC = []
for i in mismatchListB:
    if len(i[1]) > 0:
        mismatchListC.append(i[0])

for i in mismatchListC:
    rawData = falmouth.parse(i, 'data')
    rawHeader = falmouth.parse(i, 'data header')
    rawDict = buildRawDictB(rawHeader)
    rawInvDict = invertDictionary(rawDict)
    rawStartEndDate = falmouth.parseDates(rawData)
    rawStartEndTimestamp = falmouth.parseTimestamps(rawData)
    rawSerial = falmouth.parse(i, "header")[0]
    rawDeployInfo = [rawSerial, rawStartEndTimestamp[0], rawStartEndTimestamp[1]]
    for j in deployTable:
        if rawDeployInfo[0] == j[2] and rawDeployInfo[1] >= j[3] and rawDeployInfo[2] <= j[4]:
            deployKey = j[1]
        else:
            pass
    rawData = falmouth.cast(rawData)
    dbData = falmouth.retrieveRange(rawStartEndTimestamp, deployKey, alice )
    dbData = sorted(dbData, key = lambda datetime: datetime[2])
    if len(rawData)==len(dbData):
        print os.path.split(i)[1],"lengths match, proceeding"
    else: print "WARNING: Lengths do not match"


    for j,x in zip(rawData, dbData):
        mismatchRow = []        
        for v, k in enumerate(j):
            colName = rawDict[v]
            dbPosition = dbInvDict[colName]
            if type(k) == float and k == float(x[dbPosition]):
                pass
            elif type(k) == datetime.datetime and k == x[dbPosition]:
                pass
            else:
                mismatchRow.append(colName)
                print colName, j[v], x[dbPosition]
        #mismatchRow = list(set(mismatchRow))
    #mismatchListB.append([i, [item for item in mismatchRow]]) 
"""
#for j,x in zip(rawData[0:1], dbData[0:1]):
#    mismatchRow = []        
#    for k in range(len(j)):
#        colName = rawDict[k]
#        dbPosition = dbInvDict[colName]
#        if j[k] == x[dbPosition]:
#            pass
#        else:
#            mismatchRow.append(colName)
#    mismatchRow = list(set(mismatchRow))
#mismatchList.append([i, [item for item in mismatchRow]])

        