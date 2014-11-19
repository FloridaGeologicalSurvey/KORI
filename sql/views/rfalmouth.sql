--View that is oriented towards R users

CREATE OR REPLACE VIEW public.rfalmouth 
    (
    site_name,
    date_time,
    val,
    var,
    dataset
    )
    
    AS
    
    SELECT S.site_name, F.date_time, F.aspd as val, text 'aspd' as var, text 'Falmouth' as dataset FROM ((core.falmouth as F INNER JOIN core.deploy_info AS D USING (deploy_key)) INNER JOIN public.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, F.date_time, F.temp as val, text 'temp' as var, text 'Falmouth' as dataset FROM ((core.falmouth as F INNER JOIN core.deploy_info AS D USING (deploy_key)) INNER JOIN public.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, F.date_time, F.avdir as val, text 'avdir' as var, text 'Falmouth' as dataset FROM ((core.falmouth as F INNER JOIN core.deploy_info AS D USING (deploy_key)) INNER JOIN public.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, F.date_time, F.pres as val, text 'pres' as var, text 'Falmouth' as dataset FROM ((core.falmouth as F INNER JOIN core.deploy_info AS D USING (deploy_key)) INNER JOIN public.sites AS S USING (site_id)) UNION ALL
    SELECT S.site_name, F.date_time, F.cond as val, text 'cond' as var, text 'Falmouth' as dataset FROM ((core.falmouth as F INNER JOIN core.deploy_info AS D USING (deploy_key)) INNER JOIN public.sites AS S USING (site_id));
    