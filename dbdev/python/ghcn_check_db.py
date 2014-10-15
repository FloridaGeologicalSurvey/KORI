# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 14:59:38 2014

@author: Bassett_S
"""
#import ghcn
import psycopg2, psycopg2.extras, datetime, decimal

def createSelectStatement(row):
    listFields = sorted(row.keys())
    fieldStatement = ", ".join(listFields)
    insertStatement = """SELECT {0} FROM noaa_ghcn WHERE date_time = TIMESTAMP \'{1}\' and station = \'{2}\';""".format(fieldStatement, row['date_time'], row['station'])
    return insertStatement
connection_info = ["fgs-usrv","wkp_hrdb_dev","postgres",pw]    
conn = psycopg2.connect(dsn=None, 
            host= connection_info[0],
            database= connection_info[1],
            user= connection_info[2],
            password= connection_info[3])
ghcnPath = r'C:\GISData\WKP Data\Flat Data\CLEAN CDO\ghcn\five_counties.csv'
ghcnHeader = r'C:\GISData\WKP Data\Flat Data\CLEAN CDO\ghcn\five_counties_header.txt'

fcounties = Ghcn(ghcnPath, ghcnHeader, usrv)
fcounties.parse()
data = fcounties.press()

curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
rowEval = []
for v,row in enumerate(data):
    thisRow = []
    sql = createSelectStatement(row)
    curr.execute(sql)
    dbrow = curr.fetchall()[0]
    translation = {key.lower():key for key in row.keys()}
    for key in dbrow.keys():
        item = dbrow[key]
        if type(item) is datetime.datetime:
            item = item.replace(tzinfo=None)
            item = datetime.datetime.strftime(item,'%Y-%m-%d %H:%M:%S UTC')
        elif type(item) is decimal:
            float(item)
            
        if row[translation[key]] == item:
            thisRow.append(True)
        else:
            thisRow.append(False)
    rowEval.append(thisRow)
    print v,"of",len(data)
curr.close()
conn.close()
del curr, conn

    
    
    
    
