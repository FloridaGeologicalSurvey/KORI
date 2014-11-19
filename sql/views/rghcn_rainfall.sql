--View that is oriented towards R users

CREATE OR REPLACE VIEW public.rghcn_rainfall
    (
    site_name,
    date_time,
    val,
    var,
    dataset
    )
    
    AS
    
    SELECT S.site_name, ghcn.date_time, ghcn.prcp as val, text 'precipitation' as var, text 'GHCN' as dataset FROM (extra.noaa_ghcn AS ghcn INNER JOIN public.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, ghcn.date_time, ghcn.tmax as val, text 'maxtemp' as var, text 'GHCN' as dataset FROM (extra.noaa_ghcn AS ghcn INNER JOIN public.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, ghcn.date_time, ghcn.tmin as val, text 'mintemp' as var, text 'GHCN' as dataset FROM (extra.noaa_ghcn AS ghcn INNER JOIN public.sites AS S USING (site_id));