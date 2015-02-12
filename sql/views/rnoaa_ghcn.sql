--View of noaa_ghcn that is oriented towards R users
--Why doesn't this work?
DROP VIEW rnoaa_ghcn;
CREATE OR REPLACE VIEW public.rnoaa_ghcn
    (
    site_name,
    date_time,
    val,
    var,
    dataset
    )
    
    AS
    
    SELECT * FROM (SELECT S.site_name, ghcn.latitude as lat, ghcn.longitude as lon, ghcn.date_time, ghcn.prcp as val, text 'precipitation' as var, text 'GHCN' as dataset FROM (noaa_ghcn AS ghcn INNER JOIN public.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, ghcn.latitude as lat, ghcn.longitude as lon, ghcn.date_time, ghcn.tmax as val, text 'maxtemp' as var, text 'GHCN' as dataset FROM (noaa_ghcn AS ghcn INNER JOIN public.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, ghcn.latitude as lat, ghcn.longitude as lon, ghcn.date_time, ghcn.tmin as val, text 'mintemp' as var, text 'GHCN' as dataset FROM (noaa_ghcn AS ghcn INNER JOIN public.sites AS S USING (site_id))) as ttable WHERE ttable.val IS NOT NULL
    ORDER BY date_time, site_name, var;