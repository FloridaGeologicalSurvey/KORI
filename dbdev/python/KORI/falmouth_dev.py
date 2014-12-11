# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 12:18:06 2014

@author: Bassett_S
"""
import csv
import datetime
import psycopg2

class Falmouth:
    """Common base class for all Falmouth Files"""
    def __init__(self, path, connection):        
        self.path = path
        self.connection = connection
        self.flags = {}
        self.columnHeaders = self.parseColumnHeaders()
        self.data = self.parseData()
        self.castData()
        self.serial = self.parseSerialNumber()
        self.deployNumber = self.getDeployKey()
        self.insertDeployNumber()
        
    def insertDeployNumber(self):
        for row in self.data:
            row["deploy_key"] = self.deployNumber
          
    def returnMinMaxTimestamp(self):
        tslist = [datetime.datetime.strptime(row["date_time"],"%Y-%m-%d %H:%M:%S UTC") for row in self.data]
        #tslist = [item + datetime.timedelta(hours=5) for item in tslist[:]]
        tsmin = min(tslist).strftime("%Y-%m-%d %H:%M:%S UTC")
        tsmax = max(tslist).strftime("%Y-%m-%d %H:%M:%S UTC")
        return (tsmin, tsmax)
        
    def getDeployKey(self):
        cursor = self.connection.cursor()
        minTS, maxTS = self.returnMinMaxTimestamp()
        sql = "SELECT deploy_key FROM deploy_info WHERE serial_number = \'{0}\' AND start_dt <= \'{1}\' and end_dt >= \'{2}\';".format(self.serial, minTS, maxTS)
        cursor.execute(sql)
        deploy_key = cursor.fetchall()
        cursor.close()
        del cursor
        return deploy_key[0][0]
        
        
    def parseSerialNumber(self):
        with open(self.path, 'r') as f:
            data = [line for line in f]
        serial = data[8]
        serial = serial.split(":")
        serial = serial[1].strip()
        return serial
        
    def parseColumnHeaders(self):
        """Parses column headers from raw falmouth file"""
        
        with open(self.path, "r") as f:
            data = [line for line in f]
        headers = data[10]
        del data
        
        #split and convert to lower case
        headers = headers.split()
        headers = [item.lower() for item in headers[:]]
        
        #concatenate date and time headers to single date_time header        
        if "date" in headers[:]:
            indexPos = headers[:].index("date")
            headers[indexPos]="date_time"
        if "time" in headers[:]:
            headers.remove("time")
        
        #fix dual SV column headers
        svIndex = [v for v,item in enumerate(headers) if item =='sv']
        if len(svIndex) == 1:
            headers[svIndex[0]] = 'sv1'
        elif len(svIndex) == 2:
            headers[svIndex[0]] = 'sv2'
            headers[svIndex[1]] = 'sv1'
            
        return headers
    
    def parseData(self):
        """Parses data table from raw falmouth file"""
        
        #strip functions for stripping extra whitespace
        stripFunction = {i:str.strip for i in self.columnHeaders}
        
        with open(self.path, "r") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self.columnHeaders)
            
            #trash is header info, needs to be skipped for the data table
            for i in range(10):
                trash = next(reader)
            del trash           
            data = [row for row in reader]
            
            #strips extra whitespace            
        data = [{key:stripFunction[key](row[key]) for key in row.keys() if row[key] != None} for row in data[:]]
        
        #handle bad timestamps        
        badDateTime = [row for row in data[:] if row["date_time"] == '255:255:255 255-255-65535']
        if len(badDateTime) >0:
            self.flags["255"] = len(badDateTime)
            data = [row for row in data[:] if row["date_time"] != '255:255:255 255-255-65535']
        else:
            self.flags["255"] = False            
        return(data)
            
    def castData(self):
        """casts data table to proper types"""
        try:
            for row in self.data[:]:
                for key in row.keys():
                    if key == "date_time":
                        tempTime = datetime.datetime.strptime(row[key],"%H:%M:%S %m-%d-%Y")
                        tempTime = tempTime + datetime.timedelta(hours=5)
                        row[key] = tempTime.strftime("%Y-%m-%d %H:%M:%S UTC")
                    else:
                        row[key]=float(row[key])
            self.flags['cast'] = True
        except:
            self.flags["cast"] = False
            print "Error casting {0}".format(self.path)
    
    def createInsertStatement(self, row):
        """Creates an insert statement for each row"""
        listFields = sorted(row.keys())
        intoStatement = ", ".join(listFields)
        valueParts = ["%({0})s".format(i) for i in listFields]
        valuesStatement = ", ".join(valueParts)
        insertStatement = """INSERT INTO {0} ({1}) VALUES ({2});""".format('falmouth', intoStatement, valuesStatement)
        return insertStatement

    def load(self):
        """Loads data to database"""
        cursor = self.connection.cursor()
        for row in self.data:
            sql = self.createInsertStatement(row)
            cursor.execute(sql, row)
        self.connection.commit()
        cursor.close()
        del cursor
    
    