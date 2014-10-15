--View that is oriented towards R users

CREATE OR REPLACE VIEW public.rnoaa_coops
    (
    site_name,
    date_time,
    val,
    var,
    dataset
    )
    
    AS
    
    SELECT S.site_name, COOPS.date_time, COOPS.wle as val, text 'tidal_wle' as var, text 'COOPS' as dataset FROM (noaa_coops AS COOPS INNER JOIN sites AS S USING (site_id))