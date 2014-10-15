# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 12:12:06 2014

@author: Bassett_S
"""
import psycopg2, csv

class Ttable:
    def __init__(self, path, header, types, connection_info, tableName, invalid = [], lineSkips=0):
        self.path = path
        self.header = header
        self.types = types
        self.connection = psycopg2.connect(dsn=None, 
            host= connection_info[0],
            database= connection_info[1],
            user= connection_info[2],
            password= connection_info[3])
        self.status = {
            'read':None,
            'cast':None,
            'load':None}
        self.lineSkips = lineSkips
        self.invalid = invalid
        self.rawData = self.read()
        self.castData = self.cast()
        self.tableName = tableName
        if self.status['read'] and self.status['cast']:
            self.load()
    
    def read(self):
        try:
            with open(self.path, 'r') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=self.header)
                data = [row for row in reader]
            rawData = data[self.lineSkips:]
            self.status['read']=True
            return rawData
        except:
            self.status['read']=False
            return []

    def cast(self):
        if self.status['read']:
            try:
                castData = []
                for row in self.rawData:
                    newRowDict = {}
                    for key in row.keys():
                        if row[key] in self.invalid:
                            newRowDict[key] = None
                        else:
                            if self.types[key] is int:
                                newRowDict[key] = int(row[key])
                            elif self.types[key] is float:
                                newRowDict[key] = float(row[key])
                            elif self.types[key] is str:
                                newRowDict[key] = str(row[key])
                    castData.append(newRowDict)
                self.status['cast']=True
                return castData
            except:
                self.status['cast'] = False
                return []
            
    def createInsertStatement(self, row):
        listFields = sorted(row.keys())
        intoStatement = ", ".join(listFields)
        valueParts = ["%({0})s".format(i) for i in listFields]
        valuesStatement = ", ".join(valueParts)
        insertStatement = """INSERT INTO {0} ({1}) VALUES ({2});""".format(self.tableName, intoStatement, valuesStatement)
        return insertStatement
    
    def load(self):
        try:
            cursor = self.connection.cursor()
            for row in self.castData:
                sql = self.createInsertStatement(row)
                cursor.execute(sql, row)
            self.connection.commit()
            cursor.close()
            del cursor
            self.status['load'] = True
        except:
            self.status['load'] = False
            

                
                
        

            
        
        