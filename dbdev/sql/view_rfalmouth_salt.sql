CREATE OR REPLACE VIEW rfalmouth_salt AS 
     (((((SELECT s.site_name, f.date_time, f.aspd AS val, 'aspd'::text AS var, 'Falmouth'::text AS dataset
            FROM falmouth f
                JOIN deploy_info d USING (deploy_key)
                JOIN sites s USING (site_id)
        UNION ALL 
        SELECT s.site_name, f.date_time, f.temp AS val, 'temp'::text AS var, 'Falmouth'::text AS dataset
            FROM falmouth f
              JOIN deploy_info d USING (deploy_key)
              JOIN sites s USING (site_id))
        UNION ALL 
        SELECT s.site_name, f.date_time, f.avdir AS val, 'avdir'::text AS var, 'Falmouth'::text AS dataset
            FROM falmouth f
              JOIN deploy_info d USING (deploy_key)
              JOIN sites s USING (site_id))
        UNION ALL 
        SELECT s.site_name, f.date_time, f.pres AS val, 'pres'::text AS var, 'Falmouth'::text AS dataset
            FROM falmouth f
            JOIN deploy_info d USING (deploy_key)
            JOIN sites s USING (site_id))
        UNION ALL 
        SELECT s.site_name, f.date_time, f.cond AS val, 'cond'::text AS var, 'Falmouth'::text AS dataset
            FROM falmouth f
                JOIN deploy_info d USING (deploy_key)
                JOIN sites s USING (site_id))
        UNION ALL 
        SELECT s.site_name, f.date_time, f.salt AS val, 'salt'::text AS var, 'Falmouth'::text AS dataset
            FROM falmouth f
                JOIN deploy_info d USING (deploy_key)
                JOIN sites s USING (site_id)
            WHERE f.salt IS NOT NULL)
        ORDER BY date_time, var, site_name;

ALTER TABLE rfalmouth_salt;
  OWNER TO postgres;
GRANT ALL ON TABLE rfalmouth_salt TO postgres;
GRANT SELECT ON TABLE rfalmouth_salt TO wkp_user;