# -*- coding: utf-8 -*-
"""
Created on Tue Oct 07 10:18:44 2014

@author: Bassett_S
"""
import csv, re


def parseHeader (data):
    h = []
    for row in data:
        for key in row.keys():
            h.append(key)
            
    hset = set(h)
    
    headers = list(hset)
    return headers

def parseData(path, header):
    with open(path, "r") as csvfile:
        dreader = csv.DictReader(csvfile, fieldnames=header)
        data = [row for row in dreader]
    return data
        
def typeColumns(columnDic, debug=False):
    iTests = {key:isInt(columnDic[key]) for key in columnDic.keys()}
    fTests = {key:isFloat(columnDic[key]) for key in columnDic.keys()}
    dTests = {key:hasDecimal(columnDic[key]) for key in columnDic.keys()}
    
    iResults = calculateResults(iTests)
    fResults = calculateResults(fTests)
    dResults = calculateResults(dTests)

    finalTypes = {key:[] for key in columnDic.keys()}
    for key in columnDic.keys():
        if iResults[key] < 0.95 and fResults[key] > 0.95 and dResults[key] > 0.95:
            ps = pANDs(columnDic[key])
            finalTypes[key] = ["Float", ps[0], ps[1]]
        elif iResults[key] > 0.95 and fResults[key] > 0.95 and dResults[key] < 0.95:
            finalTypes[key] = "Integer"
        elif iResults[key] < 0.95 and fResults[key] < 0.95 and dResults[key] < 0.95:
            finalTypes[key] = "Other"
    if not debug:
        return finalTypes
    if debug:
        return {"tests":[iTests, fTests, dTests],"results":[iResults, fResults, dResults], "final types":finalTypes}


def lengthColumns(columnDic):
    lenDic = {key:None for key in columnDic.keys()}
    for key in columnDic.keys():
        lenList = []
        for item in columnDic[key]:
            lenList.append(len(item))
        lenDic[key] = set(lenList)
    return lenDic
        
def calculateResults(testDic):
    results = {}    
    for key in testDic.keys():
        T = float(sum(testDic[key]))
        total = float(len(testDic[key]))
        results[key] = T/total
    return results

def flattenColumns(rowDictionary):
    keySet = set()
    for row in rowDictionary:
        for key in row.keys():
            keySet.add(key)
            
    columns = {key:[] for key in keySet}
    for row in rowDictionary:
            for key in row:
                columns[key].append(row[key])
    return columns
    


def isFloat(listValues):
    testValues = []
    for value in listValues:
        try:
            float(value)
            testValues.append(True)
        except:
            testValues.append(False)
    return testValues
    
def isInt(listValues):
    testValues = []
    for value in listValues:
        try:
            int(value)
            testValues.append(True)
        except:
            testValues.append(False)
    return testValues

def hasDecimal(listValues):
    testValues = []
    for value in listValues:
        if "." in value:
            split = value.split(".")
            if len(split) == 2:
                testValues.append(True)
            else:
                testValues.append(False)
        else:
            testValues.append(False)
    return testValues
    
def pANDs(aList):
    precision = set()
    scale = set()
    for item in aList:
        if "." in item:
            stripped = item.strip("-")
            split=stripped.split(".")
            precision.add(len(split[0])+len(split[1]))
            scale.add(len(split[1]))
        else:
            try: 
                int(item)
                noNegs = item.strip("-")
                precision.add(0)
                scale.add(len(noNegs))
            except:
                precision.add(None)
                scale.add(None)
                
    return [precision, scale]

def isUTC(listValues):
    testValues = []
    regex = re.compile(r'((200[6-9]|201[0-4])\-?(0[1-9]|1[012])\-?([012][0-9]|[3][01]))(\s([01][0-9]|[2][0-3])\:([0-5][0-9])\:([0-5][0-9]))(\s([aAPp][mM]))?')
    #for item in listValues:
        
"""
for d,n in zip(tdebug[1], ["int","float","dec"]):
    print n
    for key in d.keys():
        print "\t",key,d[key]
for d,n in zip(tdebug[0], ["int","float","dec"]):
    print n
    for key in d.keys():
        print "\t",key,sum(d[key])/len(d[key]) 
"""