--creates an hourly view of the falmouth table, with values averaged by HOUR
--depends on the circavg FUNCTION

CREATE VIEW public.falmouth_daily
    (
    site_name,
    deploy_key,
    date_time,
    pres,
    temp,
    cond,
    aspd,
    avdir
    )
    
    AS
    
    SELECT 
        s.site_name site_name, temp.deploy_key deploy_key, temp.date_time date_time, round(avg(temp.pres),4) as pres, round(avg(temp.temp),4) as temp, round(avg(temp.cond),4) as cond, round(avg(temp.aspd),3) as aspd,
        CASE
            WHEN degrees(circavg(temp.avdir)) < 0 THEN degrees(circavg(temp.avdir)) + 360.0
            ELSE degrees(circavg(temp.avdir))
        END AS avdir
        FROM 
            ( SELECT 
            deploy_key, date_trunc('day',date_time) AS date_time, pres, temp, cond, aspd, radians(avdir) as avdir
            FROM falmouth f) AS temp INNER JOIN deploy_info di USING (deploy_key) INNER JOIN sites s USING (site_id)
            GROUP BY site_name, deploy_key, date_time ORDER BY date_time, site_name, deploy_key;