# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 11:01:32 2014

@author: Bassett_S
"""

import falmouth, datetime, psycopg2

def writeFlags(data, startDeploy, connection_info):
    calPeriod = datetime.timedelta(days=365)

    con = psycopg2.connect(dsn=None, 
        host= connection_info[0],
        database= connection_info[1],
        user= connection_info[2],
        password= connection_info[3])

	#establish cursor, set session time zone
    cur = con.cursor()
    cur.execute("SET SESSION TIME ZONE UTC")
    
    for j in data:
        if j[1] - startDeploy < calPeriod:
            cur.execute("UPDATE falmouth SET calibration = %s WHERE falmouth_id = %s", (True, j[0]))
            con.commit()
        elif j[1] - startDeploy > calPeriod:
            cur.execute("UPDATE falmouth SET calibration = %s WHERE falmouth_id = %s", (False, j[0]))
            con.commit()
    cur.close()
    con.close()


pw = raw_input("Enter Password: ")
dbinfo = ["fgs-usrv","wkp_hrdb","postgres",pw]


deploySQLquery = falmouth.buildSQLquery("*", "deploy_info", "NONE")
deployTable = falmouth.retrieveRows(deploySQLquery, dbinfo)
deployTableInfo = falmouth.retrieveColumnNames(deploySQLquery, dbinfo)

deployStart = {i[1]:i[3].replace(tzinfo=None) for i in deployTable}
deployEnd = {i[1]:i[4].replace(tzinfo=None) for i in deployTable}
deployNumbers = [i[1] for i in deployTable]

for i in deployNumbers:
    falmouthSQLquery = falmouth.buildSQLquery("falmouth_id, date_time", "falmouth", "deploy_key = %s" % i)
    data = falmouth.retrieveRows(falmouthSQLquery, dbinfo)
    data = [[j[0], j[1].replace(tzinfo=None)] for j in data]
    writeFlags(data, deployStart[int(i)], dbinfo)
    

