CREATE TABLE insitu_transducer
(
    site_id VARCHAR,
    station_id VARCHAR CONSTRAINT transducer_key PRIMARY KEY,
    deploy_key INTEGER REFERENCES deploy_info (deploy_key),
    toc_elev NUMERIC(6,3),
    trans_depth NUMERIC(6,3),
    adj_trans_depth NUMERIC(6,3),
    trans_elev NUMERIC(6,3),
    adj_trans_elev NUMERIC(6,3),
    
    vented BOOLEAN
);

ALTER TABLE insitu_transducer
    OWNER TO postgres;
COMMENT ON TABLE insitu_transducer
    IS 'Insitu transducer geometry. Values precomputed by the FGS. This table is used to calculate insitu.calculated_wle values using the following formula: insitu.calculated_wle = insitu_transducer.adj_trans_elev + ((insitu.pres*2.31)/0.999)';
COMMENT ON COLUMN insitu_transducer.site_id IS 'Station/Site name';
COMMENT ON COLUMN insitu_transducer.station_id IS 'Station ID, table primary KEY';
COMMENT ON COLUMN insitu_transducer.deploy_key IS 'Deploy Key, foreign key from deploy_info';
COMMENT ON COLUMN insitu_transducer.toc_elev IS 'Top of Casing elevation above MSL, NAVD88 (US ft)';
COMMENT ON COLUMN insitu_transducer.trans_depth IS 'Transducer depth below water level, NAVD88 (US ft)';
COMMENT ON COLUMN insitu_transducer.adj_trans_depth IS 'Adjusted transducer depth, accounts for transducer recess in sensor body. NAVD88 (US ft).';
COMMENT ON COLUMN insitu_transducer.trans_elev IS 'Transducer elevation above MSL, NAVD88 (US ft)';
COMMENT ON COLUMN insitu_transducer.adj_trans_elev IS 'Adjusted transducer elevation, accounts for transducer recess in sensor body. NAVD88 (US ft). This is the value used to calculate insitu.calculated_wle';
COMMENT ON COLUMN insitu_transducer.vented IS 'Sensor vented? boolean';

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Sullivan',         --site_id
    'SUL',              --station_id
    18,                 --deploy_key
    10.015,             --toc_elev
    5.917,              --trans_depth
    5.854,              --adj_trans_depth
    4.098,              --trans_elev
    4.161,              --adj_trans_elev,
    FALSE);             --vented

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Sullivan',         --site_id
    'SUL2',             --station_id
    19,                 --deploy_key
    10.015,             --toc_elev
    5.833,              --trans_depth
    5.833,               --adj_trans_depth
    4.181,              --trans_elev
    4.182,              --adj_trans_elev,
    FALSE);             --vented 

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Tobacco',          --site_id
    'TS1',              --station_id
    24,                 --deploy_key
    7.62,               --toc_elev
    5.917,              --trans_depth
    5.854,              --adj_trans_depth
    1.703,              --trans_elev
    1.766,              --adj_trans_elev,
    FALSE);             --vented   

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Tobacco',          --site_id
    'TS2',              --station_id
    25,                 --deploy_key
    7.62,               --toc_elev
    5.917,              --trans_depth
    5.854,              --adj_trans_depth
    1.703,              --trans_elev
    1.766,              --adj_trans_elev,
    FALSE);             --vented

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Revell',           --site_id
    'RS1',              --station_id
    20,                 --deploy_key
    8.24,               --toc_elev
    5.917,              --trans_depth
    5.854,              --adj_trans_depth
    2.323,              --trans_elev
    2.386,              --adj_trans_elev,
    FALSE);             --vented      

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Revell',           --site_id
    'RS2',              --station_id
    21,                 --deploy_key
    8.11,               --toc_elev
    5.870,              --trans_depth
    5.807,              --adj_trans_depth
    2.240,              --trans_elev
    2.303,              --adj_trans_elev,
    FALSE);             --vented  

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Revell',           --site_id
    'RS3',              --station_id
    22,                 --deploy_key
    8.11,               --toc_elev
    5.813,              --trans_depth
    5.813,              --adj_trans_depth
    2.297,              --trans_elev
    2.297,              --adj_trans_elev,
    FALSE);             --vented

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Revell',           --site_id
    'RS4',              --station_id
    23,                 --deploy_key
    8.11,               --toc_elev
    4.870,              --trans_depth
    4.870,              --adj_trans_depth
    3.240,              --trans_elev
    3.240,              --adj_trans_elev,
    FALSE);             --vented     

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Turner',           --site_id
    'TUR1',             --station_id
    26,                 --deploy_key
    9.288,              --toc_elev
    5.917,              --trans_depth
    5.854,              --adj_trans_depth
    3.371,              --trans_elev
    3.434,              --adj_trans_elev,
    FALSE);             --vented

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Turner',           --site_id
    'TUR2',             --station_id
    27,                 --deploy_key
    9.288,              --toc_elev
    5.927,              --trans_depth
    5.864,              --adj_trans_depth
    3.361,              --trans_elev
    3.424,              --adj_trans_elev,
    FALSE);             --vented
    
INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Turner',           --site_id
    'TUR3',             --station_id
    28,                 --deploy_key
    9.288,              --toc_elev
    6.260,              --trans_depth
    6.197,              --adj_trans_depth
    3.028,              --trans_elev
    3.091,              --adj_trans_elev,
    FALSE);             --vented

INSERT INTO insitu_transducer (    
    site_id,
    station_id,
    deploy_key,
    toc_elev,
    trans_depth,
    adj_trans_depth,
    trans_elev,
    adj_trans_elev,
    vented) VALUES (
    'Lost Creek',        --site_id
    'LC2',               --station_id
    29,                  --deploy_key
    18.43,               --toc_elev
    18.083,              --trans_depth
    18.082,              --adj_trans_depth
    0.347,               --trans_elev
    0.410,               --adj_trans_elev,
    FALSE);              --vented  