# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 13:58:10 2014

@author: Bassett_S
"""

import requests, datetime

"""
http://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20130101 10:00&end_date=20130101 10:24&station=8454000&product=water_level&datum=mllw&units=metric&time_zone=gmt&application=web_services&format=xml
"""

interval = datetime.timedelta(days=30)
startDT = datetime.datetime(2006, 1, 1, 0, 0, 0)
endDT = datetime.datetime(2006, 1, 31, 23, 59, 59)
maxDT = datetime.datetime(2013, 12, 31, 23, 59, 59)
outputPath = r'C:\PythonWorkspace\NOAA'

firstLoop = True
while endDT < maxDT:
    payload = {}
    payload['station'] = '8728690'
    if firstLoop:
        payload["begin_date"] = startDT.strftime("%Y%m%d")
        payload["end_date"] = endDT.strftime("%Y%m%d")        
        firstLoop = False
    else:
        loopStartDT = startDT + datetime.timedelta(days=1)
        payload["begin_date"] = loopStartDT.strftime("%Y%m%d")
        payload["end_date"] = endDT.strftime("%Y%m%d")
    payload["product"] = "water_level"
    payload["datum"] = 'NAVD'
    payload["units"] = 'english'
    payload["time_zone"] = 'gmt'
    payload["format"] = 'csv'
    r = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter", params=payload)
    with open(r'C:\PythonWorkspace\NOAA\WLE_API_8728690.txt', "a") as f:
        f.write(r.text)
    #print payload["begin_date"], payload["end_date"]
    startDT += interval
    endDT += interval

endDT = endDT + datetime.timedelta(days=1)
payload["begin_date"] = endDT.strftime("%Y%m%d")
payload["end_date"] = maxDT.strftime("%Y%m%d")
r = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter", params=payload)
with open(r'C:\PythonWorkspace\NOAA\WLE_API_8728690.txt', "a") as f:
    f.write(r.text)   
 
############# AIR PRES   

interval = datetime.timedelta(days=30)
startDT = datetime.datetime(2006, 7, 1, 0, 0, 0)
endDT = datetime.datetime(2006, 7, 31, 23, 59, 59)
maxDT = datetime.datetime(2013, 12, 31, 23, 59, 59)

while endDT < maxDT:
    payload = {}
    payload['station'] = '8728690'
    if firstLoop:
        payload["begin_date"] = startDT.strftime("%Y%m%d")
        payload["end_date"] = endDT.strftime("%Y%m%d")        
        firstLoop = False
    else:
        loopStartDT = startDT + datetime.timedelta(days=1)
        payload["begin_date"] = loopStartDT.strftime("%Y%m%d")
        payload["end_date"] = endDT.strftime("%Y%m%d")
    payload["product"] = "air_pressure"
    payload["datum"] = 'NAVD'
    payload["units"] = 'english'
    payload["time_zone"] = 'gmt'
    payload["format"] = 'csv'
    r = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter", params=payload)
    with open(r'C:\PythonWorkspace\NOAA\AIRPRES_API_8728690.txt', "a") as f:
        f.write(r.text)
    #print payload["begin_date"], payload["end_date"]
    startDT += interval
    endDT += interval

endDT = endDT + datetime.timedelta(days=1)
payload["begin_date"] = endDT.strftime("%Y%m%d")
payload["end_date"] = maxDT.strftime("%Y%m%d")
r = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter", params=payload)
with open(r'C:\PythonWorkspace\NOAA\AIRPRES_API_8728690.txt', "a") as f:
    f.write(r.text)


################### water temp
interval = datetime.timedelta(days=30)
startDT = datetime.datetime(2006, 7, 1, 0, 0, 0)
endDT = datetime.datetime(2006, 7, 31, 23, 59, 59)
maxDT = datetime.datetime(2013, 12, 31, 23, 59, 59)

while endDT < maxDT:
    payload = {}
    payload['station'] = '8728690'
    if firstLoop:
        payload["begin_date"] = startDT.strftime("%Y%m%d")
        payload["end_date"] = endDT.strftime("%Y%m%d")        
        firstLoop = False
    else:
        loopStartDT = startDT + datetime.timedelta(days=1)
        payload["begin_date"] = loopStartDT.strftime("%Y%m%d")
        payload["end_date"] = endDT.strftime("%Y%m%d")
    payload["product"] = "water_temperature"
    payload["datum"] = 'NAVD'
    payload["units"] = 'english'
    payload["time_zone"] = 'gmt'
    payload["format"] = 'csv'
    r = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter", params=payload)
    with open(r'C:\PythonWorkspace\NOAA\WTEMP_API_8728690.txt', "a") as f:
        f.write(r.text)
    #print payload["begin_date"], payload["end_date"]
    startDT += interval
    endDT += interval

endDT = endDT + datetime.timedelta(days=1)
payload["begin_date"] = endDT.strftime("%Y%m%d")
payload["end_date"] = maxDT.strftime("%Y%m%d")
r = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter", params=payload)
with open(r'C:\PythonWorkspace\NOAA\WTEMP_API_8728690.txt', "a") as f:
    f.write(r.text)   

################# AIR TEMP #########################

interval = datetime.timedelta(days=30)
startDT = datetime.datetime(2006, 7, 1, 0, 0, 0)
endDT = datetime.datetime(2006, 7, 31, 23, 59, 59)
maxDT = datetime.datetime(2013, 12, 31, 23, 59, 59)

while endDT < maxDT:
    payload = {}
    payload['station'] = '8728690'
    if firstLoop:
        payload["begin_date"] = startDT.strftime("%Y%m%d")
        payload["end_date"] = endDT.strftime("%Y%m%d")        
        firstLoop = False
    else:
        loopStartDT = startDT + datetime.timedelta(days=1)
        payload["begin_date"] = loopStartDT.strftime("%Y%m%d")
        payload["end_date"] = endDT.strftime("%Y%m%d")
    payload["product"] = "air_temperature"
    payload["datum"] = 'NAVD'
    payload["units"] = 'english'
    payload["time_zone"] = 'gmt'
    payload["format"] = 'csv'
    r = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter", params=payload)
    with open(r'C:\PythonWorkspace\NOAA\ATEMP_API_8728690.txt', "a") as f:
        f.write(r.text)
    #print payload["begin_date"], payload["end_date"]
    startDT += interval
    endDT += interval

endDT = endDT + datetime.timedelta(days=1)
payload["begin_date"] = endDT.strftime("%Y%m%d")
payload["end_date"] = maxDT.strftime("%Y%m%d")
r = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter", params=payload)
with open(r'C:\PythonWorkspace\NOAA\ATEMP_API_8728690.txt', "a") as f:
    f.write(r.text)   
