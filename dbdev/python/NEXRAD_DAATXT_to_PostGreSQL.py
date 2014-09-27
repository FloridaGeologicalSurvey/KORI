# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 15:06:25 2014

@author: Bassett_S
"""

import arcpy, datetime, os, psycopg2
arcpy.env.workspace = r'C:\PythonWorkspace\NEXRAD\SHP'

fcList = arcpy.ListFeatureClasses()
fcBasins = r'C:/PythonWorkspace/NEXRAD/Intersect.gdb/basins_of_interest'
fcMerged = r'C:\PythonWorkspace\NEXRAD\Intersect.gdb\daa_nov_merge'
fcProjected = r'C:\PythonWorkspace\NEXRAD\Intersect.gdb\daa_nov_merge_SP'
fcIntersect = r'C:\PythonWorkspace\NEXRAD\Intersect.gdb\daa_nov_merge_SP_Intersect'
for i in fcList:
    split = i.split("_")
    time = datetime.datetime.strptime(str(os.path.splitext(split[3])[0]), "%Y%m%d%H%M")
    texttime = time.strftime("%Y-%m-%d %H:%M:%S")
    texttime = """\'""" + texttime + """\'"""
    if len(arcpy.ListFields(i, "date_time")) == 0:
        arcpy.AddField_management(i, "date_time", "TEXT")
        arcpy.CalculateField_management(i, "date_time", str(texttime), "PYTHON")
    
    
arcpy.Merge_management(fcList, fcMerged)

arcpy.Project_management(fcMerged,fcProjected,"PROJCS['NAD_1983_HARN_StatePlane_Florida_North_FIPS_0903_Feet',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',1968500.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-84.5],PARAMETER['Standard_Parallel_1',29.58333333333333],PARAMETER['Standard_Parallel_2',30.75],PARAMETER['Latitude_Of_Origin',29.0],UNIT['Foot_US',0.3048006096012192]]","'WGS_1984_(ITRF00)_To_NAD_1983 + NAD_1983_HARN_To_WGS_1984_2'","GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
inFeaturesIntersect = [fcBasins, fcIntersect]
arcpy.Intersect_analysis(inFeaturesIntersect,fcIntersect,"ALL","#","INPUT")

import csv
from collections import namedtuple
daatxt = r'C:\PythonWorkspace\NEXRAD\daa_nov_gt0.txt'
pw = "Fgs_rocks_g1"
connection_info = ["fgs-27951g1","nexrad","post_root",pw]

con = psycopg2.connect(dsn=None, 
    host= connection_info[0],
    database= connection_info[1],
    user= connection_info[2],
    password= connection_info[3])
cur = con.cursor()
cur.execute('SET SESSION TIME ZONE UTC')
with open(daatxt) as f:
    fcsv = csv.reader(f)
    headers = next(fcsv)
    for v, i in enumerate(headers):
        print v,i
    Row = namedtuple('Row', headers)
    print "Entering Loop"
    count = 1
    for r in fcsv:
        print "Loop", count
        count += 1
        row = Row(*r)
        precipFeet = float(row.value) / 12
        precipCubed = float(row.Shape_Area) * precipFeet
        precipGallons = precipCubed * 7.48052
        timestamp = row.date_time + " UTC"
        print "Executing SQL load"        
        cur.execute("""INSERT INTO daa_nov (date_time, basin_fid, huc, exthuc, basin_name, feature_type, nexrad_fid, rainfall, intersect_area, ft_precip, ft_cubed_precip, gallons_precip)
                        values(%(date_time)s, %(basinFid)s, %(huc)s, %(exthuc)s, %(basin_name)s, %(feature_type)s, %(nexrad_fid)s, %(rainfall)s, %(intersect_area)s, %(ft_precip)s, %(ft_cubed_precip)s, %(gallons_precip)s);""",
                        {'date_time':timestamp, 'basinFid':row.FID_basins_of_interest, 'huc':row.HUC, 'exthuc':row.EXTHUC, 'basin_name':row.BASIN, 'feature_type':row.FEATURE, 'nexrad_fid':row.FID_daa_nov_merge_SP, 'rainfall':row.value, 'intersect_area':row.Shape_Area, 'ft_precip':precipFeet, 'ft_cubed_precip':precipCubed, 'gallons_precip':precipGallons})
        
con.commit()
cur.close()
con.close()

#fields = ["OBJECTID","FID_basins_of_interest", "AREA", "HUC", "EXTHUC","BASIN","FEATURE","SQ_MILES","FID_daa_nov_merge_SP","value","date_time","Shape_Area"]
#fieldDict = {v:i for v, i in enumerate(fields)}
#
#pw = "Fgs_rocks_g1"
#connection_info = ["fgs-27951g1","nexrad","post_root",pw]
#
#con = psycopg2.connect(dsn=None, 
#    host= connection_info[0],
#    database= connection_info[1],
#    user= connection_info[2],
#    password= connection_info[3])
#cur = con.cursor()
#cur.execute('SET SESSION TIME ZONE UTC')
#
#    
#with arcpy.da.SearchCursor(fcIntersect, fields) as cursor:
#    for row in cursor:
#        precipFeet = row[9] / 12
#        precipCubed = row[11] * precipFeet
#        precipGallons = precipCubed * 7.48052
#        timestamp = row[10] + " UTC"
#        cur.execute("""INSERT INTO daa_nov (date_time, basin_fid, huc, exthuc, basin_name, feature_type, nexrad_fid, rainfall, intersect_area, ft_precip, ft_cubed_precip, gallons_precip)
#                        values(%(date_time)s, %(basinFid)s, %(huc)s, %(exthuc)s, %(basin_name)s, %(feature_type)s, %(nexrad_fid)s, %(rainfall)s, %(intersect_area)s, %(ft_precip)s, %(ft_cubed_precip)s, %(gallons_precip)s);""",
#                        {'date_time':timestamp, 'basinFid':row[1], 'huc':row[3], 'exthuc':row[4], 'basin_name':row[5], 'feature_type':row[6], 'nexrad_fid':row[8], 'rainfall':row[9], 'intersect_area':row[11], 'ft_precip':precipFeet, 'ft_cubed_precip':precipCubed, 'gallons_precip':precipGallons})
#        con.commit()
#cur.close()
#con.close()
    