CREATE TABLE noaa_coops
(
    coops_id SERIAL CONSTRAINT coops_id PRIMARY KEY,
    site_id INTEGER REFERENCES sites (site_id),
    station_id INTEGER,
    date_time TIMESTAMP WITH TIME ZONE,
    wle NUMERIC(5,3),
    sigma NUMERIC(5,3),
    O integer,
    F integer,
    R integer,
    L INTEGER,
    quality CHAR(1)
);

ALTER TABLE noaa_coops
    OWNER TO postgres;
    
COMMENT ON TABLE noaa_coops IS 'NOAA Tidal Data';
COMMENT ON COLUMN noaa_coops.coops_id IS 'Table Primary Key, sequential integer';
COMMENT ON COLUMN noaa_coops.site_id IS 'Foreign Key from sites table';
COMMENT ON COLUMN noaa_coops.station_id IS 'Station Identifier';
COMMENT ON COLUMN noaa_coops.date_time IS 'Timestamp, UTC';
COMMENT ON COLUMN noaa_coops.wle IS 'Water Level Elevation, NAVD88 (ft)';
COMMENT ON COLUMN noaa_coops.sigma IS 'Unknown field';
COMMENT ON COLUMN noaa_coops.O IS 'Unknown field';
COMMENT ON COLUMN noaa_coops.F IS 'Unknown field';
COMMENT ON COLUMN noaa_coops.R is 'Unknown Field';
COMMENT ON COLUMN noaa_coops.L is 'Unknown field';
COMMENT ON COLUMN noaa_coops.quality IS 'Quality Flag. v = verified';



    