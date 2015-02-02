# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 10:02:28 2014

@author: Bassett_S
"""
import datetime, os, csv, psycopg2, re, shutil, decimal
import numpy as np

def calculateWLEs(connection_info):
    connection = psycopg2.connect(dsn=None, 
            host= connection_info[0],
            database= connection_info[1],
            user= connection_info[2],
            password= connection_info[3])
    cursor = connection.cursor()


    for i in range(30,35):
        print "Calculating {0}".format(i)
        cursor.execute("SELECT date_time, deploy_key, pres, zpo, insitu_id FROM insitu WHERE deploy_key = %s",(i,))
        table = cursor.fetchall()
        cursor.execute("SELECT adj_trans_elev, vented FROM insitu_transducer WHERE deploy_key = %s",(i,))
        trans_elev = float(cursor.fetchall()[0][0])
        for row in table:
            #cast data
            dt = row[0].strftime("%Y-%m-%d 00:00:00 UTC")
            insitu_pres = float(row[2])
            insitu_zpo = float(row[3])
            insitu_id = int(row[4])
            
            #get daily barometric pressures
            cursor.execute("SELECT yearmoda, stp FROM noaa_gsod WHERE station = 722140 AND yearmoda = TIMESTAMP %s",(dt,))            
            gsod_row = cursor.fetchall()[0]
            
            #run conversions
            #first cast stp column (millibars) to float      
            millibars = float(gsod_row[1])
            
            #convert millibars to PSI
            gsod_psi = millibars * 0.0145037738
            
            #calculate WLE in meters and convert to feet
            
            wle = (((((insitu_pres + insitu_zpo) - gsod_psi) * 0.703073) / 0.999) + trans_elev) * 3.28084

            #execute insert            
            cursor.execute("INSERT INTO insitu_wle (insitu_id, wle) VALUES (%s,%s)", (insitu_id,wle))
        #commmit changes and close connections
        connection.commit()
    cursor.close()
    connection.close()
    del cursor
    del connection
        
        
        
        
        

def checkStatistics(path, connection_info):
    files = os.listdir(path)
    filePaths = [os.path.join(path, i) for i in files]
    stats = {}
    for i in Insitu.validHeaders:
        stats[i] = []

    for i in filePaths:
        tf = Insitu(i, connection_info)
        tf.parse()
        tf.check()
        fileStats = tf.calculateStats()
        
    return stats

def loadDirectory(path, connection_info):
    """Load a directory of insiut files into the database"""
    files = os.listdir(path)
    filePaths = [os.path.join(path, i) for i in files]
    rowCount = 0
    compiledStatus = []    
    for v,i in enumerate(filePaths):
        tf = Insitu(i, connection_info)
        tf.parse()
        tf.check()
        print "Loading {0} of {1}".format(v+1, len(filePaths))
        tf.load()
        if tf.status["loaded"] == True:
            rowCount += len(tf.castData)
        compiledStatus.append([tf.path, tf.status])
    #return compiledStatus

def shutilDirectory(inPath, outPath, connection_info):
    """Copy a directory of insitu files and rename in a standard format"""
    files = os.listdir(inPath)
    filePaths = [os.path.join(inPath, i) for i in files]
    uniqueName = os.path.split(inPath)[1]
    for i in filePaths:
        tf = Insitu(i, connection_info)
        tf.parse()
        startDate = datetime.datetime.strftime(tf.keyDict["tstart"], "%Y%m%d")
        endDate = datetime.datetime.strftime(tf.keyDict["tend"], "%Y%m%d")
        tfNewName = uniqueName + "_" + startDate + "_" + endDate
        tfNewPath = os.path.join(outPath,tfNewName)
        shutil.copy(i, tfNewPath)

        
def preloadReport(path, reportDirectory, connection_info):
    """Generate a preload report for all files in a directory"""
    files = os.listdir(path)
    uniqueName = os.path.split(path)[1]
    filePaths = [os.path.join(path, i) for i in files]
    reportPath = os.path.join(reportDirectory, "insituPreloadReport_"+uniqueName+".txt")
    with open(reportPath, 'a') as f:
        f.write("\n")
        f.write("#"*40)
        f.write("\n")
        f.write("NEW FOLDER SUMMARY\n")
        f.write(str(path))
        f.write("\n")
        f.write(datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"))
        f.write("\n")
        f.write("\n")
        for i in filePaths:
            tf = Insitu(i, connection_info)
            tf.parse()
            tf.check()
            f.write(os.path.split(tf.path)[1])
            f.write("\n")
            for i in tf.problems:
                f.write(i)
                f.write("\n")
            f.write("Downloaded     : %s\n" % tf.keyDict["download"])
            f.write("Site           : %s\n" % tf.keyDict["site"])
            f.write("Serial #       : %s\n" % tf.keyDict["serial"])
            f.write("Device         : %s\n" % tf.keyDict["device"])
            f.write("# Records      : %s\n" % tf.keyDict["records"])
            f.write("Start DT       : %s\n" % tf.keyDict["tstart"])
            f.write("End DT         : %s\n" % tf.keyDict["tend"])
            f.write("Deploy Key     : %s\n" % tf.keyDict["deploykey"])
            f.write("Cal Info       : %s\n" % tf.keyDict["calibration"])
            f.write("GMT Info       : %s\n" % tf.keyDict["GMT"])
            f.write("ZPO            : %s\n" % tf.keyDict["ZPO"])
            f.write("# Headers      : %s\n" % str(len(tf.headers)))            
            f.write("# Data Columns : %s\n" % str(len(tf.castData[0])))
            f.write("File Parsed    : %s\n" % tf.status["parsed"])
            f.write("Headers OK     : %s\n" % tf.status["headers"])
            f.write("Cast OK        : %s\n" % tf.status["cast"])
            f.write("Deploy Key OK  : %s\n" % tf.status["deploykey"])
            f.write("Insitu Table OK: %s\n" % tf.status["table"])
            f.write("Headers        :\t")            
            for i in tf.headers:
                f.write(str(i))
                f.write("\t---\t")
            f.write("\n")
            for i in tf.log:
                f.write(str(i))
                f.write("\n")
            f.write("\n")
        f.write("#"*40)
def postloadReport(path, reportDirectory, connection_info):
    """Generate a preload report for all files in a directory"""
    files = os.listdir(path)
    uniqueName = os.path.split(path)[1]
    filePaths = [os.path.join(path, i) for i in files]
    reportPath = os.path.join(reportDirectory, "insituPostloadReport_"+uniqueName+".txt")
    with open(reportPath, 'a') as f:
        f.write("\n")
        f.write("#"*40)
        f.write("\n")
        f.write("NEW FOLDER SUMMARY\n")
        f.write(str(path))
        f.write("\n")
        f.write(datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"))
        f.write("\n")
        f.write("\n")
        for i in filePaths:
            tf = Insitu(i, connection_info)
            tf.parse()
            tf.check()
            tf.checkStatistics()
            tf.checkItems()
            f.write(tf.path)
            f.write("\n")
            f.write("Deploy Key     : %s\n" % tf.keyDict["deploykey"])
            f.write("# Rows         : %s\n" % tf.keyDict["records"])
            f.write("Stats Check    : %s\n" % tf.keyDict["stats"])
            f.write("Item Check     : %s\n" % tf.keyDict["items"])
        f.write("#"*40)


def serialReport(path, reportDirectory, connection_info):
    """Generate a preload report for all files in a directory"""
    files = os.listdir(path)
    uniqueName = os.path.split(path)[1]
    filePaths = [os.path.join(path, i) for i in files]
    reportPath = os.path.join(reportDirectory, "insituSerialReport_"+uniqueName+".txt")
    serialMin = {}
    serialMax = {}
    with open(reportPath, 'a') as f:
        f.write("\n")
        f.write("#"*40)
        f.write("\n")
        f.write("NEW FOLDER SUMMARY\n")
        f.write(str(path))
        f.write("\n")
        f.write(datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"))
        f.write("\n")
        f.write("\n")
        for i in filePaths:
            tf = Insitu(i, connection_info)
            tf.parse()
            if tf.keyDict["serial"] not in serialMin.keys():
                serialMin[tf.keyDict["serial"]] = tf.keyDict["tstart"] + datetime.timedelta(hours=5)
            elif tf.keyDict["serial"] in serialMin.keys():
                if tf.keyDict["tstart"] < serialMin[tf.keyDict["serial"]] and tf.keyDict["tstart"] > datetime.datetime(1980, 1, 1):
                    serialMin[tf.keyDict["serial"]] = tf.keyDict["tstart"] + datetime.timedelta(hours=5)
            if tf.keyDict["serial"] not in serialMax.keys():
                serialMax[tf.keyDict["serial"]] = tf.keyDict["tend"] + datetime.timedelta(hours=5)
            elif tf.keyDict["serial"] in serialMax.keys():
                if tf.keyDict["tend"] > serialMax[tf.keyDict["serial"]]:
                    serialMax[tf.keyDict["serial"]] = tf.keyDict["tend"]+ datetime.timedelta(hours=5)
        for keys in serialMin:
            f.write("Serial: %s\n" % keys)
            f.write("Min   : %s\n" % serialMin[keys])
            f.write("Max   : %s\n" % serialMax[keys])
            f.write("\n")

            
  

class Insitu:
    """Common base class for all insitu files"""
    validHeaders = ["Water Density (g/cm3)",
                "Depth (ft)",
                "Temperature (C)",
                "Seconds",
                "Total Dissolved Solids (ppt)",
                "Depth (in)",
                "Depth (cm)",
                "Salinity (PSU)",
                "Specific Conductivity (\xb5S)",
                "Pressure (PSI)",
                "Resistivity (ohm-cm)",
                "Actual Conductivity (µS)",
                "Date and Time"]



    dbToRaw = {'date_time': 'Date and Time',
               'resistivity': 'Resistivity (ohm-cm)',
               'cond_specific': 'Specific Conductivity (\xb5S)',
               'temp': 'Temperature (C)',
               'total_dissolved_solids':'Total Dissolved Solids (ppt)',
               'water_density': 'Water Density (g/cm3)',
               'cond_actual': 'Actual Conductivity (\xb5S)',
               'salinity': 'Salinity (PSU)',
               'elapsed_seconds': 'Seconds',
               'depth': 'Depth (ft)',
               'pres': 'Pressure (PSI)'}
    
    rawToDB = {"Water Density (g/cm3)":"water_density",
       "Depth (ft)":"depth",
       "Temperature (C)":"temp",
       "Seconds":"elapsed_seconds",
       "Total Dissolved Solids (ppt)":"total_dissolved_solids",
       "Salinity (PSU)":"salinity",
       "Specific Conductivity (\xb5S)":"cond_specific",
       "Pressure (PSI)":"pres",
       "Resistivity (ohm-cm)":"resistivity",
       "Actual Conductivity (µS)":"cond_actual",
       "Date and Time":"date_time"}
               
    def __init__(self, path, connection_info):
        self.path = path
        self.connection = psycopg2.connect(dsn=None, 
            host= connection_info[0],
            database= connection_info[1],
            user= connection_info[2],
            password= connection_info[3])
        self.status = {
            "parsed": None,
            "headers": None,
            "cast": None,
            "deploykey": None,
            "table": None,
            "loaded": None,
            "greenlit":None
            }
        self.data = []
        self.castData = []
        self.headers = []
        self.keyDict = {
            "download":None,
            "site":None,
            "serial":None,
            "device":None,
            "records":None,
            "tstart":None,
            "tend":None,
            "deploykey":None,
            "calibration":None,
            "GMT":None,
            "ZPO": None,
            "stats": None,
            "items": None
            }

        self.rowDict = {}
        self.problems = []
        self.log = []
        
    def __del__(self):
        self.connection.close()
    
    def infoMeta(self):
        print self.path
        print "Downloaded: %s" % self.keyDict["download"]
        print "Site      : %s" % self.keyDict["site"]
        print "Serial #  : %s" % self.keyDict["serial"]
        print "Device    : %s" % self.keyDict["device"]
        print "# Records : %s" % self.keyDict["records"]
        print "Start DT  : %s" % self.keyDict["tstart"]
        print "End DT    : %s" % self.keyDict["tend"]
        print "Deploy Key: %s" % self.keyDict["deploykey"]
        print "Cal Info  : %s" % self.keyDict["calibration"]
        print "GMT Info  : %s" % self.keyDict["GMT"]
        print "ZPO       : %s" % self.keyDict["ZPO"]
    
    def infoStatus(self):
        print "File Parsed    : %s" % self.status["parsed"]
        print "Headers OK     : %s" % self.status["headers"]
        print "Cast OK        : %s" % self.status["cast"]
        print "Deploy Key OK  : %s" % self.status["deploykey"]
        print "Insitu Table OK: %s" % self.status["table"]
        print "Loaded into DB : %s" % self.status["loaded"]
        
    def parse(self):
        """Basic parsing of insitu file""" 
    #try:
        with open(self.path) as f:
            reader = csv.reader(f)
            rows = []        
            for row in reader:
                thisRow = []
                for i in row:
                    value = i.strip()
                    thisRow.append(value)
                rows.append(thisRow)
        self.data = rows
        self.keyDictionary()
        self.keyRows()
        self.findMinMaxTimestamp()
        self.findCalibration()
        self.findGMTflag()
        self.findZPO()
        self.status["parsed"] = True
    #except:
#        print "Parsing Failed"
#        self.status["parsed"] = False
#        self.problems.append("Failed to parse")
    def convertDepth(self):
        convertedDepths = []
        if "Depth (cm)" in self.headers:
            for row in self.castData:
                for i, j in zip(self.headers, row):
                    if i == 'Depth (cm)':
                        convertedDepths.append(round(j * 0.0328084, 3))
        for rowpos, (depth, row) in enumerate(zip(convertedDepths, self.castData[:])):
            for itempos, cname in enumerate(self.headers):
                if cname == "Depth (cm)":
                    self.castData[rowpos][itempos] = depth
        
    def check(self):
        if self.status["parsed"] == True:
            self.checkHeaders()
            self.cast()
            self.convertDepth()
            self.checkDeployKey()
            if self.keyDict["deploykey"] ==  "*INVALID*":
                self.status["table"] == "SKIPPED"
                self.status["loaded"] == "NO DEPLOY KEY"                
                pass
            else:
                self.checkTable()
        elif self.status["parsed"] == None:
            print "Parse data before checking"
        elif self.status["parsed"] == False:
            print "There was a failure parsing - please correct"
        
        
    def load(self):
        """DOCSTRING"""
        if all(self.status.values()):
            print os.path.split(self.path)[1], "has not been greenlit, skipping"
            return
        else:
            #print os.path.split(self.path)[1],"File greenlit, loading"
            for v, row in enumerate(self.castData):
                self.executeLoad(self.createLoadDict(row))
            self.connection.commit()
            self.status["loaded"] = True
            print os.path.split(self.path)[1], "loaded successfully"
    def checkItems(self):
        startTS = self.returnUTCtimestamp(self.keyDict["tstart"])
        startTS = "\'" + startTS + "\'"
        endTS = self.returnUTCtimestamp(self.keyDict["tend"])
        endTS = "\'" + endTS + "\'"
        cursor = self.connection.cursor()
        truncatedHeaders = [i for i in self.headers if i != 'Date and Time']
        position = {}
        for v,i in enumerate(self.headers):
            position[i]=v
        flag = None
        for column in truncatedHeaders:
            cursor.execute("""SELECT date_time, %s FROM insitu WHERE date_time >= %s AND date_time <= %s AND deploy_key = %s;""" % (self.rawToDB[column],startTS,endTS, self.keyDict["deploykey"]))
            dbTable = cursor.fetchall()
            dbTable = sorted(dbTable, key = lambda datetime: datetime[0])
            for x,y in zip(dbTable,self.castData):
                if type(x[1]) is long:
                    if int(x[1]) != y[position[column]]:
                        flag = False
                elif type(x[1]) is decimal.Decimal:
                    if float(x[1]) != y[position[column]]:
                        flag=False
        if flag is None:
            self.keyDict["items"] = True
        elif flag is False:
            self.keyDict["items"] = False
                    
        cursor.close()
        del cursor
                
            
    def checkStatistics(self, debug=False):
        fData = self.calculateStats()
        dbData = self.dbStats()
        agreement = {
            'min':[],
            'mean':[],
            'max':[],
            'count':[],
            'sum':[]}
        values = {
            'min':[],
            'mean':[],
            'max':[],
            'count':[],
            'sum':[]}
        for i in dbData.keys():
            for j,k in zip(fData[i], dbData[i]):
                if round(float(j),3) == round(float(k),3):
                    agreement[i].append(True)
                    values[i].append((True, True))
                else:
                    agreement[i].append(False)
                    values[i].append((round(float(j),3), float(k)))
        flag = None
        for key in agreement.keys():
            if False in agreement[key]:
                flag = False
        if flag is None:
            self.keyDict["stats"] = True
        elif flag is False:
            self.keyDict["stats"] = False
        if debug is True:
            return [agreement, values]
    def calculateStats(self):
        data = [i[1:] for i in self.castData]
        nparr = np.array(data)
        stats = {
            "min": np.amin(nparr, axis=0),
            "mean": np.average(nparr, axis=0),
            "max": np.amax(nparr, axis=0),
            "count": [len(data)] * len(data[0]),
            "sum": np.sum(nparr, axis=0)
            }
        return stats
    def dbStats(self):
        cursor = self.connection.cursor()
        dbStats = {
            "min": [],
            "mean": [],
            "max": [],
            "count": [],
            "sum": []
            }
        startTS = self.returnUTCtimestamp(self.keyDict["tstart"])
        startTS = "\'" + startTS + "\'"
        endTS = self.returnUTCtimestamp(self.keyDict["tend"])
        endTS = "\'" + endTS + "\'"
        dKey = self.keyDict["deploykey"]
        for i in self.headers:            
            if i != "Date and Time":
                statsName = ["count", "min", "max", "sum", "mean"]
                cursor.execute("SELECT COUNT(%s), MIN(%s), MAX(%s), SUM(%s), AVG(%s) FROM insitu WHERE date_time >= %s and date_time <= %s AND deploy_key = %s" % (self.rawToDB[i], self.rawToDB[i], self.rawToDB[i], self.rawToDB[i], self.rawToDB[i], startTS, endTS, dKey))
                stats = cursor.fetchall()[0]
                for j,k in zip(statsName, stats):
                    if type(k) is long:
                        dbStats[j].append(int(k))
                    elif type(k) is decimal.Decimal:
                        dbStats[j].append(float(k))
        cursor.close()
        del cursor
        return dbStats
                
        
    def findCalibration(self):
        log = []
        for i in self.data[self.rowDict["log"]:]:
            if len(i) > 0:
                log.append(i)
            else: break
        expire = []
        for i in log:
            for j in i:
                if "Factory calibration has expired" in j:
                    expire.append(j)
        if len(expire) == 0:
            self.keyDict["calibration"] = False
        else:
            reexp = re.compile('[0-9]{1,2}/[0-9]{1,2}/[0-9]{4,4} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2} [AP]M')
            match = reexp.search(expire[0])
            expireDate = match.group()
            expireDateTime = datetime.datetime.strptime(expireDate, '%m/%d/%Y %H:%M:%S %p')
            self.keyDict["calibration"] = expireDateTime
        
    def findGMTflag(self):
        log = []
        for i in self.data[self.rowDict["log"]:]:
            if len(i) > 0:
                log.append(i)
            else: break
        self.log = log
        expire = []
        for i in log:
            for j in i:
                if "GMT" in j:
                    expire.append(j)
                    self.keyDict["GMT"]=True
        if len(expire) == 0:
            pass
        else:
            self.keyDict["GMT"] = True
#            reexp = re.compile('[0-9]{1,2}/[0-9]{1,2}/[0-9]{4,4} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2} [AP]M')
#            match = reexp.search(expire[0])
#            expireDate = match.group()
#            expireDateTime = datetime.datetime.strptime(expireDate, '%m/%d/%Y %H:%M:%S %p')
#            self.keyDict["calibration"] = expireDateTime
                
    def findZPO(self):
        offset = 0

        for v,i in enumerate(self.data):
            if "Zero Pressure Offset:" in i:
                offset = float(self.data[v][i.index("Zero Pressure Offset:")+1])
        self.keyDict["ZPO"] = offset

            
    def keyDictionary(self):
        """Create the key dictionary"""
        for v, i in enumerate(self.data):
            if len(i) != 0:
                if i[0] == "Device":
                    self.keyDict["device"] = i[1]
                elif i[0] == 'Site':
                    self.keyDict["site"] = i[1]
                elif i[0] == 'Serial Number':
                    self.keyDict["serial"] = i[1]
                elif i[0] == 'Record Count':
                    self.keyDict["records"] = i[1]
                elif i[0] == "Create Date":
                    self.keyDict["download"] = datetime.datetime.strptime(i[1], '%m/%d/%Y %I:%M:%S %p')
        

        
    def keyRows(self):
        """Row number keyed by device info, site, serial #, record count, and date and time as a dict"""
        key = {}
        for v, i in enumerate(self.data):
            if len(i) != 0:
                if i[0] == "Device":
                    key["device"] = v
                elif i[0] == 'Site':
                    key["site"] = v
                elif i[0] == 'Serial Number':
                    key["serial"] = v
                elif i[0] == 'Record Count':
                    key["records"] = v
                elif i[0] == 'Date and Time':
                    key["header"] = v
                    key["data"] = v + 1
                elif i[0] == 'Log Notes:':
                    key["log"] = v
        self.rowDict = key
        
    def findMinMaxTimestamp(self):
        """Find min/max timestamps for an insitu file"""
        dates = []
        startRow = self.rowDict["data"]
        for i in self.data[startRow:]:
            if len(i)!=0:
                timestamp = datetime.datetime.strptime(i[0], '%m/%d/%Y %I:%M:%S %p')
                dates.append(timestamp)
        minDate = min(dates)
        maxDate = max(dates)
        self.keyDict["tstart"] = minDate
        self.keyDict["tend"] = maxDate



    def checkHeaders(self):
        header = self.data[self.rowDict["header"]]
        parsedHeader = [i for i in header if len(i)>0]
        self.headers = parsedHeader
        for i in parsedHeader:
            if i in self.validHeaders and self.status["headers"] != False:
                self.status["headers"] = True
            elif i not in self.validHeaders:
                self.status["headers"] = False
                problem = "Header" + str(i) + "not valid"
                self.problems.append(problem)
            
        
    def cast(self):
        """Cast data table into proper types"""
        dataStart = self.rowDict["data"]
        castRows = []
        try:
            for i in self.data[dataStart:]:
                if len(i) > 0:                
                    thisRow = []
                    for v, j in enumerate(i):
                        if v == 0 and len(j) != 0:
                            thisRow.append(datetime.datetime.strptime(j, '%m/%d/%Y %I:%M:%S %p'))
                        elif len(j)!=0:
                            thisRow.append(float(j))
                            
                    castRows.append(thisRow)
            self.castData = castRows
            self.status["cast"] = True
        except:
            print "Casting Failed"
            self.status["cast"] = False
            self.problems.append("Failed to cast")
     
    def checkDeployKey(self):
        """Checks deploy table for a valid deploy key"""
        cursor = self.connection.cursor()
        
        #Converts to UTC
        startTS = self.returnUTCtimestamp(self.keyDict["tstart"])
        endTS = self.returnUTCtimestamp(self.keyDict["tend"])
        
        cursor.execute("""SELECT deploy_key FROM deploy_info WHERE serial_number= %s AND start_dt <= TIMESTAMP %s AND end_dt >= TIMESTAMP %s""", (self.keyDict["serial"], startTS, endTS))
        deploy_key = cursor.fetchall()
        if len(deploy_key) == 1:
            self.keyDict["deploykey"] = deploy_key[0][0]
            self.status["deploykey"] = True
        else:
            self.keyDict["deploykey"] = "*INVALID*"
            self.status["deploykey"] = False
            self.problems.append("Could not find deploy key")
        del cursor 
        
        
    def returnUTCtimestamp(self, ts):
        textTS = datetime.datetime.strftime(ts+datetime.timedelta(hours=5), "%Y-%m-%d %H:%M:%S UTC")
        return textTS
        
    def checkTable(self):
        """DOCSTRING"""
        cursor = self.connection.cursor()
        startTS = self.returnUTCtimestamp(self.keyDict["tstart"])
        endTS = self.returnUTCtimestamp(self.keyDict["tend"])
        cursor.execute("""SELECT * FROM insitu WHERE deploy_key = %s AND date_time >= TIMESTAMP %s AND date_time <= TIMESTAMP %s""", (self.keyDict["deploykey"], startTS, endTS))
        table = cursor.fetchall()
        if len(table) == 0:
            self.status["table"] = True
        else:
            self.status["table"] = False
            self.problems.append("File contains %s duplicate rows with insitu table" % str(len(table)))
        del cursor      
        
    def createLoadDict(self, row):
        """Create a dictionary of values to load into the database"""    
        headerDict = {}
        for v, i in enumerate(self.headers):
            headerDict[v] = i
        rawToDB = {"Water Density (g/cm3)":"water_density",
           "Depth (ft)":"depth", 
           "Depth (cm)":"depth",
           "Temperature (C)":"temp",
           "Seconds":"elapsed_seconds",
           "Total Dissolved Solids (ppt)":"total_dissolved_solids",
           "Salinity (PSU)":"salinity",
           "Specific Conductivity (\xb5S)":"cond_specific",
           "Pressure (PSI)":"pres",
           "Resistivity (ohm-cm)":"resistivity",
           "Actual Conductivity (\xb5S)":"cond_actual",
           "Date and Time":"date_time"}
        valueDict = {'deploy_key': self.keyDict["deploykey"],
           'date_time': None,
           'resistivity': None,
           'cond_specific': None,
           'temp': None,
           'total_dissolved_solids':None,
           'water_density': None,
           'cond_actual': None,
           'salinity': None,
           'elapsed_seconds': None,
           'depth': None,
           'pres': None,
           'calculated_wle':None,
           'calibration':None}
        for v, i in enumerate(row):
            valueDict[rawToDB[headerDict[v]]] = i
        dtIndex = self.headers.index("Date and Time")
        if self.keyDict["calibration"] is False:
                valueDict["calibration"] = True
        elif type(self.keyDict["calibration"]) is datetime.datetime:
            if row[dtIndex] > self.keyDict["calibration"]:
                valueDict["calibration"] = False
            
        return valueDict

    def executeLoad(self, rowDict):
        """Executes load of values into the database"""
        cursor = self.connection.cursor()
        cursor.execute("""INSERT INTO insitu (deploy_key, date_time, elapsed_seconds, pres, temp, depth, cond_actual, cond_specific, salinity, tds, resistivity, water_density, calibration, zpo) 
                    values(%(deploy_key)s, %(date_time)s, %(elapsed_seconds)s, %(pres)s, %(temp)s, %(depth)s, %(cond_actual)s, %(cond_specific)s, %(salinity)s, %(tds)s, %(resistivity)s, %(water_density)s, %(calibration)s, %(zpo)s);""",
                    {'deploy_key':rowDict["deploy_key"], 'date_time':self.returnUTCtimestamp(rowDict["date_time"]), 'elapsed_seconds':rowDict["elapsed_seconds"], 'pres':rowDict["pres"], 'temp':rowDict["temp"], 'depth':rowDict["depth"], 'cond_actual':rowDict["cond_actual"], 'cond_specific':rowDict["cond_specific"], 'salinity':rowDict["salinity"], 'tds':rowDict["total_dissolved_solids"], 'resistivity':rowDict['resistivity'], 'water_density':rowDict['water_density'], "calibration":rowDict['calibration'], "zpo":self.keyDict["ZPO"]})
        del cursor
    
    def calculateWLE(self, rowDict):
        cursor = self.connection.cursor()
        cursor.execute("SELECT adj_trans_elev FROM insitu_transducer WHERE deploy_key = %s" % str(rowDict["deploy_key"]))
        row = cursor.fetchall()
        transElev = float(row[0][0])
        pressure = rowDict['pres'] + self.keyDict["ZPO"]
        head = (pressure * 2.31) / 0.999
        wle = round((transElev + head), 3)
        rowDict["calculated_wle"] = wle
        return rowDict