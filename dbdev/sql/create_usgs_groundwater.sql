CREATE TABLE usgs_groundwater
(
  gwid SERIAL CONSTRAINT usgs_gw PRIMARY KEY, --Table PK
  site_id CHAR(15), -- USGS Site ID Number
  date_time timestamp with time zone, --USGS uses EST/EDT
  gw_elev numeric(4,2), --groundwater elevation, feet
  flag char(1) --data quality flag
);

ALTER TABLE usgs_groundwater
  OWNER TO post_root;
COMMENT ON TABLE usgs_groundwater
  IS 'USGS groundwater monitor station at Crawfordville';
COMMENT ON COLUMN usgs_groundwater.gwid IS 'Table Primary Key, Sequential';
COMMENT ON COLUMN usgs_groundwater.site_id IS 'USGS site ID number';
COMMENT ON COLUMN usgs_groundwater.date_time IS 'Datetime of observation. Note that USGS uses EDT/EST timezones';
COMMENT ON COLUMN usgs_groundwater.gw_elev IS 'Groundwater Elevation, in feet. Vertical datum is NGVD29';
COMMENT ON COLUMN usgs_groundwater.flag IS 'Data Quality Flag. A=approved for publication, P=provisional';