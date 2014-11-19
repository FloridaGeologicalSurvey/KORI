# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 10:01:43 2014

@author: Bassett_S
"""
import csv
import datetime

class Ttable:
    def __init__(self, 
                     path, 
                     config_path, 
                     connectionInfo=None, 
                     dbTableName=None, 
                     invalid = [], 
                     timestampFormat = '%Y-%m-%d %H:%M:%S',
                     lineSkips=0):
        self.path, self.header, self.types = self.read_config_file(config_path)
        self.types = self.create_type_dictionary(self.header, self.types)
        self.connectionInfo = connectionInfo
        self.dbTableName = dbTableName
        self.invalid = invalid
        self.lineSkips = lineSkips
        self.timestampFormat = timestampFormat
        self.status = {
            'read':None,
            'cast':None,
            'load':None}
    def read_config_file(self, config_path):
        with open(config_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = [row for row in reader]
            return (data[0], data[1], data[2])
            
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
    
    def create_type_dictionary(self, head, typedict):
        tdict = {i:j for i,j in zip(head, typedict)}        
        castDict = {}        
        for key in tdict.keys():
            if tdict[key]=="float":
                castDict[key]=float
            elif tdict[key]=="str":
                castDict[key]=str
            elif tdict[key]=="datetime":
                castDict[key]=datetime.datetime
            elif tdict[key]=="int":
                castDict[key]=int
        return castDict
            
                
            
    
        
        