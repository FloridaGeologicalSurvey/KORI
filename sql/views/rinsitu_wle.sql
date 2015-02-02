CREATE OR REPLACE VIEW rinsitu_wle AS
    SELECT s.site_name site_name, i.date_time date_time, w.wle val, 'wle'::text as var, 'Insitu'::text as dataset
        FROM (((insitu i INNER JOIN insitu_wle w USING (insitu_id)) INNER JOIN deploy_info d USING (deploy_key)) INNER JOIN sites s USING (site_id))
        ORDER BY date_time;
            
