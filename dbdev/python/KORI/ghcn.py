# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 10:20:10 2014

@author: Bassett_S

Module for handling NOAA GHCN data
"""

import datetime, os, csv, psycopg2, re, shutil
ghcnPath = r'C:\GISData\WKP Data\Flat Data\CLEAN CDO\ghcn\five_counties.csv'
ghcnHeader = r'C:\GISData\WKP Data\Flat Data\CLEAN CDO\ghcn\five_counties_header.txt'

#fcounties = Ghcn(ghcnPath, ghcnHeader, usrv)


class Ghcn:
    types = {
        'STATION':str,
        'STATION_NAME':str,
        'station': str,
        'DATE': str,
        'LATITUDE': str,
        'LONGITUDE':str,
        'ELEVATION':str,
        'date_time': str,
        'SX32': int,
        'SX32_mflag':str,
        'SX32_qflag':str,
        'SX32_sflag':str,
        'SX32_tobs':int,
        'SX33':int,
        'SX33_mflag':str,
        'SX33_qflag':str,
        'SX33_sflag':str,
        'SX33_tobs':int,
        'SX31':int,
        'SX31_mflag':str,
        'SX31_qflag':str,
        'SX31_sflag':str,
        'SX31_tobs':int,
        'SN32':int,
        'SN32_mflag':str,
        'SN32_qflag':str,
        'SN32_sflag':str,
        'SN32_tobs':int,
        'SN33':int,
        'SN33_mflag':str,
        'SN33_qflag':str,
        'SN33_sflag':str,
        'SN33_tobs':int,
        'SN31':int,
        'SN31_mflag':str,
        'SN31_qflag':str,
        'SN31_sflag':str,
        'SN31_tobs':int,
        'MDPR':int,
        'MDPR_mflag':str,
        'MDPR_qflag':str,
        'MDPR_sflag':str,
        'MDPR_tobs':int,
        'DAPR':int,
        'DAPR_mflag':str,
        'DAPR_qflag':str,
        'DAPR_sflag':str,
        'DAPR_tobs':int,
        'PRCP':int,
        'PRCP_mflag':str,
        'PRCP_qflag':str,
        'PRCP_sflag':str,
        'PRCP_tobs':int,
        'SNWD':int,
        'SNWD_mflag':str,
        'SNWD_qflag':str,
        'SNWD_sflag':str,
        'SNWD_tobs':int,
        'SNOW':int,
        'SNOW_mflag':str,
        'SNOW_qflag':str,
        'SNOW_sflag':str,
        'SNOW_tobs': int,
        'TMAX':int,
        'TMAX_mflag':str,
        'TMAX_qflag':str,
        'TMAX_sflag':str,
        'TMAX_tobs':int,
        'TMIN':int,
        'TMIN_mflag':str,
        'TMIN_qflag':str,
        'TMIN_sflag':str,
        'TMIN_tobs':int,
        'TOBS':int,
        'TOBS_mflag':str,
        'TOBS_qflag':str,
        'TOBS_sflag':str,
        'TOBS_tobs':int
        }
    def __init__(self, path, headerPath, connection_info):
        self.path = path
        self.connection = psycopg2.connect(dsn=None, 
            host= connection_info[0],
            database= connection_info[1],
            user= connection_info[2],
            password= connection_info[3])

        self.headers = self.parseHeaders(headerPath)
        self.data = []
        self.parse()

    def parse(self):
        with open(self.path) as f:
            reader = csv.DictReader(f, fieldnames=self.headers)
            self.data = [row for row in reader]
        self.data = self.data[1:]
        
    def parseHeaders(self, headerPath):
        with open(headerPath, 'r') as f:
            h = [row for row in f]
        h = [i.strip("\n") for i in h]
        return h
    
    def press(self):
        pressedrow = [dict() for row in self.data]
        for prow, row in zip(pressedrow, self.data):
            #print "ROW {0}".format(v)
            #print "appending station"
            prow['station'] = row['STATION']
            #print "compiling datetime"            
            #tobs = self.findTOBS(row)
            date = row['DATE']
            timestamp = datetime.datetime.strptime(date, "%Y%m%d")
            prow['date_time'] = timestamp.strftime("%Y-%m-%d 00:00:00 UTC")
            #"Casting"
            for key in row.keys():
                if Ghcn.types[key] is int and row[key] != '9999' and row[key] != '-9999' and row[key] != "":
                    prow[key] = int(row[key])
        return pressedrow
    def findTOBS(self, row):
        tobs = [row[key] for key in row.keys() if "_tobs" in key]
        validTOBS = [item for item in tobs if item != '-9999' and item != '9999']
        setTobs = list(set(validTOBS))
        if len(setTobs) == 0:
            setTobs = ['0000']
        return setTobs[0]
    def createInsertStatement(self, tableName, row):
        listFields = sorted(row.keys())
        intoStatement = ", ".join(listFields)
        valueParts = ["%({0})s".format(i) for i in listFields]
        valuesStatement = ", ".join(valueParts)
        insertStatement = """INSERT INTO {0} ({1}) VALUES ({2});""".format(tableName, intoStatement, valuesStatement)
        return insertStatement
    
    def load(self):
        pdata = self.press()
        cursor = self.connection.cursor()
        for row in pdata:
            sql = self.createInsertStatement("noaa_ghcn",row)
            cursor.execute(sql,row)
        self.connection.commit()
        cursor.close()
        del cursor
        
        
         
        
            

                
        
class GSOD:
    def __init__(self, path, connection_info):
        self.path = path
        self.connection = psycopg2.connect(dsn=None, 
            host= connection_info[0],
            database= connection_info[1],
            user= connection_info[2],
            password= connection_info[3])
        self.data = []
        self.headers=[]
        self.dbHeaders=[]
    def parse(self):
        with open(self.path, 'r') as f:
            #reader = csv.reader(f, delimiter =",", quotechar="\"")
            #rows = [row for row in reader]
            #self.data = rows
            #self.data = [[j.strip() for j in i] for i in rows]
            self.data = [line for line in f]
            
            self.headers = self.data[0]
    def buildDatabaseHeaders(self):
        for v,i in enumerate(self.headers):
            if len(i) == 0:
                self.dbHeaders.append(self.headers[v-1].lower() + "_count")
            else:
                self.dbHeaders.append(self.headers[v].lower())
        self.dbHeaders[0] = "station"

    def buildValueDictionary(self, row):
        parsingDictionary = {
            "station":(1,6),
            "wban":(8,12),
            "yearmoda":(15,22),
            "temp":(25,30),
            "temp_count":(32,33),
            "dewp":(36,41),
            "dewp_count":(43,44),
            "slp":(47,52),
            "slp_count":(54,55),
            "stp":(58,63),
            "stp_count":(65,66),
            "visib":(69,73),
            "visib_count":(75,76),
            "wdsp":(79,83),
            "wdsp_count":(85,86),
            "mxspd":(89,93),
            "gust":(96,100),
            "max_temp":(103,108),
            "max_temp_flag":(109,109),
            "min_temp":(111,116),
            "min_temp_flag":(117,117),
            "prcp":(119,123),
            "prcp_flag":(124,124),
            "sndp":(126,130),
            "frshtt":(133,138)
            }
    
        valueDictionary = {
            "station":None,
            "wban":None,
            "yearmoda":None,
            "temp":None,
            "temp_count":None,
            "dewp":None,
            "dewp_count":None,
            "slp":None,
            "slp_count":None,
            "stp":None,
            "stp_count":None,
            "visib":None,
            "visib_count":None,
            "wdsp":None,
            "wdsp_count":None,
            "mxspd":None,
            "gust":None,
            "max_temp":None,
            "max_temp_flag":None,
            "min_temp":None,
            "min_temp_flag":None,
            "prcp":None,
            "prcp_flag":None,
            "sndp":None,
            "frshtt":None,
            }
    
        typeDictionary = {
            "station":"int",
            "wban":"int",
            "yearmoda":"datetime",
            "temp":"float",
            "temp_count":"int",
            "dewp":"float",
            "dewp_count":"int",
            "slp":"float",
            "slp_count":"int",
            "stp":"float",
            "stp_count":"int",
            "visib":"float",
            "visib_count":"int",
            "wdsp":"float",
            "wdsp_count":"int",
            "mxspd":"float",
            "gust":"float",
            "max_temp":"float",
            "max_temp_flag":"bool",
            "min_temp":"float",
            "min_temp_flag":"bool",
            "prcp":"float",
            "prcp_flag":"char",
            "sndp":"float",
            "frshtt":"int",
            }
            
        for key in valueDictionary.keys():
            start = parsingDictionary[key][0]-1
            end = parsingDictionary[key][1]
            uncastVal = row[start:end]
            if typeDictionary[key] == "int":
                valueDictionary[key] = int(uncastVal)
            elif typeDictionary[key] == "float":
                tempVal = float(uncastVal)
                if tempVal == 999.9 or tempVal==9999.9:
                    valueDictionary[key] = None
                else:
                    valueDictionary[key] = tempVal
            elif typeDictionary[key]== "char":
                valueDictionary[key] = str(uncastVal)
            elif typeDictionary[key] == "datetime":
                valueDictionary[key] = datetime.datetime.strptime(uncastVal, "%Y%m%d")
            elif typeDictionary[key] == "bool":
                if "*" in uncastVal:
                    valueDictionary[key] = True
                else:
                    valueDictionary[key] = False
        return valueDictionary
    
    def executeLoad(self):
        cursor = self.connection.cursor()
        for row in self.data[1:]:
            loadDict = self.buildValueDictionary(row)
            cursor.execute(""" INSERT INTO noaa_gsod (station, wban, yearmoda, temp, temp_count, dewp, dewp_count, slp, slp_count, stp, stp_count, visib, visib_count, wdsp, wdsp_count, mxspd, gust, max_temp, max_temp_flag, min_temp, min_temp_flag, prcp, prcp_flag, sndp, frshtt)
                            VALUES(%(station)s, %(wban)s, %(yearmoda)s, %(temp)s, %(temp_count)s, %(dewp)s, %(dewp_count)s, %(slp)s, %(slp_count)s, %(stp)s, %(stp_count)s, %(visib)s, %(visib_count)s, %(wdsp)s, %(wdsp_count)s, %(mxspd)s, %(gust)s, %(max_temp)s, %(max_temp_flag)s, %(min_temp)s, %(min_temp_flag)s, %(prcp)s, %(prcp_flag)s, %(sndp)s, %(frshtt)s);""",
                            {'station':loadDict['station'], 'wban':loadDict['wban'], 'yearmoda':loadDict['yearmoda'], 'temp':loadDict['temp'], 'temp_count':loadDict['temp_count'], 'dewp':loadDict['dewp'], 'dewp_count':loadDict['dewp_count'], 'slp':loadDict['slp'], 'slp_count':loadDict['slp_count'], 'stp':loadDict['stp'], 'stp_count':loadDict['stp_count'], 'visib':loadDict['visib'], 'visib_count':loadDict['visib_count'], 'wdsp':loadDict['wdsp'], 'wdsp_count':loadDict['wdsp_count'], 'mxspd':loadDict['mxspd'], 'gust':loadDict['gust'], 'max_temp':loadDict['max_temp'], 'max_temp_flag':loadDict['max_temp_flag'], 'min_temp':loadDict['min_temp'], 'min_temp_flag':loadDict['min_temp_flag'], 'prcp':loadDict['prcp'], 'prcp_flag':loadDict['prcp_flag'], 'sndp':loadDict['sndp'], 'frshtt':loadDict['frshtt']})
        self.connection.commit()
        del cursor
    
    def getColumnNames(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM noaa_gsod LIMIT 0")
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        del cursor
        return colnames
    def retrieveAll(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM noaa_gsod")
        rows = cursor.fetchall()
        cursor.close()
        del cursor
        return rows


"""
with open(r'C:\GISData\WKP Data\Flat Data\CLEAN CDO\hourly\shell_point_simple.txt') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    trash = reader.next()
    rows = [row for row in reader]

data = [[item for item in row if len(item)!= 0] for row in rows]
with open(r'C:\GISData\WKP Data\Flat Data\CLEAN CDO\hourly\shell_point_simple.txt', 'r') as f:
    unsplitHeader = f.readline()

header = unsplitHeader.split()

"""