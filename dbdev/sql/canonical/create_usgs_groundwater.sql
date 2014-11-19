CREATE TABLE extra.usgs_groundwater
(
  gwid SERIAL CONSTRAINT usgs_gw PRIMARY KEY,
  site_id INTEGER REFERENCES sites (site_id),
  station CHAR(15),
  date_time timestamp with time zone, --USGS uses EST/EDT
  gw_elev numeric(4,2), --groundwater elevation, feet
  flag char(1) --data quality flag
);

ALTER TABLE extra.usgs_groundwater
  OWNER TO post_root;
COMMENT ON TABLE extra.usgs_groundwater
  IS 'USGS groundwater monitor station at Crawfordville';
COMMENT ON COLUMN extra.usgs_groundwater.gwid IS 'Table Primary Key, Sequential';
COMMENT ON COLUMN extra.usgs_groundwater.site_id IS 'Foreign key from sites table';
COMMENT ON COLUMN extra.usgs_groundwater.station IS 'USGS Station ID';
COMMENT ON COLUMN extra.usgs_groundwater.date_time IS 'Datetime of observation. Note that USGS uses EDT/EST timezones';
COMMENT ON COLUMN extra.usgs_groundwater.gw_elev IS 'Groundwater Elevation, in feet. Vertical datum is NGVD29';
COMMENT ON COLUMN extra.usgs_groundwater.flag IS 'Data Quality Flag. A=approved for publication, P=provisional';