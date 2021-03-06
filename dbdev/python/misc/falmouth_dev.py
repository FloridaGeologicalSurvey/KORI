# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 10:10:07 2014

Abstract:
This is a module for handling falmouth data.

@author: Seth Bassett

"""

import datetime, psycopg2,  psycopg2.extras, csv    
import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

###########   RAW FILE HANDLING ###########################     
def parse(falmouthFile, returnType):
    """Parse raw Falmouth files into either a data table, or a header.
    This script accepts a path to a Falmouth file and an argument as input
    Allowed returnTypes: 'data', 'header'
    Returns a list of header information or the data table from the file.
    Dpendencies: parseFalmouthHeaderRow"""
    with open(falmouthFile) as f:
        f_csv = csv.reader(f)
        deployNum = next(f_csv)
        mooring = next(f_csv)
        position = next(f_csv)
        latitude = next(f_csv)
        longitude = next(f_csv)
        depth = next(f_csv)
        downloadTime = next(f_csv)
        downloadTime = downloadTime[0]
        downloadTime = downloadTime[15:]
        downloadDate = next(f_csv)
        downloadDate = parseHeader(downloadDate)
        serial = next(f_csv)
        serial = parseHeader(serial)
        blank = next(f_csv)
        header = next(f_csv)
        header = header[0].split()
        allRows = []
        for r in f_csv:
            thisRow = []
            for i in r:
                thisValue = i.strip(",")
                thisValue = i.strip()
                thisRow.append(thisValue)
            allRows.append(thisRow)
        if returnType == "header":
            return [serial, downloadDate, downloadTime]
        elif returnType == "data":
            return allRows
        elif returnType == "data header":
            return header
            


def parseHeader(headerRow):
    """
    Strips and splits the trash off of Falmouth Header Rows
    This function is required for parseFalmouthFile to work correctly
    """
    headerRow = headerRow[0]
    headerRow = headerRow.split(":")[1]
    headerRow = headerRow.strip()
    return headerRow
    
def parseTimestamps(data):
	dates = []
	for i in data:
		if i[5] != '255:255:255 255-255-65535':
			datetimeItem = datetime.datetime.strptime(i[5], '%H:%M:%S %m-%d-%Y')
		else:
			pass
		dates.append(datetimeItem)
	minDate = min(dates)
	maxDate = max(dates)
	return [minDate, maxDate]

def parseDates(data):
    """
    Scans the data table generated by parseFalmouthFile('somefile', 'data') 
        and returns the min and max date as a list
    """
    dates = []
    for i in data:
        #required to filter bad data lines occasionally generated by the sensors
        if i[5] != '255:255:255 255-255-65535':
			datetimeItem = datetime.datetime.strptime(i[5], '%H:%M:%S %m-%d-%Y')
			datetimeItem = datetimeItem.date()
        else:
			pass
        dates.append(datetimeItem)
    minDate = min(dates)
    maxDate = max(dates)
    return [minDate, maxDate]

def cast(data):
    """
    Casts Falmouth Data into proper types
    """
    castData = []
    for i in data:
        #required to filter bad data lines occasionally generated by the sensors
        if i[5] != '255:255:255 255-255-65535':
            thisRow = []
            #LAZY! - I really need to stop doing this. What the hell it works.           
            for j in range(len(i)):
                if j != 5:
                    thisRow.append(float(i[j]))
                else:
                    thisRow.append(datetime.datetime.strptime(i[j], '%H:%M:%S %m-%d-%Y'))
            castData.append(thisRow)
        else:
			pass

    return castData

def classifyFalmouth(filePaths):
    """
    Classifies Falmouth files as either "A" or "B"
    Use to prepare data to write to the dev_log table
    Input is a list of file paths to the raw files.
    Output is the nested list [[TypeA],[TypeB],[Unknown]]
    """
    typeA = ['AVN', 'AVE', 'ASPD', 'AVDIR', 'ATLT', 'TIME', 'DATE', 
            'COND', 'TEMP', 'PRES', 'HDNG', 'BATT', 'VX', 'VY', 'TX', 
            'TY', 'HX', 'HY', 'HZ', 'VN', 'VE', 'STEMP', 'SV', 'VAB', 
            'VCD', 'VEF', 'VGH']
            
    typeB = ['AVN', 'AVE', 'ASPD', 'AVDIR', 'ATLT', 'TIME', 'DATE', 
         'COND', 'TEMP', 'PRES', 'SALT', 'SV', 'HDNG', 'BATT', 
         'VX', 'VY', 'TX', 'TY', 'HX', 'HY', 'HZ', 'VN', 'VE', 
         'STEMP', 'SV', 'VAB', 'VCD', 'VEF', 'VGH']
    
    pathsTypeA = [f for f in filePaths if parse(f, "data header") == typeA ]
    pathsTypeB = [f for f in filePaths if parse(f, "data header") == typeB ]
    pathsTypeU = [f for f in filePaths if parse(f, "data header") != typeA and parse(f, "data header") != typeB]
    returnList = [pathsTypeA, pathsTypeB, pathsTypeU]
    return returnList
###############################################################################


##################  PANDAS   ##################################################
def pandizeSensor(sensorData):
    newSensorData = []
    for i in sensorData:
        newRow = []
        if str(i[5]) != '255:255:255 255-255-65535':
            for j in range(26):
                if j != 5:
                    newRow.append(float(i[j]))
                else:
                    dt = datetime.datetime.strptime(str(i[j]), '%H:%M:%S %m-%d-%Y')
                    newRow.append(dt)
            newSensorData.append(newRow)
    array = np.array(newSensorData)
    pdSensor = pd.DataFrame(array, index=array[:,5])
    return pdSensor

def pandizeDB(dbData):
    newDBdata = []
    for i in dbData:
        newRow = []
        for j in range(len(i)):
            if j != 5 and i[j] != None:
                newRow.append(float(i[j]))
            elif i[j] == None:
                newRow.append(i[j])
            elif j == 5:
                date = i[j].replace(tzinfo=None)
                date = date.toordinal()
                newRow.append(i[j].replace(tzinfo=None))
        newDBdata.append(newRow)
    array = np.array(newDBdata)
    pdData = pd.DataFrame(array, index=array[:,5])
    pdData.columns = ['avn', 'ave', 'aspd', 'avdir', 'atlt', 'date_time', 'cond', 'temp', 'pres', 'hdng', 'batt', 'vx', 'vy', 'tx', 'ty', 'hx', 'hy', 'hz', 'vn', 've', 'stemp', 'sv1', 'vab', 'vcd', 'vef', 'vgh', 'id','deploy_key', "salt", "depth", "sv2"]
    pdData = pdData.sort_index()
    return pdData

def pandizeCompare(df1, df2):
    try: 
        assert_frame_equal(df1.sort(axis=0), df2.sort(axis=0))
        return True
    except:
        return False

def pandizeDBordinal(dbData):
    newDBdata = []
    for i in dbData:
        newRow = []
        for j in range(28):
            if j != 5:
                newRow.append(float(i[j]))
            else:
                date = i[j].replace(tzinfo=None)
                date = date.toordinal()
                newRow.append(date)
        newDBdata.append(newRow)
    array = np.array(newDBdata)
    pdData = pd.DataFrame(array, index=array[:,5])
    del pdData[26]
    del pdData[27]
    pdData.columns = ['avn', 'ave', 'aspd', 'avdir', 'atlt', 'date_time', 'cond', 'temp', 'pres', 'hdng', 'batt', 'vx', 'vy', 'tx', 'ty', 'hx', 'hy', 'hz', 'vn', 've', 'stemp', 'sv', 'vab', 'vcd', 'vef', 'vgh']
    pdData = pdData.sort_index()
    return pdData


###############################################################################

###################   SQL OPERATIONS ##########################################
def est2utc(timestamp):
    """
    Casts Falmouth Data into proper types
    """
    utc = timestamp + datetime.timedelta(hours=5)
    return utc

def edt2utc(timestamp):
    utc = timestamp + datetime.timedelta(hours=4)
    return utc
    

def writeFalmouthDataTypeB(falmouthFile, deploy_key, connection_info):
    #establish connection and cursor    
    con = psycopg2.connect(dsn=None, 
        host= connection_info[0],
        database= connection_info[1],
        user= connection_info[2],
        password= connection_info[3])

    cur = con.cursor()      
    dataBlock = parse(falmouthFile, "data")
    startEnd = parseTimestamps(dataBlock)

    
    #query the database to see if the datetime range for the current file and deploy key already exists in the database
    sqlQuery = cur.mogrify("SELECT * FROM falmouth WHERE deploy_key = %s AND (date_time BETWEEN %s AND %s);", (deploy_key, startEnd[0], startEnd[1]))
    rows = retrieveRows(sqlQuery, connection_info)
    
    #only add rows if SQL query returns null, otherwise print filename to console
    if len(rows)  == 0:
        #lAZY - Revell_Falmouth_02-16-2011_02-17-2011 threw an error when casting to type using the castFalmouthData function. I have no idea why. Try/except is to bypass this one file.        
        try:        
            #cast the datablock into int & datetime.datetime types in preperation for upload            
            castBlock = cast(dataBlock)
        except:
            print "Error Casting", falmouthFile, "--------- SKIPPING"
            return
        for i in castBlock:
            utcTime = est2utc(i[5]).strftime("%Y-%m-%d %H:%M:%S+00")
            cur.execute("""INSERT INTO falmouth (avn, ave, aspd, avdir, atlt, date_time, cond, temp, pres, salt, sv2, hdng, batt, vx, vy, tx, ty, hx, hy, hz, vn, ve, stemp, sv1, vab, vcd, vef, vgh, deploy_key)
                        values(%(avn)s, %(ave)s, %(aspd)s, %(avdir)s, %(atlt)s, %(date_time)s, %(cond)s, %(temp)s, %(pres)s, %(salt)s, %(sv2)s, %(hdng)s, %(batt)s, %(vx)s, %(vy)s, %(tx)s, %(ty)s, %(hx)s, %(hy)s, %(hz)s, %(vn)s, %(ve)s, %(stemp)s, %(sv1)s, %(vab)s, %(vcd)s, %(vef)s, %(vgh)s, %(key)s);""",
                        {'avn':i[0], 'ave':i[1], 'aspd':i[2], 'avdir':i[3], 'atlt':i[4], 'date_time':utcTime, 'cond':i[6], 'temp':i[7], 'pres':i[8], 'salt':i[9], 'sv2':i[10], 'hdng':i[11], 'batt':i[12], 'vx':i[13], 'vy':i[14], 'tx':i[15], 'ty':i[16], 'hx':i[17], 'hy':i[18], 'hz':i[19], 'vn':i[20], 've':i[21], 'stemp':i[22], 'sv1':i[23], 'vab':i[24], 'vcd':i[25], 'vef':i[26], 'vgh':i[27], 'key': deploy_key})
        con.commit()
        print falmouthFile, 'written successfully with', len(castBlock), 'rows'
    else:
        #there is something very strange with B_Falmouth_01-18-2010_02-05-2010 & B_Falmouth_01-05-2010_03-01-2010. Find originals and ask Scott      
        print "\n"        
        print "There was an error with", falmouthFile
        print len(rows), "rows already exist."
        print "\n"                
    cur.close()
    con.close()
    
def writeFalmouthDataTypeA(falmouthFile, deploy_key, connection_info):
    #establish connection and cursor    
    con = psycopg2.connect(dsn=None, 
        host= connection_info[0],
        database= connection_info[1],
        user= connection_info[2],
        password= connection_info[3])

    cur = con.cursor()      
    dataBlock = parse(falmouthFile, "data")
    startEnd = parseTimestamps(dataBlock)

    
    #query the database to see if the datetime range for the current file and deploy key already exists in the database
    sqlQuery = cur.mogrify("SELECT * FROM falmouth WHERE deploy_key = %s AND (date_time BETWEEN %s AND %s);", (deploy_key, startEnd[0], startEnd[1]))
    rows = retrieveRows(sqlQuery, connection_info)

    #only add rows if SQL query returns null, otherwise print filename to console
    if len(rows)  == 0:
        #lAZY - Revell_Falmouth_02-16-2011_02-17-2011 threw an error when casting to type using the castFalmouthData function. I have no idea why. Try/except is to bypass this one file.        
        try:        
            #cast the datablock into int & datetime.datetime types in preperation for upload            
            castBlock = cast(dataBlock)
        except:
            print "Error Casting", falmouthFile, "--------- SKIPPING"
            return
        for i in castBlock:
            utcTime = est2utc(i[5]).strftime("%Y-%m-%d %H:%M:%S+00")
            cur.execute("""INSERT INTO falmouth (avn, ave, aspd, avdir, atlt, date_time, cond, temp, pres, hdng, batt, vx, vy, tx, ty, hx, hy, hz, vn, ve, stemp, sv1, vab, vcd, vef, vgh, deploy_key)
            values(%(avn)s, %(ave)s, %(aspd)s, %(avdir)s, %(atlt)s, %(date_time)s, %(cond)s, %(temp)s, %(pres)s, %(hdng)s, %(batt)s, %(vx)s, %(vy)s, %(tx)s, %(ty)s, %(hx)s, %(hy)s, %(hz)s, %(vn)s, %(ve)s, %(stemp)s, %(sv1)s, %(vab)s, %(vcd)s, %(vef)s, %(vgh)s, %(key)s);""",
                        {'avn':i[0], 'ave':i[1], 'aspd':i[2], 'avdir':i[3], 'atlt':i[4], 'date_time':utcTime, 'cond':i[6], 'temp':i[7], 'pres':i[8], 'hdng':i[9], 'batt':i[10], 'vx':i[11], 'vy':i[12], 'tx':i[13], 'ty':i[14], 'hx':i[15], 'hy':i[16], 'hz':i[17], 'vn':i[18], 've':i[19], 'stemp':i[20], 'sv1':i[21], 'vab':i[22], 'vcd':i[23], 'vef':i[24], 'vgh':i[25], 'key': deploy_key})
        con.commit()
        print falmouthFile, 'written successfully with', len(castBlock), 'rows'
    else:
        #there is something very strange with B_Falmouth_01-18-2010_02-05-2010 & B_Falmouth_01-05-2010_03-01-2010. Find originals and ask Scott      
        print "\n"        
        print "There was an error with", falmouthFile
        print len(rows), "rows already exist."
        print "\n"                
    cur.close()
    con.close()

def retrieveColumnNames(sqlQuery, connection_info):
    con = psycopg2.connect(dsn=None, 
        host= connection_info[0],
        database= connection_info[1],
        user= connection_info[2],
        password= connection_info[3])

	#establish dictionary database cursor to read DB
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

	#set SQL query to run against DB tables
    cur.execute(sqlQuery)

	#fetch all rows that meet criteria, load into variable "rows"
    columnInfo = cur.description
    header = [i[0] for i in columnInfo]
	#close connection
    con.close()

	#return list
    return header

def retrieveRange(startEnd, deploy_key, connection_info):   
    con = psycopg2.connect(dsn=None, 
        host= connection_info[0],
        database= connection_info[1],
        user= connection_info[2],
        password= connection_info[3])

	#establish dictionary database cursor to read DB
    cur = con.cursor()
    sqlQuery = sqlQuery = cur.mogrify("SELECT * FROM falmouth WHERE deploy_key = %s AND (date_time BETWEEN %s AND %s);", (deploy_key, startEnd[0], startEnd[1]))
	#set SQL query to run against DB tables
    cur.execute(sqlQuery)

	#fetch all rows that meet criteria, load into variable "rows"
    rows = cur.fetchall()

	#close connection
    con.close()

	#return list
    return rows


def retrieveRows(sqlQuery, connection_info):
    con = psycopg2.connect(dsn=None, 
        host= connection_info[0],
        database= connection_info[1],
        user= connection_info[2],
        password= connection_info[3])

	#establish dictionary database cursor to read DB
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

	#set SQL query to run against DB tables
    cur.execute(sqlQuery)

	#fetch all rows that meet criteria, load into variable "rows"
    rows = cur.fetchall()

	#close connection
    con.close()

	#return list
    return rows

def buildSQLquery(what, table, criteria):
	if criteria != "NONE":
		sqlQuery = "SELECT " + what + " FROM " + table + " WHERE " + criteria
	else:
		sqlQuery = "SELECT " + what + " FROM " + table
	return sqlQuery

def buildTableHeader(infoTable):
	header = [i[0] for i in infoTable]
	return header

def findIndexNumber(serial, start, end, deployTable, parsedDeployTable):
	for i, j in zip(parsedDeployTable, deployTable):
		if i[0] == serial and start >= i[1] and end <= i[2]:
			return j[10]

def parseDeployTable(deployTable):
	newDeployTable = []
	for i in deployTable:
		if i[3] is None:
			newStart = datetime.date(1, 1, 1)
		elif type( i[3] ) is datetime.date:
			newStart = i[3]
		if i[4] is None:
			newEnd = datetime.date(9999, 1, 1)
		elif type( i[4] ) is datetime.date:
			newEnd = i[4]
		newDeployTable.append( [ i[2] , newStart , newEnd ] )
	return newDeployTable


    