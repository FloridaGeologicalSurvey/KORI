CREATE TABLE falmouth
(
  falmouth_id SERIAL CONSTRAINT falmouth_key PRIMARY KEY, 
  deploy_key INTEGER REFERENCES deploy_info (deploy_key), 
  date_time timestamp with time zone, 
  avn NUMERIC(5, 2),
  ave NUMERIC(5,2),
  aspd NUMERIC(6,3),
  avdir NUMERIC(6,3) CONSTRAINT on_compass_min CHECK(avdir >= 0) CONSTRAINT on_compass_max CHECK(avdir <= 360),
  atlt NUMERIC(4,2),
  cond NUMERIC(6,4),
  temp NUMERIC(6,4),
  pres NUMERIC(6,4),
  hdng NUMERIC(5,2),
  batt NUMERIC(4,2),
  vx NUMERIC(5,2),
  vy NUMERIC(5,2),
  tx NUMERIC(4,2),
  ty NUMERIC(4,2),
  hx NUMERIC(5,4),
  hy NUMERIC(5,4),
  hz NUMERIC(5,4),
  vn NUMERIC(5,2),
  ve NUMERIC(5,2),
  stemp NUMERIC(4,2),
  sv1 NUMERIC(8,2),
  sv2 NUMERIC(8,4),
  vab NUMERIC(5,2),
  vcd NUMERIC(5,2),
  vef NUMERIC(5,2),
  vgh NUMERIC(5,2),
  salt NUMERIC(6,4),
  calibration BOOLEAN,
  CONSTRAINT unique_observation UNIQUE(date_time, deploy_key)
  );
  
ALTER TABLE falmouth
  OWNER TO post_root;
COMMENT ON TABLE falmouth
  IS 'FGS Deep Network Falmouth 2D-ACM Deep Network sensor data';
COMMENT ON COLUMN falmouth.falmouth_id IS 'table PK';
COMMENT ON COLUMN falmouth.deploy_key IS 'Deploy Key, foreign key from deploy_info table';
COMMENT ON COLUMN falmouth.date_time IS 'Timestamp of observation, UTC';
COMMENT ON COLUMN falmouth.avn IS 'Vector averaged north current velocity in cm/sec';
COMMENT ON COLUMN falmouth.ave IS 'Vector averaged east current velocity in cm/sec';
COMMENT ON COLUMN falmouth.aspd IS 'Calculated vector averaged current speed in cm/sec';
COMMENT ON COLUMN falmouth.avdir IS 'Calculated average direction in degrees';
COMMENT ON COLUMN falmouth.atlt IS 'Vector averaged tilt in degrees';
COMMENT ON COLUMN falmouth.cond IS 'conductivity in mmho/cm from CTD';
COMMENT ON COLUMN falmouth.temp IS 'Water temperature in C from CTD';
COMMENT ON COLUMN falmouth.pres IS 'Water pressure in dbars from CTD';
COMMENT ON COLUMN falmouth.hdng IS 'instantaneous instrument heading in degrees';
COMMENT ON COLUMN falmouth.batt IS 'Battery voltage in volts';
COMMENT ON COLUMN falmouth.vx IS 'Instantaneous X current velocity in cm/sec';
COMMENT ON COLUMN falmouth.vy IS 'Instantaneous Y current velocity in cm/sec';
COMMENT ON COLUMN falmouth.tx IS 'Instantaneous Tilt X in degrees';
COMMENT ON COLUMN falmouth.ty IS 'Instantaneous Tilt Y in degrees';
COMMENT ON COLUMN falmouth.hx IS 'Instantaneous Compass X';
COMMENT ON COLUMN falmouth.hy IS 'Instantaneous Compass Y';
COMMENT ON COLUMN falmouth.hz IS 'Instantaneous Compass Z';
COMMENT ON COLUMN falmouth.vn IS 'Instantaneous north current velocity in cm/sec';
COMMENT ON COLUMN falmouth.ve IS 'Instantaneous east current velocity in cm/sec';
COMMENT ON COLUMN falmouth.stemp IS 'Sea temperature in C';
COMMENT ON COLUMN falmouth.sv1 IS 'Calculated sound velocity in water cm/s';
COMMENT ON COLUMN falmouth.sv2 IS 'Calculated sound velocity in water m/s';
COMMENT ON COLUMN falmouth.vab IS 'Unknown';
COMMENT ON COLUMN falmouth.vcd IS 'Unknown';
COMMENT ON COLUMN falmouth.vef IS 'Unknown';
COMMENT ON COLUMN falmouth.vgh IS 'Unknown';
COMMENT ON COLUMN falmouth.salt IS 'salinity in Practical Salinity Units (PSU)';
COMMENT ON COLUMN falmouth.calibration IS 'In calibration period or out of calibration period?';

  
