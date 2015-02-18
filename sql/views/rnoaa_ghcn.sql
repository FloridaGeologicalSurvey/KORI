--View that is oriented towards R users

CREATE OR REPLACE VIEW public.rgchn
    (
    site_name,
    date_time,
    val,
    var,
    dataset
    )
    
    AS
    
    SELECT S.site_name, ghcn.date_time, ghcn.prcp as val, text 'prcp' as var, text 'GHCN' as dataset FROM (extra.ghcn AS ghcn INNER JOIN extra.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, ghcn.date_time, ghcn.tmax as val, text 'maxtemp' as var, text 'GHCN' as dataset FROM (extra.ghcn AS ghcn INNER JOIN extra.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, ghcn.date_time, ghcn.tmin as val, text 'mintemp' as var, text 'GHCN' as dataset FROM (extra.ghcn AS ghcn INNER JOIN extra.sites AS S USING (site_id));