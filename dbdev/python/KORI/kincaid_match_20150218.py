# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 16:09:12 2015

@author: Bassett_S
"""
import csv
import datetime
import psycopg2
def parseKincaid(filename):
    
    with open(filename, 'r') as f:
        creader = csv.reader(f, delimiter="\t")
        data = [row for row in creader]
    headers = data.pop(0)
    datad = [{head:val for head, val in zip(headers, row) if head != 'FLOW(CFS)' and head != 'FLOW(CM^3/SEC)' and head != 'FLOW(M^3/SEC)'} for row in data]
    return datad

def press(data):
    for row in data[:]:
        combine = " ".join([row["DATE"], row["TIME"]])
        row["AVDIR"] = row["ADIR"]
        del row["ADIR"]
        del row["DATE"]
        del row["TIME"]
        for key in row.keys():
            row[key] = float(row[key])
        row["date_time"] = datetime.datetime.strptime(combine, "%m-%d-%Y %H:%M:%S")
        row["date_time"] = row["date_time"] + datetime.timedelta(hours=5)
        
    return data
    
def create_insert_statement(row, tableName):
    """Creates an insert statement for each row"""
    listFields = sorted(row.keys())
    intoStatement = ", ".join(listFields)
    valueParts = ["%({0})s".format(i) for i in listFields]
    valuesStatement = ", ".join(valueParts)
    insertStatement = """INSERT INTO {0} ({1}) VALUES ({2});""".format(tableName, intoStatement, valuesStatement)
    return insertStatement

def insert_table(data, tableName):
    cursor = connection.cursor()
    for row in data:
        sql = create_insert_statement(row, tableName)
        cursor.execute(sql, row)
    connection.commit()
    cursor.close
    del cursor
            

ad_path = r'C:\GISData\WKP Data\kincaiddb\cumulative_flow_data_AD_200402-201109\cumulative_flow_data.dat'  
ak_path = r'C:\GISData\WKP Data\kincaiddb\cumulative_flow_data_AK_200402-201109\cumulative_flow_data.dat'
connection = psycopg2.connect(database="wkp_kincaid", user="postgres", password=pw, host="fgs-usrv")
        