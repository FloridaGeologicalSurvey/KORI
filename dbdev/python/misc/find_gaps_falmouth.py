# -*- coding: utf-8 -*-
"""
Created on Mon Aug 04 14:42:56 2014

@author: Bassett_S
"""

import falmouth, datetime

pw = raw_input("Enter Password: ")
dbinfo = ["FGS-27951g1","wkp_hrdb","post_root",pw]

gaps = []
for i in range(1, 16):
    sqlquery = "SELECT date_time FROM falmouth WHERE deploy_key = " + str(i)
    sensorQuery = "SELECT site_id FROM deploy_info WHERE deploy_key = " + str(i)
    sensor = falmouth.retrieveRows(sensorQuery, dbinfo)[0][0]
    data = falmouth.retrieveRows(sqlquery, dbinfo)
    data = [x[0].replace(tzinfo=None) for x in data]
    data = sorted(data)
    offset = datetime.timedelta(hours=5)
    data = [x-offset for x in data]
    gapSize = datetime.timedelta(hours=2)
    for v in range(1, len(data)-1):
        newLine = []
        if data[v + 1] - data[v] > gapSize:
            gaps.append([sensor, data[v], data[v+1]])

with open(r'C:\PythonWorkspace\gapsummary.txt', 'w') as f:
    for i in gaps:
        for j in i:
            if type(j) != datetime.datetime:
                f.write(str(j))
            else:
                f.write(j.strftime('%Y-%m-%d %H:%M:%S'))
            f.write("\t")
        f.write("\n")


        
    
    
    