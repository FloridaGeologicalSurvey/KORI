# -*- coding: utf-8 -*-
"""
Created on Wed Oct 08 11:24:23 2014

@author: Bassett_S
"""

def createInsertStatement(tableName, row):
    listFields = sorted(row.keys())
    intoStatement = ", ".join(listFields)
    valueParts = ["%({0})s".format(i) for i in listFields]
    valuesStatement = ", ".join(valueParts)
    insertStatement = """INSERT INTO {0} ({1}) VALUES ({2});""".format(tableName, intoStatement, valuesStatement)
    return insertStatement
    
    
    
    
    