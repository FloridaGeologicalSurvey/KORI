# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:20:18 2014

@author: fgsuser
"""

import os
import tarfile
import datetime
import sys
import psycopg2
import re
import shutil
import logging


    
def build_system_call(inputDir, outputDir):
    xml = '/home/fgsuser/Documents/wct-3.7.4/wctBatchConfig.xml'
    exe = '/home/fgsuser/Documents/wct-3.7.4/wct-export'
    systemCall = "{0} {1} {2} {3} {4} >/media/data/nexrad/wctlog.log".format(exe, inputDir, outputDir, "wkt", xml)
    return systemCall

class TarDirectory:
    def __init__(self, path, workspace, varList = [None]):
        """Class TarDirectory builds filenames and paths for a directory of nexrad
        tar files."""
        self.path = path
        self.files = os.listdir(path)
        self.workspace = workspace
        self.tarpaths = [os.path.join(self.path, item) for item in self.files]
        self.var = varList
    
    def write_output_folders(self):
        """Create a folder for each variable in the workspace"""
        for arg in self.var:
            newBinaryOut = os.path.join(self.workspace, arg)
            if not os.path.exists(newBinaryOut):
                os.mkdir(newBinaryOut)
            newWKTout = os.path.join(self.workspace, "{0}_wkt".format(arg))
            if not os.path.exists(newWKTout):
                os.mkdir(newWKTout)       


class NexradTar:
    def __init__(self, path, workspace, dataset = [None]):
        """Class NexradTar takes a tarred nexrad files and extrats the datasets of
        interest"""
        self.path = path
        self.workspace = workspace
        self.datasets = dataset
        self.timestamp = self.parse_timestamp()
        self.tf = tarfile.TarFile(path)
        
        
    def parse_timestamp(self):
        fname = os.path.split(self.path)[1]
        tstxt = fname.split("_")[4][0:8]
        tsdt = datetime.datetime.strptime(tstxt, "%Y%m%d").date()
        return tsdt
        
        
    def process_members(self):
        """Extracts files of interest out of tarball"""
        #There has to be a better way to do this
        #this is a dumb hack - fix at later date
        members = self.tf.getnames()
        splitMembers = [item.split("_") for item in members]        
        dsNames = [[item[0:3] if v==2 else item for v, item in enumerate(row)] for row in splitMembers]
        for member, row in zip(members, dsNames):
            if row[2] in self.datasets:
                outputPath = os.path.join(self.workspace, row[2])
                self.tf.extract(member, outputPath)
                
class WktDirectory:
    def __init__(self, path):
        self.path = path
        self.files = self.list_wkt_files()
        self.paths = [os.path.join(self.path, item) for item in self.files]


    def list_wkt_files(self):
        files = os.listdir(self.path)
        files = [file.split(".") for file in files[:]]
        files = [file for file in files if file[1] == "wkt" and file[2] == "txt"]
        files = [".".join(file) for file in files[:]]
        return files


class WktFile:
    def __init__(self, path, tableName):
        self.path = path
        self.lines = None
        self.tableName = tableName.lower()
        self.uploadBook = []
        self.timestamp = None
        self.connection = psycopg2.connect("dbname=nexrad user=post_root password=Fgs_rocks_g1 host=localhost")
        
    def get_lines(self):
        with open(self.path, "r") as f:
            self.lines=[line for line in f]

    def parse_geom(self, line):
        geom = re.findall("""POLYGON\s\(\(.*\)\)""", line)[0]
        quoted = "\'{0}\'".format(geom)
        return geom

    def parse_values(self, line):
        txt = re.findall("""value\=\d+\.\d+""", line)[0]
        split = txt.split("=")[1]
        return float(split)

    def parse_color_index(self, line):
        txt = re.findall("""colorIndex\=\d+""", line)[0]
        split = txt.split("=")[1]
        return int(split)

    def parse_timestamp(self):
        basePath = self.path.split(".")[0]
        fn = os.path.split(basePath)[1]
        fnSplit = fn.split("_")[3]
        timestamp = datetime.datetime.strptime(fnSplit, "%Y%m%d%H%M")
        utc = timestamp.strftime("\'%Y-%m-%d %H:%M:00 UTC\'")
        self.timestamp = utc
        
    def parse_all_lines(self):
        if self.lines is None:
            self.get_lines()
        if self.timestamp is None:
            self.parse_timestamp()


        for i in range(len(self.lines)):
            line = self.lines.pop(0)
            rowDict = {}
            rowDict["geom"] = self.build_st_geom(self.parse_geom(line))
            rowDict["value"] = self.parse_values(line)
            rowDict["colorindex"] = self.parse_color_index(line)
            rowDict["date_time"] = self.timestamp
            rowDict["table"] = self.tableName
            self.uploadBook.append(rowDict)
    def build_st_geom(self, geom):
        sql = "ST_GeomFromText(\'{0}\',{1})".format(geom, 4269)
        return sql

    def upload(self):
        cursor=self.connection.cursor()
        for row in self.uploadBook:
            if row["value"] > 0:
                cursor.execute("""INSERT INTO %(table)s (geom, val, date_time) values (%(geom)s, %(value)s, %(date_time)s);""" % row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        del cursor, self.connection
        
if __name__ == "__main__":
    
    #logging setup  
    times = {"start": datetime.datetime.now()}
    logPath = '/media/data/nexrad/nexradlog.log'
    logging.basicConfig(filename = logPath, filemode='w', level=logging.DEBUG)
    logging.critical('Begin Import: %s' % datetime.datetime.now())
        

    args = sys.argv[1:]
    inputPath = args[0]
    #print inputPath
    outputPath = args[1]
    #print outputPath
    voi = args[2:]
    #print voi
    
    tDir = TarDirectory(inputPath, outputPath, voi)
    
    logging.info('Writing folders: %s' % datetime.datetime.now)
    tDir.write_output_folders()
    

    print "Untarring"
    times["tar"] = [datetime.datetime.now()]
    for v, path in enumerate(tDir.tarpaths):
        print "Untarring {0} of {1}".format(v+1, len(tDir.tarpaths) + 1)
        tFile = NexradTar(path, outputPath, voi)
        tFile.process_members()
        del tFile
    times['tar'].append(datetime.datetime.now())

          
    
    times['wct'] = [datetime.datetime.now()]
    for var in voi:
        print "Calling WCT for:", var
        binaryIn = os.path.join(outputPath, var)        
        wktOut = os.path.join(outputPath, "{0}_wkt".format(var))
        systemcall = build_system_call(binaryIn, wktOut)
        os.system(systemcall)
    times['wct'].append(datetime.datetime.now())

    
    for var in voi:
        print "Removing:", var
        rmDir = os.path.join(outputPath, var)
        shutil.rmtree(rmDir)    
    
    for v, var in enumerate(voi):        
        times[var] = [datetime.datetime.now()]
        print "Uploading:",var
        wktIn = os.path.join(outputPath, "{0}_wkt".format(var))
        wktDir = WktDirectory(wktIn)
        for w, path in enumerate(wktDir.paths):
            print "Importing {0} ({1} of {2}): {3} ({4} of {5})".format(var, v+1, len(voi), os.path.split(path)[1], w+1, len(wktDir.paths))
            wkt = WktFile(path, var)
            wkt.parse_all_lines()
            wkt.upload()
            del wkt
        shutil.rmtree(wktIn)
        times[var].append(datetime.datetime.now())
        
    logging.info('----Elapsed Times----')
    elapsedTar = times['tar'][1] - times['tar'][0]
    logging.info('Untar: %s' % elapsedTar)
    elapsedWct = times['wct'][1] - times['wct'][0]
    logging.info('WCT: %s' % elapsedWct)
    for var in voi:
        elapsedTime = times[var][1] - times[var][0]
        logging.info('Upload {0}: {1}'.format(var, elapsedTime))
        print var, "uploaded"
    print "Done"

        
      
"""
python nexrad.py /media/data/nexrad/original/2012tar /media/data/nexrad/workspace DAA N1P N3P DPA
"""   
    
    
    
        
        