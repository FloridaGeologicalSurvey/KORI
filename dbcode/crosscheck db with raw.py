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
outputWorkspace = r"C:\PythonWorkspace\falmouthCheck"
alice = ["FGS-27951g1","wkp_seth","post_root","Fgs_rocks_g1"]
timeRange = [datetime.datetime(2005, 1, 1, 0, 0, 0), datetime.datetime(2014, 1, 1, 0, 0, 0)]

falmouthFiles = os.listdir(falmouthWorkspace)
falmouthPaths = [os.path.join(falmouthWorkspace, i) for i in falmouthFiles]

classedFalmouth = falmouth.classifyFalmouth(falmouthPaths)
aFalmouth = classedFalmouth[0]
bFalmouth = classedFalmouth [1]
uFalmouth = classedFalmouth[2]
del classedFalmouth


#deployTableInfo = falmouth.retrieveColumnInfo(deploySQLquery, alice)
#deployTableHeader = falmouth.retrieveColumnNames(deploySQLquery, alice)
deploySQLquery = falmouth.buildSQLquery("*", "site_dev_deploy", "NONE")
deployTable = falmouth.retrieveRows(deploySQLquery, alice)
deployTable = falmouth.parseDeployTable(deployTable)

sqlQuery = falmouth.buildSQLquery("*", "dev_log", "NONE")
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
    rawDeployInfo = [rawSerial, rawStartEndDate[0], rawStartEndDate[1]]
    for j in deployTable:
        if rawDeployInfo[0] == j[0] and rawDeployInfo[1] >= j[1] and rawDeployInfo[2] <= j[2]:
            deployKey = j[3]
        else:
            pass
    rawData = falmouth.cast(rawData)
    dbData = falmouth.retrieveRange(rawStartEndTimestamp, deployKey, alice )
    if len(rawData)==len(dbData):
        print "Lengths match, proceeding"        


    for j,x in zip(rawData, dbData):
        mismatchRow = []        
        for k in range(len(j)):
            colName = rawDict[k]
            dbPosition = dbInvDict[colName]
            if k!= 21 and j[k] == x[dbPosition]:
                pass
            elif k == 21 and j[k] == float(x[dbPosition]):
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
    rawDeployInfo = [rawSerial, rawStartEndDate[0], rawStartEndDate[1]]
    for j in deployTable:
        if rawDeployInfo[0] == j[0] and rawDeployInfo[1] >= j[1] and rawDeployInfo[2] <= j[2]:
            deployKey = j[3]
        else:
            pass
    rawData = falmouth.cast(rawData)
    dbData = falmouth.retrieveRange(rawStartEndTimestamp, deployKey, alice )
    dbData = sorted(dbData, key = lambda datetime: datetime[5])
    if len(rawData)==len(dbData):
        print "Lengths match, proceeding"        


    for j,x in zip(rawData, dbData):
        mismatchRow = []        
        for k in range(len(j)):
            colName = rawDict[k]
            dbPosition = dbInvDict[colName]
            if (k!= 10 or k!=23) and j[k] == x[dbPosition]:
                pass
            elif (k == 10 or k==23) and j[k] == float(x[dbPosition]):
                pass
            else:
                mismatchRow.append(colName)
        mismatchRow = list(set(mismatchRow))
    mismatchListB.append([i, [item for item in mismatchRow]])     
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

        