# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 13:05:25 2014

@author: Bassett_S
"""
import psycopg2
import datetime

def getTable(connection, tableName):
    cursor = connection.cursor()
    cursor.execute("""SELECT date, time FROM {0}""".format(tableName))
    data = cursor.fetchall()
    data = [datetime.datetime.combine(row[0],row[1]) for row in data[:]]
    data = [item + datetime.timedelta(hours=5) for item in data[:]]
    data = sorted(data[:])
    cursor.close()
    del cursor
    
    return data

def getHRDB(connection, siteCode):
    cursor = connection.cursor()
    cursor.execute("""select date_time FROM falmouth INNER JOIN deploy_info USING (deploy_key)
        WHERE site_code = \'{0}\';""".format(siteCode))
    data = cursor.fetchall()
    data = [item[0].replace(tzinfo=None) for item in data[:]]
    data = sorted(data[:])
    
    cursor.close()
    del cursor
    return data
    
connection_usrv = psycopg2.connect(dsn=None, 
            host= "fgs-usrv",
            database= "wkp_hrdb_v1.0",
            user= "postgres",
            password= "incorrectLitho")

connection_alice = psycopg2.connect(dsn=None, 
            host= "fgs-27951g1",
            database= "kincaid",
            user= "post_root",
            password= "Fgs_rocks_g1")

cursorUsrv = connection_usrv.cursor()
cursorAlice = connection_alice.cursor()

cursorAlice.execute("""SELECT date, time FROM ad_tunnel""")

adAlice = cursorAlice.fetchall()

adAlice = [{"date":row[0], "time":row[1]} for row in adAlice[:]]

adAlice = [datetime.datetime.combine(row["date"],row["time"]) for row in adAlice[:]]
