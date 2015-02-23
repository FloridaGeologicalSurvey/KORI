CREATE OR REPLACE VIEW public.rfalmouth_daily
    (
    site_name,
    date_time,
    val,
    var,
    dataset
    )
    
    AS
    
    SELECT site_name, date_time, aspd as val, text 'aspd' as var, text 'Falmouth Daily' as dataset FROM public.falmouth_daily UNION ALL
    SELECT site_name, date_time, temp as val, text 'temp' as var, text 'Falmouth Daily' as dataset FROM public.falmouth_daily UNION ALL
    SELECT site_name, date_time, avdir as val, text 'avdir' as var, text 'Falmouth Daily' as dataset FROM public.falmouth_daily UNION ALL
    SELECT site_name, date_time, pres as val, text 'pres' as var, text 'Falmouth Daily' as dataset FROM public.falmouth_daily UNION ALL
    SELECT site_name, date_time, cond as val, text 'cond' as var, text 'Falmouth Daily' as dataset FROM public.falmouth_daily;