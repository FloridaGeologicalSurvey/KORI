# -*- coding: utf-8 -*-
"""
Created on Tue May 06 09:45:08 2014

@author: Bassett_s

Get Database Values
"""

import falmouth, datetime, os, psycopg2, shutil
import numpy as np
import pandas as pd
from decimal import Decimal
import math

import math
####### GLOBALS ######

#resample period. Standard periods are '15min', '1H', '1D'
resampleTo = '1H'

#connection info, of type [host, database, user, password]
alice = []
#directory to write final files to
outputWorkspace = r"C:\PythonWorkspace\Pandas"

#a directory to hold temporary pickles. Script will clean up when it is finished
pickleJar = r"C:\PythonWorkspace\PickleJar"

startYear = 2006
endYear = 2013
currentYear = startYear
##############################################

#################### HARD CODE VARIABLES #######################################
header = ['avn', 'ave', 'aspd', 'avdir', 'atlt', 'date_time', 'cond', 'temp', 'pres', 'hdng', 'batt', 'vx', 'vy', 'tx', 'ty', 'hx', 'hy', 'hz', 'vn', 've', 'stemp', 'sv1', 'vab', 'vcd', 'vef', 'vgh', 'id','dev_deply_ky', "salt", "depth", "sv2"]
pdHeader = ['datetime','avn','ave','aspd','avdir','atlt','cond','temp','pres','hdng','batt','vx','vy','tx','ty','hx','hy','hz','vn','ve','stemp','sv1','vab','vcd','vef','vgh','id','dev_deply_ky','salt','depth','sv2']
columnIndex = {v:i for v, i in enumerate(header)}
columnIndexInv = {i:v for v, i in enumerate(header)}
valuesIndex = {i: None for i in header}

falmouthDictionary = {16: 'B',
                      17: 'C',
                      18: 'AD',
                      20: 'D',
                      23: 'SC10',
                      25: 'AK',
                      27: 'D',
                      28: 'K',
                      48: 'AK',
                      49: 'D',
                      50: 'K',
                      51: 'SC1',
                      53: 'Vent',
                      55: 'Vent',
                      56: 'Vent',
                      57: 'Revell'}

masterSensorList = ["B","C","D","K","AD","AK","SC1","SC10","Revell","Vent"]                      
###############################################################################

##################### FUNCTIONS   ############################################

def averageBearing(data):
    radians = [math.radians(i) for i in data if not math.isnan(i)]
    coss = [math.cos(i) for i in radians]
    sinn = [math.sin(i) for i in radians]
    sum_cos = sum(coss)
    sum_sin = sum(sinn)
    mean_radians= math.atan2(sum_sin, sum_cos)
    mean_degrees= math.degrees(mean_radians)
     
    if mean_degrees < 0:
       fixedMean = mean_degrees + 360.0
    elif mean_degrees > 360:
        fixedMean = mean_degrees - 360.0
    else:
        fixedMean = mean_degrees 
    if fixedMean == 0:
        return None
    else:
        return fixedMean

def average(data):
    ldata = [i for i in data]
    length = len(ldata)
    total = sum(ldata)
    returnVal = total / length
    return returnVal



def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
    
##############################################################################
#increments by year from the start year to the end year
for y in range(startYear, endYear+1, 1):
    print "\n"
    print "*"*20+" "+str(y)+" "+"*"*20
    timeRange = [datetime.datetime(y, 1, 1, 0, 0, 0), datetime.datetime(y, 12, 31, 23, 59, 59)]
    #connection parameters
    con = psycopg2.connect(dsn=None, 
        host= alice[0],
        database= alice[1],
        user= alice[2],
        password= alice[3])
    
    #establish connection
    cur = con.cursor()
    #mogify SQL, query DB, return values
    print "Querying DB"
    mogrifySQL = cur.mogrify("""SELECT * FROM falmouth WHERE date_time BETWEEN %s AND %s ORDER BY (dev_deply_ky, date_time);""", (timeRange[0], timeRange[1]))
    cur.execute(mogrifySQL)
    rows = cur.fetchall()
    con.close()
    
    #generate list of deploy keys
    deployKeys = [i[columnIndexInv["dev_deply_ky"]] for i in rows]
    deployKeys = list(set(deployKeys))

    
    #pandize
    blankIndex = pd.date_range(start=timeRange[0], end=timeRange[1], freq=resampleTo)
    blankSeries = pd.Series(index=blankIndex)
    sensors = [falmouthDictionary[key] for key in deployKeys]
    sensors = list(set(sensors))    
    #if no data rows present in database, write a blank year to output file    
    for s in masterSensorList:
        if s not in sensors:
            print "-"*40            
            print s, "Not Found, writing blank year"
            dfBlank = pd.DataFrame(index=blankIndex, columns = header)
            del dfBlank["date_time"]
            outFile = os.path.join(outputWorkspace, s)
            if not os.path.exists(outFile):
                dfBlank.to_csv(outFile, mode='a', header=True, index_label="datetime")
            elif os.path.exists(outFile):
                dfBlank.to_csv(outFile, mode='a', header=False)
            del dfBlank
            print "-"*40
    #iterate through the deploy keys found in the database table, pandize, and write to output
    for i in deployKeys:
        print "\n"
        print "-"*40        
        print falmouthDictionary[i], y
        #extract sensor data
        print "Pandizing"        
        sensorData = [k for k in rows if k[columnIndexInv["dev_deply_ky"]] == i]
        #create numpy array and pandize
        array = np.array(sensorData)
        pdData = pd.DataFrame(array, index=array[:,5])
        pdData.columns = header
    
        del pdData["date_time"]
        del array
        
        #resample each column and pickle (to conserve memory)
        print "Pickling"
        for k in header:
            if k == "date_time":
                continue

            series = pdData[k]
            series = series.astype(float)
            if k != "avdir":
                series = series.resample(resampleTo, how=average)
            elif k == "avdir":
                series = series.resample(resampleTo, how = averageBearing)
    
            series = series.combine_first(blankSeries)
            path=os.path.join(pickleJar, k)
            series.to_pickle(path)
        del series, path, k
        
        #create a blank dataFrame, delete the old values
        dfBlank = pd.DataFrame(index=blankIndex, columns=pdData.columns)
        del pdData
        
        #depickle and create new dataframe   
        print "Depickling"
        for k in header:
            if k=="date_time":
                continue
            path = os.path.join(pickleJar, k)
            a = pd.read_pickle(path)
            dfBlank[k] = a
        outFile = os.path.join(outputWorkspace, falmouthDictionary[i])
        
        if not os.path.exists(outFile):
            print "Writing file"
            dfBlank.to_csv(outFile, header=True, index_label="datetime")
        elif os.path.exists(outFile):
            print "Appending File"
            dfBlank.to_csv(outFile, mode='a', header=False)               
        print "-"*40
        pickles = os.listdir(pickleJar)
        print "Cleaning up pickles"
        for k in pickles:
            thisPath = os.path.join(pickleJar, k)            
            os.remove(thisPath)

            
            
      


    
