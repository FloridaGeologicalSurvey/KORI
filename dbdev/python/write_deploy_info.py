# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:47:13 2014

@author: Bassett_S
"""

import falmouth, psycopg2, psycopg2.extras, os
from operator import itemgetter

pw = raw_input("Enter DB password: ")
dataWorkspace = r"C:\GISData\WKP Data\Flat Data\Original Sensor Data\Falmouth_Sorted_Sanitized_03-21-2014"
connection_info = ["FGS-27951g1","wkp_hrdb_dev","post_root", pw]


print "listing directory"
files = os.listdir(dataWorkspace)
filePaths = [os.path.join(dataWorkspace, f) for f in files]
#pathsTypeA = [f for f in filePaths if falmouth.parse(f, "data header") == typeA ]
#pathsTypeB = [f for f in filePaths if falmouth.parse(f, "data header") == typeB ]
#pathsTypeU = [f for f in filePaths if falmouth.parse(f, "data header") != typeA and falmouth.parse(f, "data header") != typeB]

print "Building location names"
locNames = [i.split("_")[0] for i in files]

print "Getting MinMax timestamps"
minMaxTable = []
for i, j in zip(filePaths, locNames):
    header = falmouth.parse(i, "header")
    data = falmouth.parse(i, "data")
    timestamps = falmouth.parseTimestamps(data)
    fileTable = [(j, header[0]), timestamps[0], timestamps[1]]
    minMaxTable.append(fileTable)

masterID = [i[0] for i in minMaxTable]
masterID = list(set(masterID))

maxDict = {i:None for i in masterID}
minDict = {i:None for i in masterID}

for i in minMaxTable:
    if minDict[i[0]] == None:
        minDict[i[0]] = i[1]
    elif i[1] < minDict[i[0]]:
        minDict[i[0]] = i[1]

for i in minMaxTable:
    if maxDict[i[0]] == None:
        maxDict[i[0]] = i[2]
    elif i[2] > maxDict[i[0]]:
        maxDict[i[0]] = i[2]

masterAll = [[i, minDict[i], maxDict[i]] for i in sorted(masterID, key=itemgetter(0))]

con = psycopg2.connect(
    dsn=None, 
    host= connection_info[0], 
    database= connection_info[1], 
    user= connection_info[2], 
    password= connection_info[3])

cur = con.cursor() 
dev_type='Falmouth 2D-ACM'
net_type = 'Deep'

for i in masterAll:   
    cur.execute("""INSERT INTO deploy_info (site_id, serial_number, start_dt, end_dt, device_type, network)
                            values(%(site_id)s, %(serial_number)s, %(start_dt)s, %(end_dt)s, %(device_type)s, %(network)s);""",
                            {'site_id':i[0][0], 'serial_number':i[0][1], 'start_dt':i[1], 'end_dt':i[2], 'device_type':dev_type, 'network':net_type})
    con.commit()
cur.close()
con.close()
