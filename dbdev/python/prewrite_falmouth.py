# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 13:34:09 2014

@author: Bassett_S
"""

import datetime, os, shutil, falmouth, psycopg2
workspace = r'C:\GISData\WKP Data\Flat Data\Original Sensor Data\Canonical_Falmouth\good'
#dupeWorkspace = r'C:\GISData\WKP Data\Flat Data\Original Sensor Data\Canonical_Falmouth\dupes'


connection_info = ['fgs-usrv', 'wkp_hrdb','wkp_user','Fgs_wkp']
con = psycopg2.connect(dsn=None, 
    host= connection_info[0],
    database= connection_info[1],
    user= connection_info[2],
    password= connection_info[3])

cur = con.cursor()
cur.execute('SET SESSION TIME ZONE UTC')

files = os.listdir(workspace)
count = 0
for i in files:    
    path = os.path.join(workspace, i)
    dates = falmouth.parseDates(falmouth.parse(path, 'data'))
    timestamps = falmouth.parseTimestamps(falmouth.parse(path, 'data'))
    timestampsUTC = [falmouth.est2utc(j) for j in timestamps]
    serial = falmouth.parse(path, 'header')[0]
    cur.execute('SELECT deploy_key FROM deploy_info WHERE serial_number = %s AND start_dt <= %s AND end_dt >= %s', (serial, timestampsUTC[0], timestampsUTC[1]) )
    deployKey = cur.fetchall()
    deployKey = deployKey[0][0]
    cur.execute('SELECT * FROM falmouth WHERE deploy_key = %s AND date_time >= %s AND date_time <= %s', (deployKey, timestampsUTC[0], timestampsUTC[1]) )
    dbdata = cur.fetchall()
    fileData = falmouth.parse(path, 'data')
    print i, len(fileData), len(dbdata)
#    if len(dbdata) != 0:
#        destination = os.path.join(dupeWorkspace, i)
#        shutil.move(path, destination)

        

print count


    