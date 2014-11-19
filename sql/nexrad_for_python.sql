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