# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 17:02:16 2014

@author: Bassett_S
"""
import csv, psycopg2
pw = raw_input("Enter Password: ")
connection_info = ["FGS-27951g1", "wkp_hrdb", "post_root", pw]

    #establish connection and cursor    
con = psycopg2.connect(dsn=None, 
    host= connection_info[0],
    database= connection_info[1],
    user= connection_info[2],
    password= connection_info[3])

cur = con.cursor() 

importFile = r"C:\GISData\WKP Data\Flat Data\USGS Station Data\GW_Crawfordville_2007-10-01_2014-04-11.txt"
with open(importFile, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter = "\t", )
    data = []
    for row in reader:
        if row[0].startswith("#"): pass
        else: data.append(row)

newData = []
for i in data[2:]:
    site_id = i[1]
    date_time = i[2] + " " + i[3]
    gw_elev = i[4]
    flag = i[5]
    newData.append([site_id, date_time, gw_elev, flag])

for i in newData:
    cur.execute("""INSERT INTO usgs_groundwater (site_id, date_time, gw_elev, flag) values(%(site_id)s, %(date_time)s, %(gw_elev)s, %(flag)s);""", 
            {'site_id':i[0], 'date_time':i[1], 'gw_elev':i[2], 'flag':i[3]})
    con.commit()
cur.close()
con.close()    
