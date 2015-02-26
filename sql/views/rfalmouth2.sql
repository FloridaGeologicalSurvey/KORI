CREATE OR REPLACE VIEW public.rfalmouth2 
    (
    site_name,
    date_time,
    val,
    var,
    dataset
    )
    
    AS
    
    SELECT S.site_name, D.deploy_key deploy_key, F.date_time, F.aspd as val, text 'aspd' as var FROM ((public.falmouth as F INNER JOIN public.deploy_info AS D USING (deploy_key) INNER JOIN public.sites AS S USING (site_id))) UNION ALL
    SELECT S.site_name, D.deploy_key deploy_key, F.date_time, F.temp as val, text 'temp' as var FROM ((public.falmouth as F INNER JOIN public.deploy_info AS D USING (deploy_key) INNER JOIN public.sites AS S USING (site_id))) UNION ALL
    SELECT S.site_name, D.deploy_key deploy_key, F.date_time, F.avdir as val, text 'avdir' as var FROM ((public.falmouth as F INNER JOIN public.deploy_info AS D USING (deploy_key) INNER JOIN public.sites AS S USING (site_id))) UNION ALL
    SELECT S.site_name, D.deploy_key deploy_key, F.date_time, F.pres as val, text 'pres' as var FROM ((public.falmouth as F INNER JOIN public.deploy_info AS D USING (deploy_key) INNER JOIN public.sites AS S USING (site_id))) UNION ALL
    SELECT S.site_name, D.deploy_key deploy_key, F.date_time, F.cond as val, text 'cond' as var FROM ((public.falmouth as F INNER JOIN public.deploy_info AS D USING (deploy_key) INNER JOIN public.sites AS S USING (site_id)));