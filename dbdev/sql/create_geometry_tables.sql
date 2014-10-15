CREATE TABLE benchmarks 
(
    benchmark_id VARCHAR CONSTRAINT benchmark_key PRIMARY KEY,
    site_id VARCHAR,
    easting NUMERIC(9,3),
    easting_error NUMERIC(4,3),
    northing NUMERIC(10,3),
    northing_error NUMERIC(4,3),
    orthometric_height NUMERIC(6,3),
    height_error NUMERIC(5,2),
    method VARCHAR,
    survey_date DATE,
    projection VARCHAR,
    xydatum VARCHAR,
    zdatum VARCHAR,
    latitude NUMERIC(11,8),
    longitude NUMERIC(11,8),
    active BOOLEAN,
    elevation_ft NUMERIC(5,2)
);

ALTER TABLE benchmarks
    OWNER TO postgres;
COMMENT ON TABLE benchmarks
    IS 'Benchmark data. Used to calculate top of casing and transducer depth for insitu data';
COMMENT ON COLUMN benchmarks.benchmark_id IS 'Benchmark ID, primary key';
COMMENT ON COLUMN benchmarks.site_id IS 'Site ID';
COMMENT ON COLUMN benchmarks.easting IS 'Easting (Meters)';
COMMENT ON COLUMN benchmarks.easting_error IS '95% error for Easting';
COMMENT ON COLUMN benchmarks.northing IS 'Northing (Meters)';
COMMENT ON COLUMN benchmarks.northing_error IS '95% Error for Northing';
COMMENT ON COLUMN benchmarks.orthometric_height IS 'Orthometric Height (Meters)';
COMMENT ON COLUMN benchmarks.height_error IS '95% Error for Orthometric Height';
COMMENT ON COLUMN benchmarks.method IS 'Method of Survey';
COMMENT ON COLUMN benchmarks.survey_date IS 'Date of Survey';
COMMENT ON COLUMN benchmarks.projection IS 'Survey Projection';
COMMENT ON COLUMN benchmarks.xydatum IS 'Survey XY Datum';
COMMENT ON COLUMN benchmarks.zdatum IS 'Survey Z Datum';
COMMENT ON COLUMN benchmarks.latitude IS 'Calculated Latitude, NAD83';
COMMENT ON COLUMN benchmarks.longitude IS 'Calculated Longitude, NAD83';
COMMENT ON COLUMN benchmarks.active IS 'Benchmark currently active, boolean';
COMMENT ON COLUMN benchmarks.elevation_ft IS 'Calculated elevation in feet, NAVD88';

CREATE OR REPLACE FUNCTION benchmarks_insert() RETURNS trigger AS '
     BEGIN
         NEW.elevation_ft := NEW.orthometric_height * 3.28084;
         RETURN NEW;
     END;
 ' LANGUAGE plpgsql;
CREATE TRIGGER benchmarks_insert BEFORE INSERT OR UPDATE ON benchmarks FOR EACH ROW EXECUTE PROCEDURE benchmarks_insert();

INSERT INTO benchmarks (
    benchmark_id, 
    site_id, 
    easting, 
    easting_error, 
    northing, 
    northing_error,
    orthometric_height, 
    height_error, 
    method, 
    survey_date, 
    projection, 
    xydatum, 
    zdatum, 
    latitude, 
    longitude, 
    active)
    VALUES (
    'TSINK', --benchmark_id
    'Tobacco', --site_name
    758354.020, --EASTING
    0.055, --EASTING error
    3336273.195, --NORTHING
    0.051, --NORTHING ERROR
    4.317, --orthometric height
    0.061, --height error
    'GPS SURVEY', --method
    '2009-01-13', --date
    'UTM ZONE 16N', --xy projection
    'NAD83', --xy datum
    'NAVD88', --z datum
    30.13041767, --latitude
    -84.31827933, --longitude
    TRUE); --active
    
INSERT INTO benchmarks (
    benchmark_id, 
    site_id, 
    easting, 
    easting_error, 
    northing, 
    northing_error,
    orthometric_height, 
    height_error, 
    method, 
    survey_date, 
    projection, 
    xydatum, 
    zdatum, 
    latitude, 
    longitude, 
    active) VALUES (
    'RS01',
    'Revell',
    757174.705,
    0.033,
    3342040.467,
    0.035,
    5.695,
    0.033,
    'GPS SURVEY',
    '2009-01-06',
    'UTM ZONE 16N',
    'NAD83',
    'NAVD88',
    30.18265648,
    -84.32910782,
    TRUE);

INSERT INTO benchmarks (
    benchmark_id, 
    site_id, 
    easting, 
    easting_error, 
    northing, 
    northing_error,
    orthometric_height, 
    height_error, 
    method, 
    survey_date, 
    projection, 
    xydatum, 
    zdatum, 
    latitude, 
    longitude, 
    active)
    VALUES (
    'LC01', --benchmark_id
    'Lost Creek 1', --site_name
    750966.480, --EASTING
    0.024, --EASTING error
    3340263.903, --NORTHING
    0.020, --NORTHING error
    5.493, --orthometric height
    0.033, --height error
    'GPS SURVEY', --method
    '2009-01-13', --date
    'UTM ZONE 16N', --xy projection
    'NAD83', --xy datum
    'NAVD88', --z datum
    30.16793753, --latitude
    -84.39394864, --longitude
    TRUE); --active




CREATE TABLE reference_surveys
(
    benchmark_id VARCHAR REFERENCES benchmarks (benchmark_id),
    survey_id VARCHAR CONSTRAINT survey_key PRIMARY KEY,
    survey_type VARCHAR,
    S1BS_TO_BM NUMERIC(5,2),
    S1FS NUMERIC(5,2),
    S2BS_TO_S1 NUMERIC(5,2),
    S2FS NUMERIC(5,2),
    S3BS_TO_S2 NUMERIC(5,2),
    S3FS NUMERIC(5,2)
);
ALTER TABLE reference_surveys
    OWNER TO postgres;
COMMENT ON TABLE reference_surveys
    is 'Reference survey data. Used to calculate benchmark, top of casing, and transducer elevations for insitu data';
COMMENT ON COLUMN reference_surveys.survey_id IS 'Survey ID, primary key';
COMMENT ON COLUMN reference_surveys.survey_type IS 'Type of survey, REFERENCE or BACKUP';
COMMENT ON COLUMN reference_surveys.S1BS_TO_BM IS 'Shot 1 backsight to Benchmark, ft';
COMMENT ON COLUMN reference_surveys.S1FS IS 'Shot 1 fowardsight, ft';
COMMENT ON COLUMN reference_surveys.S2BS_TO_S1 IS 'Shot 2 backsight to Shot 1, ft';
COMMENT ON COLUMN reference_surveys.S2FS IS 'Shot 2 fowardsight, ft';
COMMENT ON COLUMN reference_surveys.S3BS_TO_S2 IS 'Shot 3 backsight to Shot 2, ft';
COMMENT ON COLUMN reference_surveys.S3FS IS 'Shot 3 fowardsight, ft';

INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'TSINK',        --benchmark_id
    'TSINK-RS1',    --survey_id,
    'REFERENCE',     --survey_type,
    0.43,           --S1BS_TO_BM,
    6.73,           --S1FS,
    2.9,            --S2BS_TO_S1,
    6.2,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS    
    
 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'TSINK',        --benchmark_id
    'TSINK-RS2',    --survey_id,
    'REFERENCE',     --survey_type,
    0.43,           --S1BS_TO_BM,
    6.73,           --S1FS,
    2.9,            --S2BS_TO_S1,
    6.22,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS

 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'TSINK',        --benchmark_id
    'TSINK-RS3',    --survey_id,
    'REFERENCE',     --survey_type,
    0.43,           --S1BS_TO_BM,
    6.73,           --S1FS,
    2.9,            --S2BS_TO_S1,
    6.24,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS

 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'TSINK',        --benchmark_id
    'TSINK-BU1',    --survey_id,
    'BACKUP',     --survey_type,
    0.43,           --S1BS_TO_BM,
    6.73,           --S1FS,
    2.9,            --S2BS_TO_S1,
    5.46,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS

 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'RS01',        --benchmark_id
    'RS01-RS1',    --survey_id,
    'REFERENCE',     --survey_type,
    0.4,           --S1BS_TO_BM,
    14.51,           --S1FS,
    NULL,            --S2BS_TO_S1,
    NULL,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS   
 
 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'RS01',        --benchmark_id
    'RS01-RS2',    --survey_id,
    'REFERENCE',     --survey_type,
    0.4,           --S1BS_TO_BM,
    14.50,           --S1FS,
    NULL,            --S2BS_TO_S1,
    NULL,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS   

 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'RS01',        --benchmark_id
    'RS01-RS3',    --survey_id,
    'REFERENCE',     --survey_type,
    0.4,           --S1BS_TO_BM,
    14.51,           --S1FS,
    NULL,            --S2BS_TO_S1,
    NULL,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS

 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'RS01',        --benchmark_id
    'RS01-BU1',    --survey_id,
    'BACKUP',     --survey_type,
    0.4,           --S1BS_TO_BM,
    13.64,           --S1FS,
    NULL,            --S2BS_TO_S1,
    NULL,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS

 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'LC01',        --benchmark_id
    'LC01-RS1',    --survey_id,
    'REFERENCE',     --survey_type,
    1.93,           --S1BS_TO_BM,
    15.0,           --S1FS,
    NULL,            --S2BS_TO_S1,
    NULL,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS

 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'LC01',        --benchmark_id
    'LC01-RS2',    --survey_id,
    'REFERENCE',     --survey_type,
    1.93,           --S1BS_TO_BM,
    15.03,           --S1FS,
    NULL,            --S2BS_TO_S1,
    NULL,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS 

 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'LC01',        --benchmark_id
    'LC01-RS3',    --survey_id,
    'REFERENCE',     --survey_type,
    1.93,           --S1BS_TO_BM,
    15.03,           --S1FS,
    NULL,            --S2BS_TO_S1,
    NULL,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS
    
 INSERT INTO reference_surveys (
    benchmark_id,
    survey_id,
    survey_type,
    S1BS_TO_BM,
    S1FS,
    S2BS_TO_S1,
    S2FS,
    S3BS_TO_S2,
    S3FS) VALUES (
    'LC01',        --benchmark_id
    'LC01-BU1',    --survey_id,
    'BACKUP',     --survey_type,
    1.93,           --S1BS_TO_BM,
    14.2,           --S1FS,
    NULL,            --S2BS_TO_S1,
    NULL,            --S2FS,
    NULL,           --S3BS_TO_S2,
    NULL);          --S3FS  

CREATE TABLE measurement_abbreviations
(
    abbreviation VARCHAR CONSTRAINT abbreviations_key PRIMARY KEY,
    description VARCHAR
);

ALTER TABLE measurement_abbreviations
    OWNER TO postgres;
COMMENT ON TABLE measurement_abbreviations
    IS 'Lookup table for insitu casing measurement abbreviations';
COMMENT ON COLUMN measurement_abbreviations.abbreviation IS 'Abbreviation, primary key';
COMMENT ON COLUMN measurement_abbreviations.description IS 'Full description';

INSERT INTO measurement_abbreviations values ('TBS','Top of Black Swath');
INSERT INTO measurement_abbreviations values ('TOC','Top of Well Casing');
INSERT INTO measurement_abbreviations values ('TOD','Top of Dock or Platform');
INSERT INTO measurement_abbreviations values ('SWL','Surface Water Elevation');
INSERT INTO measurement_abbreviations values ('TRED','Top of Reducer');
INSERT INTO measurement_abbreviations values ('BOWI', 'Bottom of Well, INSIDE');
INSERT INTO measurement_abbreviations values ('BOWO', 'Bottom of Well, OUTSIDE');
INSERT INTO measurement_abbreviations values ('TRANS','Bottom of Transducer');
INSERT INTO measurement_abbreviations values ('SW','Stilling Well');
INSERT INTO measurement_abbreviations values ('TOB','Top of Box');
INSERT INTO measurement_abbreviations values ('WTSurf','Water Table Surface');
INSERT INTO measurement_abbreviations values ('SWK','SW Knotch');
    
CREATE TABLE casing_data
(
    cd_id SERIAL CONSTRAINT cd_key PRIMARY KEY, 
    benchmark_id VARCHAR REFERENCES benchmarks (benchmark_id),
    mfrom VARCHAR REFERENCES measurement_abbreviations (abbreviation),
    mto VARCHAR REFERENCES measurement_abbreviations (abbreviation),
    feet INTEGER,
    inches INTEGER,
    eighths INTEGER,
    sixteenths INTEGER,
    mprecision NUMERIC(5,4),
    calculated_ft NUMERIC(6,4)
    
    
);
ALTER TABLE casing_data
    OWNER TO postgres;
COMMENT ON TABLE reference_surveys
    is 'Reference survey data. Used to calculate benchmark, top of casing, and transducer elevations for insitu data';
COMMENT ON COLUMN casing_data.cd_id IS 'Table Primary Key';
COMMENT ON COLUMN casing_data.benchmark_id IS 'Foreign key from benchmarks table';
COMMENT ON COLUMN casing_data.mfrom IS 'Measurement From, foreign key from measurement_abbreviations table';
COMMENT ON COLUMN casing_data.mto IS 'Measurement To, foreign key from measurements_abbreviations';
COMMENT ON COLUMN casing_data.feet IS 'Measurement, total feet';
COMMENT ON COLUMN casing_data.inches IS 'Measurement, total inches';
COMMENT ON COLUMN casing_data.eighths IS 'Measurement, total 1/8 inches';
COMMENT ON COLUMN casing_data.sixteenths IS 'Measurement, total 1/16 inches';
COMMENT ON COLUMN casing_data.mprecision IS 'Precision of measurement, inches';
COMMENT ON COLUMN casing_data.calculated_ft IS 'Calculated total measurement, in decimal feet';

CREATE OR REPLACE FUNCTION casing_data_insert() RETURNS trigger AS '
     BEGIN
         NEW.calculated_ft := (CAST(NEW.feet AS FLOAT) + (CAST(NEW.inches AS FLOAT)/12) + ((CAST(NEW.eighths AS FLOAT)/8)/12) + ((CAST(NEW.sixteenths AS FLOAT)/16)/12));
         RETURN NEW;
     END;
 ' LANGUAGE plpgsql;
CREATE TRIGGER casing_data_insert BEFORE INSERT OR UPDATE ON casing_data FOR EACH ROW EXECUTE PROCEDURE casing_data_insert();


INSERT INTO casing_data ( 
    benchmark_id, 
    mfrom,
    mto, 
    feet, 
    inches, 
    eighths,
    sixteenths,
    mprecision) VALUES (
    'TSINK',            --benchmark_id, 
    'TRED',             --mfrom,
    'BOWO',             --mto, 
    6,                  --feet, 
    1,                  --inches, 
    5,                  --eighths,
    0,                  --sixteenths,
    0.0104             --mprecision, 
  );
  
INSERT INTO casing_data ( 
    benchmark_id, 
    mfrom,
    mto, 
    feet, 
    inches, 
    eighths,
    sixteenths,
    mprecision) VALUES (
    'TSINK',            --benchmark_id, 
    'TRED',             --mfrom,
    'BOWI',             --mto, 
    6,                  --feet, 
    1,                  --inches, 
    3,                  --eighths,
    0,                  --sixteenths,
    0.0104             --mprecision, 
  );  

INSERT INTO casing_data ( 
    benchmark_id, 
    mfrom,
    mto, 
    feet, 
    inches, 
    eighths,
    sixteenths,
    mprecision) VALUES (
    'TSINK',            --benchmark_id, 
    'TBS',             --mfrom,
    'TRED',             --mto, 
    0,                  --feet, 
    1,                  --inches, 
    0,                  --eighths,
    7,                  --sixteenths,
    0.0104             --mprecision, 
  );  
  
INSERT INTO casing_data ( 
    benchmark_id, 
    mfrom,
    mto, 
    feet, 
    inches, 
    eighths,
    sixteenths,
    mprecision) VALUES (
    'TSINK',            --benchmark_id, 
    'TBS',             --mfrom,
    'TRANS',             --mto, 
    5,                  --feet, 
    11,                  --inches, 
    0,                  --eighths,
    0,                  --sixteenths,
    0.0833             --mprecision, 
  ); 

INSERT INTO casing_data ( 
    benchmark_id, 
    mfrom,
    mto, 
    feet, 
    inches, 
    eighths,
    sixteenths,
    mprecision) VALUES (
    'TSINK',            --benchmark_id, 
    'TBS',             --mfrom,
    'SWK',             --mto, 
    3,                  --feet, 
    0,                  --inches, 
    0,                  --eighths,
    15,                  --sixteenths,
    0.0052             --mprecision, 
  ); 