CREATE TABLE core.insitu
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
  zpo numeric(6,3),
  calibration BOOLEAN,
  CONSTRAINT unique_observation_insitu UNIQUE(deploy_key, date_time)
);

ALTER TABLE core.insitu
  OWNER TO postgres;
COMMENT ON TABLE insitu
  IS 'FGS Insitu Level Troll Suficial Network sensor data';
COMMENT ON COLUMN core.insitu.insitu_id IS 'Table Primary Key';
COMMENT ON COLUMN core.insitu.deploy_key IS 'Deploy Key, foreign key from deploy_info';
COMMENT ON COLUMN core.insitu.date_time IS 'Timestamp for observation (timestamp)';
COMMENT ON COLUMN core.insitu.elapsed_seconds IS 'Elapsed seconds since sensor was initialized (S)';
COMMENT ON COLUMN core.insitu.pres IS 'Pressure, PSI (PSI)';
COMMENT ON COLUMN core.insitu.temp IS 'Temperature, Celsius (C)';
COMMENT ON COLUMN core.insitu.depth IS 'Depth, Feet (ft). Note this value may be incorrect if ZPO is non-zero';
COMMENT ON COLUMN core.insitu.cond_actual IS 'Actual Conductivity, mirosiemens (µS)';
COMMENT ON COLUMN core.insitu.cond_specific IS 'Specific Conductivity, microsiemens (µS)';
COMMENT ON COLUMN core.insitu.salinity IS 'Salinity, practical salinity units (PSU)';
COMMENT ON COLUMN core.insitu.tds IS 'Total Dissolved Solids, parts per trillion (ppt)';
COMMENT ON COLUMN core.insitu.resistivity IS 'Resistivity, ohm-centimeter (Ω-cm)';
COMMENT ON COLUMN core.insitu.water_density IS 'Water Density, gallons per cubic centimeter (g/cm3)';
COMMENT ON COLUMN core.insitu.zpo IS 'Zero Pressure Offset (PSI). ZPO should be added to the pres column to get the true pressure reading at the transducer';
COMMENT ON COLUMN core.insitu.calibration IS 'Calibration Flag, boolean';

/*
CREATE TABLE insitu_wle
(
    insitu_id integer REFERENCES insitu (insitu_id),
    wle NUMERIC(6,3),
    PRIMARY KEY (insitu_id)
);

ALTER TABLE insitu_wle
    OWNER TO postgres;
COMMENT ON TABLE insitu_wle
    IS 'Insitu calculated Water Level Elevations';
COMMENT ON COLUMN insitu_wle.insitu_id IS 'Primary Key, foreign key from the insitu table';
COMMENT ON COLUMN insitu_wle.wle IS 'Calculated water level elevation, NAVD88 (US ft)';
*/