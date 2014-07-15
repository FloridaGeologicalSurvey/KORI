-- Table: deploy_info

-- DROP TABLE deploy_info;

CREATE TABLE deploy_info
(
  site_id VARCHAR, -- Site ID Name
  deploy_key integer NOT NULL DEFAULT nextval('deploy_key_seq'::regclass), -- Deploy Key. DB Primary Key.
  serial_number VARCHAR, -- Serial Number of Device
  start_dt timestamp without time zone, -- Start Timestamp of Deployment
  end_dt timestamp without time zone, -- End timestamp of deployment
  active boolean, -- Is device currently active?
  device_type VARCHAR,
  network VARCHAR,
  CONSTRAINT deploy_key PRIMARY KEY (deploy_key)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE deploy_info
  OWNER TO post_root;
COMMENT ON TABLE deploy_info
  IS 'Deployment table for FGS Hydrologic Sensor Network';
COMMENT ON COLUMN deploy_info.site_id IS 'Site ID Name';
COMMENT ON COLUMN deploy_info.deploy_key IS 'Deploy Key. DB Primary Key.';
COMMENT ON COLUMN deploy_info.serial_number IS 'Serial Number of Device';
COMMENT ON COLUMN deploy_info.start_dt IS 'Start Timestamp of Deployment';
COMMENT ON COLUMN deploy_info.end_dt IS 'End timestamp of deployment';
COMMENT ON COLUMN deploy_info.active IS 'Is device currently active?';