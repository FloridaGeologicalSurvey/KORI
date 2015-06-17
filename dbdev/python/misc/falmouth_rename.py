# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\Bassett_S\.spyder2\.temp.py
"""
import datetime, os, shutil, falmouth, psycopg2
mode = 'check'
toplevel = r'C:\GISData\WKP Data\Flat Data\Original Sensor Data\Canonical_Falmouth\no_deploy_key'
subdir = os.listdir(toplevel)

for sub in range(1):
    workspace = r'C:\GISData\WKP Data\Flat Data\Original Sensor Data\Canonical_Falmouth\good'
    outputWorkspace = r'C:\GISData\WKP Data\Flat Data\Original Sensor Data\Canonical_Falmouth\good'
    noDeployWorkspace = r'C:\GISData\WKP Data\Flat Data\Original Sensor Data\Canonical_Falmouth\no_deploy_key'
    connection_info = ['fgs-usrv', 'wkp_hrdb','wkp_user','Fgs_wkp']

    
    files = os.listdir(workspace)
    
    con = psycopg2.connect(dsn=None, 
        host= connection_info[0],
        database= connection_info[1],
        user= connection_info[2],
        password= connection_info[3])
    
    cur = con.cursor()
    cur.execute('SET SESSION TIME ZONE UTC')
    
    if mode == 'check':       
        for i in files:
            try:                
                path = os.path.join(workspace, i)
                dates = falmouth.parseDates(falmouth.parse(path, 'data'))
                timestamps = falmouth.parseTimestamps(falmouth.parse(path, 'data'))
                timestampsUTC = [falmouth.est2utc(j) for j in timestamps]
                serial = falmouth.parse(path, 'header')[0]
                cur.execute('SELECT site_id FROM deploy_info WHERE serial_number = %s AND start_dt <= %s AND end_dt >= %s', (serial, timestampsUTC[0], timestampsUTC[1]) )
                siteID = cur.fetchall()
                print i, siteID, serial
            except:
                print "Failed on:"
                print path
    elif mode == 'write':
        for i in files:
            path = os.path.join(workspace, i)
            split = i.split("_")
            dates = falmouth.parseDates(falmouth.parse(path, 'data'))
            timestamps = falmouth.parseTimestamps(falmouth.parse(path, 'data'))
            timestampsUTC = [falmouth.est2utc(j) for j in timestamps]
            serial = falmouth.parse(path, 'header')[0]
            cur.execute('SELECT site_id FROM deploy_info WHERE serial_number = %s AND start_dt <= %s AND end_dt >= %s', (serial, timestampsUTC[0], timestampsUTC[1]) )
            siteID = cur.fetchall()
            if len(siteID) == 1 and len(siteID[0]) == 1:
                siteID = siteID[0][0]
                startDate = dates[0].strftime('%Y%m%d')
                endDate = dates[1].strftime('%Y%m%d')
                newName = "_".join([siteID,"Falmouth",startDate,endDate])
                outPath = os.path.join(outputWorkspace,newName)
                if not os.path.exists(outPath):
                    shutil.copyfile(path, outPath)
                else:
                    print "Did not copy",i,"path already exists"
            else:
                print i,"cannot find site ID", siteID
                outPath = os.path.join(noDeployWorkspace, i)
                shutil.copyfile(path, outPath)
                
        
cur.close()
con.close()
    