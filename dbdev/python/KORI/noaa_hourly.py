# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 09:58:50 2014

@author: Bassett_S
"""

import re, datetime, psycopg2

class NOAA_hourly:
    def __init__(self, path, headerPath, connection_info):
        self.connection = psycopg2.connect(dsn=None, 
                host= connection_info[0],
                database= connection_info[1],
                user= connection_info[2],
                password= connection_info[3])
        self.path = path
        self.headerPath = headerPath
        self.header = self.readHeader()
        
    def readHeader(self):
        with open(self.headerPath, 'r') as f:
            header = [line for line in f]
        return header

            