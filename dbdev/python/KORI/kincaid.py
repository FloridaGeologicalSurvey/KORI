# -*- coding: utf-8 -*-
"""
Created on Mon Feb 02 13:20:24 2015

@author: Bassett_S
"""

import psycopg2
import datetime
import decimal
import os
idPairs = [('ad_tunnel', 'AD (Deep)'),
        ('ak_tunnel', 'AK (Deep)'),
        ('k_tunnel', 'K (Deep)'),
        ('d_tunnel', 'D (Deep)'),
        ('revell', 'Revell Sink (Deep)'),
        ('b_tunnel', 'B (Deep)'),
        ('c_tunnel', 'C (Deep)'),
        ('sc1', 'Spring Creek 1 (Deep)'),
        ('sc10', 'Spring Creek 10 (Deep)')]
        
class Kincaid:
    def __init__(self, password, tsRange, idPair):
        self.connection = psycopg2.connect(
            dsn=None, 
            host= "fgs-usrv",
            database= "wkp_kincaid",
            user= "postgres",
            password= password)
        self.connection2 = psycopg2.connect(
            dsn=None, 
            host= "fgs-usrv",
            database= "wkp_hrdb_dev",
            user= "postgres",
            password= password)
        self.tsRange = tsRange
        self.queryColumns = ['date', 'time', 'aspd', 'adir', 'cond', 'temp', 'pressure']
        self.headers = ['date', 'time', 'aspd', 'avdir', 'cond', 'temp', 'pres']
        self.table, self.site_id = idPair
        self.sql = self.set_sql()
        self.data = self.cast_data(self.get_data())
        self.utcRange = self.set_utcRange()
        self.deploy_table = self.get_deploy_table()
        
        
    def set_sql(self):
        if self.tsRange == (None, None):
            sql = "SELECT {0} FROM {1}".format(", ".join(self.headers), self.table)
        else:
            sql = "SELECT {0} FROM {1} WHERE date >= \'{2}\' AND date < \'{3}\'\
            ORDER BY (date, time);".format(
                                ", ".join(self.queryColumns),       #{0}
                                self.table,                         #{1}
                                self.tsRange[0].split(" ")[0],                    #{2}
                                self.tsRange[1].split(" ")[0])                   #{3}
        return sql
    
    def get_data(self):
        cursor = self.connection.cursor()
        cursor.execute(self.sql)
        data = cursor.fetchall()
        dictData = [{key:item for key,item in zip(self.headers, row)} for row in data]
        cursor.close()
        del cursor
        return dictData
    
    def cast_data(self, data):
        for row in data[:]:
            date = row["date"]
            time = row["time"]
            tempTimestamp = datetime.datetime.combine(date, time)
            row["est"] = tempTimestamp
            row["date_time"] = tempTimestamp + datetime.timedelta(hours=5)        
        return data
    
    def set_utcRange(self):
        dtList = [row["date_time"] for row in self.data]
        return (min(dtList), max(dtList))
        
    def create_insert_statement(self, row):
        """Creates an insert statement for each row"""
        listFields = sorted(row.keys())
        intoStatement = ", ".join(listFields)
        valueParts = ["%({0})s".format(i) for i in listFields]
        valuesStatement = ", ".join(valueParts)
        insertStatement = """INSERT INTO {0} ({1}) VALUES ({2});""".format('falmouth', intoStatement, valuesStatement)
        return insertStatement
        
    def prepare_table_for_insert(self):
        for row in self.data[:]:
            del row["est"], row["date"], row["time"]
            row["deploy_key"] = self.return_deploy_key(row)
            row["date_time"] = datetime.datetime.strftime(row["date_time"], '%Y-%m-%d %H:%M:%S')
            row["source"] = "Hazlett-Kincaid"
        
    
        
    def get_deploy_table(self):
        cursor = self.connection2.cursor()
        sql = "SELECT s.site_name, d.deploy_key, d.start_dt, d.end_dt FROM deploy_info d INNER JOIN sites s USING (site_id);"
        cursor.execute(sql)
        deploy_key = cursor.fetchall()
        keys = ["site_name", "deploy_key", "start", "end"]        
        dt = [{key:value for key, value in zip(keys, row)} for row in deploy_key]
        for row in dt[:]:
            for key in row.keys():
                if type(row[key]) == datetime.datetime:
                    row[key] = row[key].replace(tzinfo=None)
        
        cursor.close()
        del cursor
        return dt
    
    def return_deploy_key(self, row):
        for i in self.deploy_table:
            if i["site_name"] == self.site_id and row["date_time"] >= i["start"] and row["date_time"] <= i["end"]:
                deploy_key = i["deploy_key"]
        return deploy_key
        
class Raw:
    def __init__(self, password, tsRange, site):
        self.connection = psycopg2.connect(
            dsn=None, 
            host= "fgs-usrv",
            database= "wkp_hrdb_dev",
            user= "postgres",
            password= password)
        
        self.tsRange = tsRange
        self.site = site
        self.queryColumns = ['s.site_name', 'f.deploy_key', 'f.date_time', 'f.aspd', 
                        'f.avdir', 'f.cond', 'f.temp', 'f.pres']
        self.headers = ['site_name', 'deploy_key', 'date_time', 'aspd', 'avdir',
                        'cond', 'temp', 'pres']
        self.sql = self.set_sql()
        self.data = self.cast_data(self.get_data())
        self.utcRange = self.set_utcRange()
    
    def set_sql(self):
        sql = """SELECT {0} FROM falmouth f INNER JOIN deploy_info d
            USING (deploy_key) INNER JOIN sites s USING (site_id)
            WHERE f.date_time >=\'{1}\' AND f.date_time < \'{2}\' AND 
            s.site_name = \'{3}\' ORDER BY date_time;""".format(", ".join(self.queryColumns),
                                             self.tsRange[0],
                                             self.tsRange[1],
                                             self.site)
        return sql
    
    def get_data(self):
        cursor = self.connection.cursor()
        cursor.execute(self.sql)
        data = cursor.fetchall()
        cursor.close()
        del cursor
        dictData = [{key:item for key,item in zip(self.headers, row)} for row in data]
        return dictData
    
    def cast_data(self, data):
        for row in data[:]:
            for key in row.keys():
                if type(row[key]) == decimal.Decimal:
                    row[key] = float(row[key])
                elif type(row[key]) == datetime.datetime:
                    row[key] = row[key].replace(tzinfo=None)
        return data        

    def set_utcRange(self):
        dtList = [row["date_time"] for row in self.data]
        return (min(dtList), max(dtList))

        
class Comparator:
    def __init__(self, table1, table2, keyValue):
        """Compares two tables. For this class, bopth table1 and table2 should
        be a list of dictionaries, 
        e.g.[{"A": a1, "B":b1, "C":c1}, {"A":a2, "B":b2, "C":c2} ...]
        
        The key value is a unique identifier"""
        
        self.table1 = table1
        self.table2 = table2
        self.keyValue = keyValue
        self.flags = {'abscount': None,
                      't1 not t2': None,
                      't2 not t1': None}
        self.comparisonKeys = self.set_comparison_keys()
                      
                      
    def set_key_diff(self):
        dt1 = set([row[self.keyValue] for row in self.table1])
        dt2 = set([row[self.keyValue] for row in self.table2])
        #diff = (sorted(list(dt1 - dt2)), sorted(list(dt2 - dt1)))
        self.flags['t1 not t2'] = len(list(dt1 - dt2))
        self.flags['t2 not t1'] = len(list(dt2 - dt1))
        #return diff
    
    def return_key_overlap(self):
        """Returns the overlap between key value columns"""
        dt1 = set([row[self.keyValue] for row in self.table1])
        dt2 = set([row[self.keyValue] for row in self.table2])
        overlap = sorted(list((dt1 & dt2)))
        return overlap
    
    def return_t2_not_t1(self):
        dt1 = set([row[self.keyValue] for row in self.table1])
        dt2 = set([row[self.keyValue] for row in self.table2])
        return sorted(list(dt2 - dt1))
        
    def return_abs_diff(self):
        "return the absolute difference in row counts"
        return abs(len(self.table2) - len(self.table1))
    
    def set_comparison_keys(self):
        """Sets the comparison keys using the keys from the first rows in two
        lists of dictionaries, minus the value of self.keyValue"""
        
        keys1 = self.table1[0].keys()
        keys2 = self.table2[0].keys()
        allKeys = sorted([i for i in keys1 if i in keys2 and i != self.keyValue])
        return allKeys
        
    def transmute_table(self, table):
        """
        Transmute a list of dictionaries into a dictionary of dictionaries
        using self.keyValue. This is useful, as dictionary lookups are much,
        much faster than interating through a pair of lists to find matches
        
        E.g. given the list:
        [{"A": a1, "B":b1, "C":c1}, {"A":a2, "B":b2, "C":c2} ...]
        and the key value "B", transmute_table produces:
        {"b1":{"A":a1, "C":c1}, "b2":{"A":a2, "C":c2}}
        etcetera. 
        
        Required values are self.keyValue and a table
        """
        
        keys = self.comparisonKeys
        
        #compare the list of values to a list of unique values to make sure the
        #keyValue is unique
        keyValueList = [i[self.keyValue] for i in table]
        lenRawList = len(keyValueList)
        lenSetList = len(list(set(keyValueList)))
        
        
        if lenRawList == lenSetList:
            print "Success"
            transmute = {i[self.keyValue]:{key:i[key] for key in keys if key != self.keyValue} for i in table}
            return transmute
        else:
            print "This does not appear to be a unique identifier!"
            exit
    
    def fast_compare(self, filename):
        """Compares table1 and table2 using transmuted tables.
        Output is in TRUE and FALSE form for convenience sake"""
        ttable1 = self.transmute_table(self.table1)
        ttable2 = self.transmute_table(self.table2)
        overlap = self.return_key_overlap()
        with open(filename, 'w') as f:
            f.write("{0}\t".format(self.keyValue))            
            f.write("\t".join(sorted(self.comparisonKeys)))
            f.write("\n")
            for timestamp in overlap:
                row1 = ttable1[timestamp]
                row2 = ttable2[timestamp]
                f.write("{0}\t".format(timestamp))
                for key in sorted(self.comparisonKeys):
                    if row1[key] == row2[key]:
                        f.write("TRUE\t")
                    else:
                        f.write("FALSE\t")
                f.write("\n")
        
    def detailed_compare(self, filename):
        """Compares table1 and table2 using transmuted tables.
        Output is in paired values"""
        ttable1 = self.transmute_table(self.table1)
        ttable2 = self.transmute_table(self.table2)
        overlap = self.return_key_overlap()
        with open(filename, 'w') as f:
            f.write("{0}\t".format(self.keyValue))            
            f.write("\t".join(sorted(self.comparisonKeys)))
            f.write("\n")
            for timestamp in overlap:
                row1 = ttable1[timestamp]
                row2 = ttable2[timestamp]
                f.write("{0}\t".format(timestamp))
                for key in sorted(self.comparisonKeys):
                    f.write("( {0},{1} )\t".format(row1[key],row2[key]))
                f.write("\n")
                
"""  
#main comparison script, compares all Falmouth sites to the kincaid values            
if __name__ == "__main__":
    idPairs = [('ad_tunnel', 'AD (Deep)'),
            ('ak_tunnel', 'AK (Deep)'),
            ('k_tunnel', 'K (Deep)'),
            ('d_tunnel', 'D (Deep)'),
            ('revell', 'Revell Sink (Deep)'),
            ('b_tunnel', 'B (Deep)'),
            ('c_tunnel', 'C (Deep)'),
            ('sc1', 'Spring Creek 1 (Deep)'),
            ('sc10', 'Spring Creek 10 (Deep)')]
    
    tsRangeEST = ('2003-01-01 00:00:00','2015-01-01 00:00:00' )
    tsRangeUTC = ('2003-01-01 05:00:00','2015-01-01 05:00:00' )
    overlapRows = 0
    
    for pair in idPairs:
        kincaid = Kincaid(pw, tsRangeEST, pair[0])
        raw = Raw(pw, tsRangeUTC, pair[1])
        comparator = Comparator(raw.data, kincaid.data, "date_time")
        #fnFast = ["fast", pair[0], datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')]
        #fnDetailed = ["detailed", pair[0], datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')]
        #fastPath = os.path.join(r'C:\PythonWorkspace', "_".join(fnFast))
        #detailPath = os.path.join(r'C:\PythonWorkspace', "_".join(fnDetailed))       
        #comparator.fast_compare(fastPath)
        #comparator.detailed_compare(detailPath)
        overlap = len(comparator.return_key_overlap())
        comparator.set_key_diff()
        print pair[0],comparator.flags['t2 not t1']
        overlapRows = overlapRows + overlap
        del kincaid
        del raw
        del comparator
    
    print "Total Overlapped Rows = {0}".format(overlapRows)
    
"""       
    
        
        


        
    