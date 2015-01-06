CREATE TABLE sites (
  site_id SERIAL CONSTRAINT site_id PRIMARY KEY,
  site_name VARCHAR,
  site_code VARCHAR,
  latitude NUMERIC(8,6),
  longitude NUMERIC(8,6),
  xy_datum_epsg INTEGER,
  elevation_ft NUMERIC(6,3),
  z_datum_epsg INTEGER,
  localx NUMERIC(10,3),
  localy NUMERIC(9,3),
  projection_epsg INTEGER,
  pos_accuracy_ft NUMERIC,
  state_name VARCHAR,
  county_name VARCHAR,
  owner_name VARCHAR,
  program_name VARCHAR,
  table_name VARCHAR
  
);
ALTER TABLE sites OWNER to postgres;
COMMENT ON TABLE sites IS 'Site Information and Geometry';
COMMENT ON COLUMN sites.site_id IS 'Unique Serial Integer, Primary Key';
COMMENT ON COLUMN sites.site_name IS 'Site Name, Long Form';
COMMENT ON COLUMN sites.site_code IS 'The native sensor ID for the sensors program';
COMMENT ON COLUMN sites.latitude IS 'Latitude (NAD83)';
COMMENT ON COLUMN sites.longitude IS 'Longitude (NAD83)';
COMMENT ON COLUMN sites.xy_datum_epsg IS 'EPSG code for XY geographic datum';
COMMENT ON COLUMN sites.elevation_ft IS 'Elevation in feet (NAVD88)';
COMMENT ON COLUMN sites.z_datum_epsg IS 'EPSG code for Z geographic datum';
COMMENT ON COLUMN sites.localx IS 'Easting (State Plane North US ft.)';
COMMENT ON COLUMN sites.localy IS 'Northing (State Plane North US ft.)';
COMMENT ON COLUMN sites.projection_epsg IS 'EPSG code for local projection';
COMMENT ON COLUMN sites.pos_accuracy_ft IS 'XY Positional Accuracy (ft)';
COMMENT ON COLUMN sites.state_name IS 'State name';
COMMENT ON COLUMN sites.county_name IS 'County name';
COMMENT ON COLUMN sites.owner_name IS 'Owner name';
COMMENT ON COLUMN sites.program_name IS 'Program name';
COMMENT ON COLUMN sites.table_name IS 'Table name in which this data appears in the WKP-HRDB';

/* psql STDIN VALUES

COPY sites (site_name, site_code, latitude, longitude, xy_datum_epsg, elevation_ft, z_datum_epsg, localx, localy, projection_epsg, pos_accuracy_ft, state_name, county_name, owner_name, program_name, table_name) FROM stdin;
\.


*/