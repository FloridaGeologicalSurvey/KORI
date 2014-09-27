# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 10:01:44 2014

@author: Bassett_S
"""
import datetime, psycopg2,  psycopg2.extras, csv, os

validHeaders = ["Water Density (g/cm3)",
                "Depth (ft)",
                "Temperature (C)",
                "Seconds",
                "Total Dissolved Solids (ppt)",
                "Depth (in)",
                "Depth (cm)",
                "Salinity (PSU)",
                "Specific Conductivity (µS)",
                "Pressure (PSI)",
                "Resistivity (ohm-cm)",
                "Actual Conductivity (µS)",
                "Date and Time"]

rawToDB = {"Water Density (g/cm3)":"water_density",
           "Depth (ft)":"depth",
           "Temperature (C)":"temp",
           "Seconds":"elapsed_seconds",
           "Total Dissolved Solids (ppt)":"total_dissolved_solids",
           "Salinity (PSU)":"salinity",
           "Specific Conductivity (µS)":"cond_specific",
           "Pressure (PSI)":"pres",
           "Resistivity (ohm-cm)":"resistivity",
           "Actual Conductivity (µS)":"cond_actual",
           "Date and Time":"date_time"}


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

valueDict = {"Water Density (g/cm3)":None,
           "Depth (ft)":None,
           "Temperature (C)":None,
           "Seconds":None,
           "Total Dissolved Solids (ppt)":None,
           "Salinity (PSU)":None,
           "Specific Conductivity (µS)":None,
           "Pressure (PSI)":None,
           "Resistivity (ohm-cm)":None,
           "Actual Conductivity (µS)":None,
           "Date and Time":None}

def parse(insituPath):
    """Basic parsing of insitu file"""  
    with open(insituPath) as f:
        reader = csv.reader(f)
        rows = []        
        for row in reader:
            thisRow = []
            for i in row:
                value = i.strip()
                thisRow.append(value)
            rows.append(thisRow)
    return rows


def keyList(data):
    """Returns device info, site, serial #, record counts, and header info as a list"""
    for v, i in enumerate(data):
        if len(i) != 0:
            if i[0] == "Device":
                device = ["device", i[1], v, i.index(i[1])]
            elif i[0] == 'Site':
                site = ["site", i[1], v, i.index(i[1])]
            elif i[0] == 'Serial Number':
                serial = ["serial", i[1], v, i.index(i[1])]
            elif i[0] == 'Record Count':
                recordCount = ["records", i[1], v, i.index(i[1])]
            elif i[0] == "Date and Time":
                header = ["dataHeader", i, v, i.index(i[1])]
    masterList = [device, site, serial, recordCount, header]
    return masterList

def keyDictionary(data):
    """Returns device info, site, serial #, record count, and creation date as a dictionary"""
    key = {}
    for v, i in enumerate(data):
        if len(i) != 0:
            if i[0] == "Device":
                key["device"] = i[1]
            elif i[0] == 'Site':
                key["site"] = i[1]
            elif i[0] == 'Serial Number':
                key["serial"] = i[1]
            elif i[0] == 'Record Count':
                key["records"] = i[1]
            elif i[0] == "Create Date":
                key["download"] = datetime.datetime.strptime(i[1], '%m/%d/%Y %I:%M:%S %p')
    return key

def keyRows(data):
    """Returns row number keyed by device info, site, serial #, record count, and date and time as a dict"""
    key = {}
    for v, i in enumerate(data):
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
    return key

def castData(data, rowKey):
    """Cast data table into proper types"""
    dataStart = rowKey["data"]
    castRows = []   
    for i in data[dataStart:]:
        thisRow = []
        for v, j in enumerate(i):
            if v == 0 and len(j) != 0:
                thisRow.append(datetime.datetime.strptime(j, '%m/%d/%Y %I:%M:%S %p'))
            elif len(j)!=0:
                thisRow.append(float(j))
                
        castRows.append(thisRow)      
                
    return castRows

def findMinMaxTimestamp(data, startRow):
    """Find min/max timestamps for an insitu file"""
    dates = []
    for i in data[startRow:]:
        if len(i)!=0:
            timestamp = datetime.datetime.strptime(i[0], '%m/%d/%Y %I:%M:%S %p')
            dates.append(timestamp)
    minDate = min(dates)
    maxDate = max(dates)
    return [minDate, maxDate]

def buildSerialMinMax(inputPath):
    """Finds the MinMax Timestamp by serial number for a directory of files"""
    print "Building Serial Tables..."
    inputFiles = os.listdir(inputPath)
    serials = []
    minmaxTS = {}
    for f in inputFiles:
        path = os.path.join(inputPath, f)
        data = parse(path)
        keyInfo = keyDictionary(data)
        if keyInfo["serial"] not in serials: 
            serials.append(keyInfo["serial"])
    for i in serials:
        minmaxTS[i] = [datetime.datetime(9999, 1, 1), datetime.datetime(1, 1, 1)]
    for f in inputFiles:
        path = os.path.join(inputPath, f)
        data = parse(path)
        key = keyRows(data)
        keyInfo = keyDictionary(data)
        minmaxTimestamp = findMinMaxTimestamp(data, key["data"])
        if minmaxTimestamp[0] < minmaxTS[keyInfo["serial"]][0]:
            minmaxTS[keyInfo["serial"]][0] = minmaxTimestamp[0]
        if minmaxTimestamp[1] > minmaxTS[keyInfo["serial"]][1]:
            minmaxTS[keyInfo["serial"]][1] = minmaxTimestamp[1]    
    print "Serial table built"
    return minmaxTS

def testDeployTable(serialTable):
    serials = serialTable.keys()
    for i in serials:
        minTS = serialTable[i][0].strftime("%Y-%m-%d %H:%M:%S")
        maxTS = serialTable[i][1].strftime("%Y-%m-%d %H:%M:%S")
        

    
    
def testFiles(inputPath):
    print "Testing Files..."
    minmaxTS = buildSerialMinMax(inputPath)
    files=os.listdir(inputPath)
    for f in files:
        path = os.path.join(inputPath, f)


        
    
def loadDict(row, header):
    """Create a dictionary of values to load into the database"""    
    headerDict = {}
    for v, i in enumerate(header):
        headerDict[v] = i
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
    valueDict = {'date_time': None,
               'resistivity': None,
               'cond_specific': None,
               'temp': None,
               'total_dissolved_solids':None,
               'water_density': None,
               'cond_actual': None,
               'salinity': None,
               'elapsed_seconds': None,
               'depth': None,
               'pres': None}
    for v, i in enumerate(row):
        valueDict[rawToDB[headerDict[v]]] = i
    return valueDict
    
def checkLoad(deployKey, rowDict):
    """Check to see if datetime range already exists in the database"""    
    query = cur.mogrify("""SELECT * FROM insitu WHERE deploy_key = %s AND date_time = %s""", (deployKey, rowDict["date_time"]))
    cur.execute(query)
    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    elif len(rows) == 0:
        return False

def executeLoad(deployKey, rowDict):
    """Executes load of values into the database"""
    cur.execute("""INSERT INTO insitu (deploy_key, date_time, elapsed_seconds, pres, temp, depth, cond_actual, cond_specific, salinity, total_dissolved_solids, resistivity, water_density) 
                values(%(deploy_key)s, %(date_time)s, %(elapsed_seconds)s, %(pres)s, %(temp)s, %(depth)s, %(cond_actual)s, %(cond_specific)s, %(salinity)s, %(total_dissolved_solids)s, %(resistivity)s, %(water_density)s);""",
                {'deploy_key':deployKey, 'date_time':rowDict["date_time"], 'elapsed_seconds':rowDict["elapsed_seconds"], 'pres':rowDict["pres"], 'temp':rowDict["temp"], 'depth':rowDict["depth"], 'cond_actual':rowDict["cond_actual"], 'cond_specific':rowDict["cond_specific"], 'salinity':rowDict["salinity"], 'total_dissolved_solids':rowDict["total_dissolved_solids"], 'resistivity':rowDict['resistivity'], 'water_density':rowDict['water_density']})


def retrieveColumnNames(sqlQuery, connection_info):
    """
    Retrieves the Column names of an SQL table and returns a list
    """
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

def retrieveRows(sqlQuery, connection_info):
    """
    Very basic. Pass the function an SQL query, it returns the corresponding rows
    """
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

if "__name__" == "__main__":
    inputPath = r"C:\GISData\WKP Data\Flat Data\Original Sensor Data\In Situ Upload Bucket\Sullivan"
    inputFiles = os.listdir(inputPath)    
    pw = raw_input("DB Password:")
    alice = ["FGS-USRV","wkp_hrdb_dev","postgres",pw]
    
    
    con = psycopg2.connect(dsn=None, 
        host= alice[0],
        database= alice[1],
        user= alice[2],
        password= alice[3])
    cur = con.cursor()
    
    totalRows = 0
    fileCount = 1
    totalRaw = 0
    totalSkipped = 0
    skippedFiles = []
    for f in inputFiles:
        path = os.path.join(inputPath, f)
        print "\n"    
        print "-"*40
        print "File",fileCount,"of",len(inputFiles)
        print "Parsing", f
        data = parse(path)
        print "Building Row Key"
        key = keyRows(data)
        print "Compiling Key Values"    
        keyInfo = keyDictionary(data)
        print "Getting minmax dates for raw data"
        minmaxTimestamp = findMinMaxTimestamp(data, key["data"])
        minmaxDate = [minmaxTimestamp[0].date(), minmaxTimestamp[1].date()]
        print "Querying DB for deploy key"    
        query = cur.mogrify("SELECT id FROM deploy_table WHERE ser_num = (%s) AND start_dt <= (%s) AND end_dt >= (%s);",(keyInfo["serial"], minmaxDate[0], minmaxDate[1]))
        cur.execute(query)
        try:
            deployID = cur.fetchall()
            deployID = deployID[0][0]
        except:
            print "Skipping", f, "could not find deploy key"
            skippedFiles.append(f)
            print "-"*40
            pass
        else:
            print "Deploy key found:", deployID
            print "Generating header"    
            header = data[key["header"]]
            print "Removing empty values from header"    
            if header[-1] == "":
                del header[-1]
            print "Casting Data"
            cast = castData(data, key)
            print "Loading", len(cast), "rows"
            existingRows = 0
            loadedRows = 0
            for rows in cast:
                if len(rows)!= 0:        
                    loadValues = loadDict(rows, header)
                    status = checkLoad(deployID, loadValues)
                    if status is False:
                        executeLoad(deployID, loadValues)
                        loadedRows += 1
                    elif status is True:
                        existingRows += 1
            
            print keyInfo["records"], "records in raw file"
            print loadedRows, "records loaded into database"
            print existingRows, "records already in DB, skipped"
            print "Committing Changes"
            con.commit()
            print "Done with", f
            totalRows += loadedRows
            fileCount += 1
            totalRaw += int(keyInfo["records"])
            totalSkipped += existingRows
            print "-"*40
    
            
    #    for i in cast:
    #        for j, x in zip(i, header):
    #            cur.mogrify("INSERT )
    cur.close()
    con.close()
    print "\n"
    print "Script Finished"
    print totalRaw, "rows in raw files"
    print totalRows, "rows loaded into database"
    print totalSkipped, "pre-existing rows skipped"
    print "-"*40
    print "Skipped the following files due to no deploy key"
    for i in skippedFiles:
        print i