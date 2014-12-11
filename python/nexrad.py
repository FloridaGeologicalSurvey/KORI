import os
import tarfile
import datetime
import sys
import psycopg2
import re
import shutil
import logging
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="Input Directory of NEXRAD Tarballs")
    parser.add_argument("output", type=str, help="Scratch Workspace")
    parser.add_argument("-d","--datasets", type=str, action="append", help="NEXRAD datasets to export, can be multiple")
    parser.add_argument("-x","--xml", type=str, help="location of WCT xml config file")
    parser.add_argument("-w","--wct", type=str, help="location of wct-batch exe")
    parser.add_argument("-db","--database", type=str, help="Database Name")
    parser.add_argument("-ho","--host",type=str, help="host name")
    parser.add_argument("-v","--verbose", type='store_true')
    args = parser.parse_args()
    
    location = os.getcwd()
    logfile = os.path.join(location, "nexrad.log")
    logging.basicConfig(filename = logfile, filemode='w', level=logging.DEBUG)
    
    tarDir = TarDirectory(args.input, args.output, args.datasets)
    if args.verbose:
        print "Writing Workspace Folders"
    logging.info('Writing folders: %s' % datetime.datetime.now())
    tarDir.write_output_folders()
    
    #untar
    logging.info('Starting Untar: %s' % datetime.datetime.now())
    if args.verbose:
        print "Untarring"
    for path in tarDir.tarpaths:
        if args.verbose:
            print "Processing:", path
        tfile = NexradTar(path, args.output, args.datasets)
        tfile.process_members()
        del tfile
    logging.info('Finished Untar: %s' % datetime.datetime.now())
    
    #Call wct-batch
    if args.wct and args.xml:
        if os.path.exists(args.wct) and os.path.exists(args.xml):
            if args.verbose:
                print "Calling WCT"
            for dset in args.datasets:
                logging.info('Calling WCT for {0}: {1}'.format(dset, 
                                 datetime.datetime.now()))
                inputDir = os.path.join(args.output, dset)
                output = os.path.join(args.output, "{0}_wkt".format(dset))
                systemcall = build_system_call(args.wct, inputDir, output, args.xml)
                os.system(systemcall)
                logging.info('Finished WCT for {0}: {1}'.format(dset, 
                                 datetime.datetime.now()))
                
            #remove binary files
            if args.verbose:
                print "Deleting Binary Files"
            for dset in args.datasets:
                logging.info('Deleting Binaries for {0}: {1}'.format(dset, 
                                 datetime.datetime.now()))
                rmDir = os.path.join(args.output, dset)
                shutil.rmtree(rmDir)
            
            if args.database:
                #create db tables
                if args.verbose:
                    print "Creating Tables"
                for dset in args.datasets:
                    sql = create_table_sql(dset)
                    execute_sql(location, sql, args.database)
                    
                #upload
                if args.verbose:
                    print "Uploading"
                for dset in args.datasets:
                    logging.info('Uploading {0}: {1}'.format(dset, 
                                     datetime.datetime.now()))
                    inputDir = os.path.join(args.output, "{0}_wkt".format(dset))
                    wktdir = WktDirectory(inputDir)
                    for path in wktdir.paths:
                        wkt = WktFile(path, dset)
                        wkt.parse_all_lines()
                        wkt.upload()
                        del wkt
                    shutil.rmtree(inputDir)
                
                #vacuum analyze
                logging.info('VACUUM ANALYZE: {0}'.format(datetime.datetime.now()))
                if args.verbose:
                    print "VACUUM ANALYZING"
                execute_sql(location, "VACUUM ANALYZE;", args.database)
                
                #execute postgis
                if args.verbose:
                    print "Intersecting"
                for dset in args.datasets:
                    logging.info('PostGIS Function {0}: {1}'.format(dset, 
                                     datetime.datetime.now()))
                    sql = postgis_sql(dset)
                    execute_sql(location, sql, args.database)
                if args.verbose:
                    print "VACUUM ANALYZING"                
                execute_sql(location, "VACUUM ANALYZE;", args.database)
                if args.verbose:
                    print "Done"
    
####    


    
def execute_sql(path, sql, dbname):
    sqlpath = os.path.join(path, "sql.sql")
    with open(sqlpath, "w") as f:
        f.write(sql)
    psql = "psql -d {0} -a -f {1}".format(dbname, sqlpath)
    os.system(psql)


def create_table_sql(table):
    sql = """CREATE TABLE {0} (
	fid BIGSERIAL PRIMARY KEY,
	geom geometry(POLYGON,4269) ,
	val NUMERIC,
	date_time TIMESTAMP WITH TIME ZONE
	);"""
    return sql.format(table.lower())

def postgis_sql(table):
    sql = """
    --POSTGIS PROCESSING CHAIN

    --Project to State Plane North (US Ft.)
    CREATE TABLE {0}_sp AS
        SELECT fid, ST_Transform(geom, 2238) as geom, val, date_time
        FROM {0};

    --Drop Original Table
    DROP TABLE {0};

    --Rename Projected table to Original Name
    ALTER TABLE {0}_sp RENAME TO {0};

    --Create index. Is this needed before large intersection?
    CREATE INDEX indx_geom_{0} ON {0} USING gist (geom);

    --Create a table for invalid geometries
    --This should be a flagged option in python
    CREATE TABLE {0}_invalid AS 
        SELECT * FROM {0} WHERE ST_IsValid(geom) IS FALSE;

    --Delete invalid geometries
    DELETE FROM {0} WHERE ST_IsValid(geom) IS FALSE;

    --intersect with basins and create intersection table
    CREATE TABLE {0}_intersection AS 
        SELECT clipped_geom geom, clipped.date_time date_time, clipped.objectid objectid, clipped.fid fid, clipped.val val
            FROM (SELECT (ST_Intersection(n.geom, b.geom)) As clipped_geom, n.date_time, b.objectid, n.fid, n.val
            FROM {0} as n
                INNER JOIN basins b
                ON ST_Intersects(n.geom, b.geom))  As clipped
                WHERE ST_Dimension(clipped.clipped_geom) = 2;

    --Add columns for calculated values
    ALTER TABLE {0}_intersection ADD COLUMN area NUMERIC;
    ALTER TABLE {0}_intersection ADD COLUMN volume NUMERIC;
    ALTER TABLE {0}_intersection ADD COLUMN gallons NUMERIC;

    --Calculate area of each intersection polygon
    UPDATE {0}_intersection SET area = ST_Area(geom);

    --Calculate volume of water represented by intersection polygon;
    UPDATE {0}_intersection SET volume = (val/12) * area;

    --Calculate gallons from cubic feet
    UPDATE {0}_intersection SET gallons = volume * 7.48052;

    CREATE INDEX ON {0}_intersection (objectid, date_time);



    --sum by basins
    CREATE TABLE {0}_basins AS
        SELECT objectid, date_time, sum(area) as area, sum(volume) as volume, sum(gallons) as gallons FROM {0}_intersection GROUP BY objectid, date_time ORDER BY date_time;

    ALTER TABLE {0}_basins ADD CONSTRAINT {0}_fk FOREIGN KEY (objectid) REFERENCES basins (objectid);
    CREATE INDEX ON {0}_basins (objectid);
    CREATE INDEX on {0}_basins (date_time);
    CREATE UNIQUE INDEX ON {0}_basins (objectid, date_time);
    CREATE INDEX ON {0}_basins (volume);
    CREATE INDEX ON {0}_basins (gallons);

    DROP TABLE {0}_intersection;
    """
    return sql.format(table.lower())
    
def build_system_call(exe, inputDir, outputDir, xml):
    logfile = os.getcwd()
    logfile = os.path.join(logfile, "nexradlog.log")
    systemCall = "{0} {1} {2} {3} {4} > {5}".format(exe, inputDir, outputDir, "wkt", xml, logfile)
    return systemCall


class TarDirectory:
    """A directory of NEXRAD tar files"""
    def __init__(self, path, workspace, varList = [None]):
        """Class TarDirectory builds filenames and paths for a directory of nexrad
        tar files when it is initialized
        Args:
            path (str): The path to the directory that holds the tar files
            workspace (str): The path to the workspace directory
            varList (list of str): A list of the NEXRAD datasets
        
        """
        self.path = path
        self.files = os.listdir(path)
        self.workspace = workspace
        self.tarpaths = [os.path.join(self.path, item) for item in self.files]
        self.var = varList
    
    def write_output_folders(self):
        """Create a folder in the workspace for each variable in varList"""
        for arg in self.var:
            newBinaryOut = os.path.join(self.workspace, arg)
            if not os.path.exists(newBinaryOut):
                os.mkdir(newBinaryOut)
            newWKTout = os.path.join(self.workspace, "{0}_wkt".format(arg))
            if not os.path.exists(newWKTout):
                os.mkdir(newWKTout)  

class NexradTar:
    """A single NEXRAD tar file. See __init__ for full description"""
    
    def __init__(self, path, workspace, dataset = [None]):
        """This class if for individual nexrad tar files. The methods for this class
        parse the date for the NEXRAD data and extracts the members to a workspace folder
        created by ClassDirectory
        
        Args:
            path (str): the path to the NEXRAD tarball
            workspace (str): the path to the output workspace
            dataset (list of str): a list of the NEXRAD datasets of interest
        """
        self.path = path
        self.workspace = workspace
        self.datasets = dataset
        self.timestamp = self.parse_timestamp()
        self.tf = tarfile.TarFile(path)
        
        
    def parse_timestamp(self):
        """Strips the date from the filename"""
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
    """See __init__ for full documentation"""
    def __init__(self, path):
        """This class is for directories of WKT files created by the NOAA WCT batch exporter.
        
        Args:
            path (str): The path to the directory containing the WKT exports"""
        
        self.path = path
        self.files = self.list_wkt_files()
        self.paths = [os.path.join(self.path, item) for item in self.files]


    def list_wkt_files(self):
        """Lists just the .wkt files, ignores the others"""
        files = os.listdir(self.path)
        files = [file.split(".") for file in files[:]]
        files = [file for file in files if file[1] == "wkt" and file[2] == "txt"]
        files = [".".join(file) for file in files[:]]
        return files

class WktFile:
    """A Well Known Text file. See __init__ for full docstring"""
    
    def __init__(self, path, tableName):
        """This class is for uploading WKT files to PostGRESQL
        Args:
            path (str): the path to the WKT file
            tableName (str): the table name to upload to
        """
        self.path = path
        self.lines = None
        self.tableName = tableName.lower()
        self.uploadBook = []
        self.timestamp = None
        self.connection = psycopg2.connect("dbname=nexrad user=post_root password=Fgs_rocks_g1 host=localhost")
        
    def get_lines(self):
        """Read the WKT file"""
        with open(self.path, "r") as f:
            self.lines=[line for line in f]

    def parse_geom(self, line):
        """Parses the geometry string
        Args:
            line (str) : a line from a WKT file"""
        geom = re.findall("""POLYGON\s\(\(.*\)\)""", line)[0]
        return geom

    def parse_values(self, line):
        """Parses the value of the polygon
        Args:
            line (str) : a line from a WKT file"""
        txt = re.findall("""value\=\d+\.\d+""", line)[0]
        split = txt.split("=")[1]
        return float(split)

    def parse_color_index(self, line):
        """Parses the color index of a polygon
        Args:
            line (str) : a line from a WKT file"""
        txt = re.findall("""colorIndex\=\d+""", line)[0]
        split = txt.split("=")[1]
        return int(split)

    def parse_timestamp(self):
        """Parses the timestamp for the NEXRAD file."""
        basePath = self.path.split(".")[0]
        fn = os.path.split(basePath)[1]
        fnSplit = fn.split("_")[3]
        timestamp = datetime.datetime.strptime(fnSplit, "%Y%m%d%H%M")
        utc = timestamp.strftime("\'%Y-%m-%d %H:%M:00 UTC\'")
        self.timestamp = utc
        
    def parse_all_lines(self):
        """Build a list of dictionaries that represents the WKT strings and values for each polygon"""
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
        """Builds the necessary ST statement to insert the geometry as a PostGIS geometry"""
        sql = "ST_GeomFromText(\'{0}\',{1})".format(geom, 4269)
        return sql

    def upload(self):
        """Uploads the data to the database
        Currently set to that polygons with a value of 0 are ignored"""
        cursor=self.connection.cursor()
        for row in self.uploadBook:
            if row["value"] > 0:
                cursor.execute("""INSERT INTO %(table)s (geom, val, date_time) values (%(geom)s, %(value)s, %(date_time)s);""" % row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        del cursor, self.connection
 
if __name__=="__main__":
    main()
