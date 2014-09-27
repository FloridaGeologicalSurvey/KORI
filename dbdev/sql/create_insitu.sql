CREATE TABLE insitu
(
  insitu_id SERIAL CONSTRAINT insitu_key PRIMARY KEY,
  deploy_key integer REFERENCES deploy_info (deploy_key),
  date_time timestamp with time zone,
  elapsed_seconds numeric(10,3),
  pres numeric(6,3),
  temp numeric(5,3),
  depth numeric(6,3),
  cond_actual numeric(7,3),
  cond_specific numeric(7,3),
  salinity numeric(5,3),
  tds numeric(4,3),
  resistivity numeric(7,3),
  water_density numeric(4,3),
  calibration BOOLEAN
);

ALTER TABLE insitu
  OWNER TO postgres;
COMMENT ON TABLE insitu
  IS 'FGS Insitu Level Troll Suficial Network sensor data';
COMMENT ON COLUMN insitu.insitu_id IS 'Table Primary Key';
COMMENT ON COLUMN insitu.deploy_key IS 'Deploy Key, foreign key from deploy_info';
COMMENT ON COLUMN insitu.date_time IS 'Timestamp for observation (timestamp)';
COMMENT ON COLUMN insitu.elapsed_seconds IS 'Elapsed seconds since sensor was initialized (S)';
COMMENT ON COLUMN insitu.pres IS 'Pressure, PSI (PSI)';
COMMENT ON COLUMN insitu.temp IS 'Temperature, Celsius (C)';
COMMENT ON COLUMN insitu.depth IS 'Depth, Feet (ft)';
COMMENT ON COLUMN insitu.cond_actual IS 'Actual Conductivity, mirosiemens (µS)';
COMMENT ON COLUMN insitu.cond_specific IS 'Specific Conductivity, microsiemens (µS)';
COMMENT ON COLUMN insitu.salinity IS 'Salinity, practical salinity units (PSU)';
COMMENT ON COLUMN insitu.tds IS 'Total Dissolved Solids, parts per trillion (ppt)';
COMMENT ON COLUMN insitu.resistivity IS 'Resistivity, ohm-centimeter (Ω-cm)';
COMMENT ON COLUMN insitu.water_density IS 'Water Density, gallons per cubic centimeter (g/cm3)';
COMMENT ON COLUMN insitu.calibration IS 'Calibration Flag, boolean';
