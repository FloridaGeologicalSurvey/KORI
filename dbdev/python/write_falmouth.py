# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 16:34:29 2014

@author: Bassett_S
"""

import os, falmouth

#workspace that holds the raw files
#dataWorkspace = r"C:\GISData\WKP Data\Flat Data\Original Sensor Data\Falmouth_Sorted_Sanitized_03-21-2014"
dataWorkspace = r'C:\GISData\WKP Data\Flat Data\Original Sensor Data\Falmouth_import_Run_20140428'


pw = raw_input("Enter DB password: ")


alice = ["FGS-27951g1","wkp_hrdb","post_root",pw]

######################    Constants  ###########################################
#this is the ordered headers for the two types of Falmouth files

typeB = ['AVN', 'AVE', 'ASPD', 'AVDIR', 'ATLT', 'TIME', 'DATE', 
         'COND', 'TEMP', 'PRES', 'SALT', 'SV', 'HDNG', 'BATT', 
         'VX', 'VY', 'TX', 'TY', 'HX', 'HY', 'HZ', 'VN', 'VE', 
         'STEMP', 'SV', 'VAB', 'VCD', 'VEF', 'VGH']
    
typeA = ['AVN', 'AVE', 'ASPD', 'AVDIR', 'ATLT', 'TIME', 'DATE', 
        'COND', 'TEMP', 'PRES', 'HDNG', 'BATT', 'VX', 'VY', 'TX', 
        'TY', 'HX', 'HY', 'HZ', 'VN', 'VE', 'STEMP', 'SV', 'VAB', 
        'VCD', 'VEF', 'VGH']
##############################################################################

#parse raw files and build list of Type A, Type B, and Type U (unknown)
print "Building Type Tables"     
files = os.listdir(dataWorkspace)
filePaths = [os.path.join(dataWorkspace, f) for f in files]
pathsTypeA = [f for f in filePaths if falmouth.parse(f, "data header") == typeA ]
pathsTypeB = [f for f in filePaths if falmouth.parse(f, "data header") == typeB ]
pathsTypeU = [f for f in filePaths if falmouth.parse(f, "data header") != typeA and falmouth.parse(f, "data header") != typeB]

#query the DB for the deploy table
print "Fetching Deploy Table"
deploySQLquery = falmouth.buildSQLquery("*", "deploy_info", "NONE")
deployTableInfo = falmouth.retrieveColumnNames(deploySQLquery, alice)
deployTable = falmouth.retrieveRows(deploySQLquery, alice)
print "Success"
print "\n"

#Build a report list, which identifies each raw file's appropriate deploy key
print "-"*60
reportListA = []
print "Generating Report List For Type A"
for f in pathsTypeA:
    sensorData = falmouth.parse(f, "data")
    sensorSerial = falmouth.parse(f, "header")[0] 
    sensorStartEnd = falmouth.parseTimestamps(sensorData)
    for i in deployTable:
        if i[2] == sensorSerial and i[3] <= sensorStartEnd[0] and i[4] >= sensorStartEnd[1]:
            reportListA.append([f, i[1]])
print "Success"
print "-"*60
print "\n"

print "-"*60
reportListB = []
print "Generating Report List For Type B"
for f in pathsTypeB:
    sensorData = falmouth.parse(f, "data")
    sensorSerial = falmouth.parse(f, "header")[0] 
    sensorStartEnd = falmouth.parseTimestamps(sensorData)
    for i in deployTable:
        if i[2] == sensorSerial and i[3] <= sensorStartEnd[0] and i[4] >= sensorStartEnd[1]:
            reportListB.append([f, i[1]])
print "Success"
print "-"*60
print "\n"


#write to database
print "*"*60
print "\n"
print "Writing Falmouth Data for Type A"
for i in reportListA:
    falmouth.writeFalmouthDataTypeA(str(i[0]), i[1], alice)
print "With Great Success Comrade!"

print "Writing Falmouth Data for Type B"
for i in reportListB:
    falmouth.writeFalmouthDataTypeB(str(i[0]), i[1], alice)
print "With Great Success Comrade!"
print "\n"
print "*"*60

for i in pathsTypeU:
    print "Did not write", os.path.split(i)[1], "due to unknown row header type"





