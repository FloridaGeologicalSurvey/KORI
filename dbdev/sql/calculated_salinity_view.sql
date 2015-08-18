DROP VIEW rfalmouth_zx;

CREATE VIEW rfalmouth_zx AS
	SELECT s.site_name, 
		f.date_time, 
		c.salt AS val, 
		'salinity'::text AS var, 
		'Falmouth'::text AS dataset
         FROM falmouth f
         JOIN deploy_info d USING (deploy_key)
         JOIN sites s USING (site_id)
         JOIN falmouth_salt c USING (falmouth_id)
         ORDER BY date_time, site_name;
         
         
	