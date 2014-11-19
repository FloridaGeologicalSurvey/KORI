--POSTGIS PROCESSING CHAIN

--Project to State Plane North (US Ft.)
CREATE TABLE n3p_sp AS
    SELECT fid, ST_Transform(geom, 2238) as geom, val, date_time
    FROM n3p;

--Drop Original Table
DROP TABLE n3p;

--Rename Projected table to Original Name
ALTER TABLE n3p_sp RENAME TO n3p;

--Create index. Is this needed before large intersection?
CREATE INDEX indx_geom_n3p ON n3p USING gist (geom);

--Create a table for invalid geometries
--This should be a flagged option in python
CREATE TABLE n3p_invalid AS 
    SELECT * FROM n3p WHERE ST_IsValid(geom) IS FALSE;

--Delete invalid geometries
DELETE FROM n3p WHERE ST_IsValid(geom) IS FALSE;

--intersect with basins and create intersection table
CREATE TABLE n3p_intersection AS 
    SELECT clipped_geom geom, clipped.date_time date_time, clipped.objectid objectid, clipped.fid fid, clipped.val val
        FROM (SELECT (ST_Intersection(n.geom, b.geom)) As clipped_geom, n.date_time, b.objectid, n.fid, n.val
        FROM n3p as n
            INNER JOIN basins b
            ON ST_Intersects(n.geom, b.geom))  As clipped
            WHERE ST_Dimension(clipped.clipped_geom) = 2;

--Add columns for calculated values
ALTER TABLE n3p_intersection ADD COLUMN area NUMERIC;
ALTER TABLE n3p_intersection ADD COLUMN volume NUMERIC;
ALTER TABLE n3p_intersection ADD COLUMN gallons NUMERIC;

--Calculate area of each intersection polygon
UPDATE n3p_intersection SET area = ST_Area(geom);

--Calculate volume of water represented by intersection polygon;
UPDATE n3p_intersection SET volume = (val/12) * area;

--Calculate gallons from cubic feet
UPDATE n3p_intersection SET gallons = volume * 7.48052;

CREATE INDEX ON n3p_intersection (objectid, date_time);



--sum by basins
CREATE TABLE n3p_basins AS
    SELECT objectid, date_time, sum(area) as area, sum(volume) as volume, sum(gallons) as gallons FROM n3p_intersection GROUP BY objectid, date_time ORDER BY date_time;

ALTER TABLE n3p_basins ADD CONSTRAINT n3p_fk FOREIGN KEY (objectid) REFERENCES basins (objectid);
CREATE INDEX ON n3p_basins (objectid);
CREATE INDEX on n3p_basins (date_time);
CREATE UNIQUE INDEX ON n3p_basins (objectid, date_time);
CREATE INDEX ON n3p_basins (volume);
CREATE INDEX ON n3p_basins (gallons);

DROP TABLE n3p_intersection;