# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 12:40:09 2014

@author: Bassett_S
"""

import tarfile

testFile = r'C:\GISData\WKP Data\Flat Data\NEXRAD\2012tar\NWS_NEXRAD_NXL3_KTLH_20120101000000_20120101235959.tar'

tz = tarfile.TarFile(testFile)

mList = tz.getnames()
for i in mList:
    if i.split("_")[2] == "DSPTLH":
        tz.extract(i, r'C:\PythonWorkspace\zipworkspace')
