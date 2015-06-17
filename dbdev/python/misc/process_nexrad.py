# -*- coding: utf-8 -*-
"""
Created on Tue Sep 09 15:17:00 2014

@author: Bassett_S
"""
import os, tarfile, datetime
from subprocess import Popen



inputWorkspace = r'C:\GISData\WKP Data\Flat Data\NEXRAD\2012tar'
zipWorkspace = r'C:\PythonWorkspace\NEXRAD\zipworkspace'

print 'Enter Start Date in format YYYY-MM-DD'
startDate = raw_input('---> ')
startDT = datetime.datetime.strptime(startDate, "%Y-%m-%d")
startDate = startDT.date()

print 'Enter End Date in Format YYYY-MM-DD'
endDate = raw_input('---> ')
endDT = datetime.datetime.strptime(endDate, "%Y-%m-%d")
endDate = endDT.date()

del startDT, endDT

files = os.listdir(inputWorkspace)
parsedFiles = [i.split("_") for i in files]
print "Looping filenames"
for i,j in zip(parsedFiles, files):
    fDate = datetime.datetime.strptime(i[4], "%Y%m%d%H%M%S")
    fDate = fDate.date()
    if fDate >= startDate and fDate <= endDate:
        tfPath = os.path.join(inputWorkspace, j)
        tf = tarfile.TarFile(tfPath)
        tfMembers = tf.getnames()
        print "Extracting",j        
        for k in tfMembers:
            if k.split("_")[2] == 'DAATLH':
                tf.extract(k, zipWorkspace)

del files, parsedFiles, i, j, fDate, tfPath, tf, tfMembers, k

print "Converting to SHP"
batch = Popen(["cmd.exe","/c nexrad_batch_to_shape.bat"], cwd= r"C:\\GISData\\WKP Data\\Flat Data\\wct-3.7.3")
stdout, stderr = batch.communicate()






#for i, j in zip(files, parsedFiles):
#    if len(j) > 1:
#        if j[2] == 'N1PTLH' or j[2] == 'N3PTLH' or j[2] == 'DPRTLH':
#            pass
#        else:
#            rmfile = os.path.join(inputWorkspace, i)
#            os.remove(rmfile)

