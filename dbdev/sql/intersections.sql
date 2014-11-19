/*INSERT INTO intersections (geom, date_time, bid, n3p_id)
SELECT clipped_geom, clipped.date_time, clipped.gid, clipped.fid
FROM (SELECT (ST_Dump(ST_Intersection(n.geom, b.geom))).geom As clipped_geom, n.date_time, b.gid, n.fid
FROM n3p_sp as n
	INNER JOIN basins b
	ON ST_Intersects(n.geom, b.geom))  As clipped
	WHERE ST_Dimension(clipped.clipped_geom) = 2;*/

--worked(?)	

CREATE TABLE n3p_invalid AS 
    SELECT * FROM n3p WHERE ST_IsValid(geom) IS FALSE;

DELETE FROM n3p WHERE ST_IsValid(geom) IS FALSE;

CREATE TABLE n3p_intersection AS 
    SELECT clipped_geom geom, clipped.date_time date_time, clipped.gid gid, clipped.fid fid, clipped.val val
        FROM (SELECT (ST_Intersection(n.geom, b.geom)).geom As clipped_geom, n.date_time, b.gid, n.fid, n.val
        FROM n3p as n
            INNER JOIN basins b
            ON ST_Intersects(n.geom, b.geom))  As clipped
            WHERE ST_Dimension(clipped.clipped_geom) = 2;
            
ALTER TABLE n3p_intersection ADD COLUMN area NUMERIC;
ALTER TABLE n3p_intersection ADD COLUMN volume NUMERIC;
ALTER TABLE n3p_intersection ADD COLUMN gallons NUMERIC;
UPDATE n3p_intersection SET area = ST_Area(geom);
UPDATE n3p_intersection SET volume = (val/12) * area;
UPDATE n3p_intersection SET gallons = volume * 7.48052;

CREATE INDEX ON n3p_intersection (gid);


CREATE TABLE n1p_invalid AS 
    SELECT * FROM n1p WHERE ST_IsValid(geom) IS FALSE;

DELETE FROM n1p WHERE ST_IsValid(geom) IS FALSE;

CREATE TABLE n1p_intersection AS 
    SELECT clipped_geom geom, clipped.date_time date_time, clipped.gid gid, clipped.fid fid, clipped.val val
        FROM (SELECT (ST_Intersection(n.geom, b.geom)) As clipped_geom, n.date_time, b.gid, n.fid, n.val
        FROM n1p as n
            INNER JOIN basins b
            ON ST_Intersects(n.geom, b.geom))  As clipped
            WHERE ST_Dimension(clipped.clipped_geom) = 2;
            
ALTER TABLE n1p_intersection ADD COLUMN area NUMERIC;
ALTER TABLE n1p_intersection ADD COLUMN volume NUMERIC;
ALTER TABLE n1p_intersection ADD COLUMN gallons NUMERIC;
UPDATE n1p_intersection SET area = ST_Area(geom);
UPDATE n1p_intersection SET volume = (val/12) * area;
UPDATE n1p_intersection SET gallons = volume * 7.48052;

CREATE TABLE dpa_invalid AS 
    SELECT * FROM dpa WHERE ST_IsValid(geom) IS FALSE;

    DELETE FROM dpa WHERE ST_IsValid(geom) IS FALSE;

CREATE TABLE dpa_intersection AS 
    SELECT clipped_geom geom, clipped.date_time date_time, clipped.gid gid, clipped.fid fid, clipped.val val
        FROM (SELECT (ST_Intersection(n.geom, b.geom)) As clipped_geom, n.date_time, b.gid, n.fid, n.val
        FROM dpa as n
            INNER JOIN basins b
            ON ST_Intersects(n.geom, b.geom))  As clipped
            WHERE ST_Dimension(clipped.clipped_geom) = 2;

ALTER TABLE dpa_intersection ADD COLUMN area NUMERIC;
ALTER TABLE dpa_intersection ADD COLUMN volume NUMERIC;
ALTER TABLE dpa_intersection ADD COLUMN gallons NUMERIC;
UPDATE dpa_intersection SET area = ST_Area(geom);
UPDATE dpa_intersection SET volume = (val/12) * area;
UPDATE dpa_intersection SET gallons = volume * 7.48052;
/*NOT RUN YET!!!!!!

CREATE TABLE daa_invalid AS 
    SELECT * FROM daa WHERE ST_IsValid(geom) IS FALSE;

    DELETE FROM daa WHERE ST_IsValid(geom) IS FALSE;

CREATE TABLE daa_intersection AS 
    SELECT clipped_geom geom, clipped.date_time date_time, clipped.gid gid, clipped.fid fid, clipped.val val
        FROM (SELECT (ST_Intersection(n.geom, b.geom)) As clipped_geom, n.date_time, b.gid, n.fid, n.val
        FROM daa as n
            INNER JOIN basins b
            ON ST_Intersects(n.geom, b.geom))  As clipped
            WHERE ST_Dimension(clipped.clipped_geom) = 2;
            
ALTER TABLE n1p_intersection ADD COLUMN area NUMERIC;
ALTER TABLE n1p_intersection ADD COLUMN volume NUMERIC;
ALTER TABLE n1p_intersection ADD COLUMN gallons NUMERIC;





/*
CREATE TABLE daa_invalid AS 
    SELECT * FROM daa WHERE ST_IsValid(geom) IS FALSE;

DELETE FROM daa WHERE ST_IsValid(geom) IS FALSE;
*/
