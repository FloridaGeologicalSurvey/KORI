# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 09:29:55 2014

@author: Bassett_S
"""
import csv, datetime, psycopg2

class NoaaWle:
    stationID = 8728690
    def __init__(self, path, connection_info):
        self.connection = psycopg2.connect(dsn=None, 
                host= connection_info[0],
                database= connection_info[1],
                user= connection_info[2],
                password= connection_info[3])
        self.path = path
        self.header = []
        self.data=[]
        self.ddata = {}

    def testparse(self):
#        with open(self.path, "r") as csvfile:
#            creader = csv.reader(csvfile)
#            self.header = creader.next()
#            self.data = [row for row in creader if row != self.header]
        with open(self.path, "r") as csvfile:
            dreader = csv.DictReader(csvfile)
            self.ddata = [row for row in dreader]
            self.header = [i for i in self.ddata[0].keys()]  

    def parse(self):
#        with open(self.path, "r") as csvfile:
#            creader = csv.reader(csvfile)
#            self.header = creader.next()
#            self.data = [row for row in creader if row != self.header]
        with open(self.path, "r") as csvfile:
            dreader = csv.DictReader(csvfile)
            self.ddata = [row for row in dreader]
            self.header = [i for i in self.ddata[0].keys()]
        for i in self.ddata:
            for key in i.keys():
                if len(i[key]) == 0:
                    i[key] = None
                else:
                    if key in [' F', ' O', 'L', ' R']:
                        i[key] = int(i[key])
                    elif key in [' Water Level', ' Sigma']:
                        i[key] = float(i[key])
                    elif key == 'Date Time':
                        i[key] = i[key] + ":00 UTC"
            i["station_id"] = NoaaWle.stationID
            
    def analyzeLen(self):
        dvals = {}
        dlens = {}
        dsets = {}
        for i in self.header:
            dvals[i] = []
            dlens[i] = []
        for i in self.ddata:
            for j in i.keys():
                dlens[j].append(len(i[j]))
        for key in dlens.keys():
            dsets[key] = set(dlens[key])
        return dsets
        
    def load(self):
        field2db = {
            ' F': 'F',
            ' Water Level': 'wle' ,
            ' O': 'O',
            ' L': 'L',
            ' R': 'R',
            'Date Time': 'date_time' ,
            ' Quality ': 'quality',
            ' Sigma': 'sigma'
            }
        db2field = {
            'R' : ' R',
            'F' : ' F',
            'date_time' : 'Date Time',
            'quality' : ' Quality ',
            'wle' : ' Water Level',
            'O' : ' O',
            'L' : ' L',
            'sigma' : ' Sigma'}
        curr = self.connection.cursor()
        for i in self.ddata:
            curr.execute("""INSERT INTO noaa_tidal (station_id, date_time, wle, sigma, O, F, R, L, quality)
                            values (%(station_id)s, %(Date Time)s, %( Water Level)s, %( Sigma)s, %( O)s, %( F)s, %( R)s, %( L)s, %( Quality )s);""",
                            i)
        self.connection.commit()
        curr.close()
        del curr
    def analyzeColumns(self):
        columns = {key:[] for key in self.header}
        
        #hack
        columns["station_id"] = []
        
        #flatten rows
        for row in self.ddata:
            for key in row:
                columns[key].append(row[key])        
        


        
            
