--creates an hourly view of the falmouth table, with values averaged by HOUR
--depends on the circavg FUNCTION

CREATE OR REPLACE VIEW public.hourly_falmouth
    (
    deploy_key,
    date_time,
    avdir,
    cond,
    pres,
    temp,
    aspd
    )
    
    AS
    
    SELECT 
        deploy_key, date_time, avg(pres) as pres, avg(temp) as temp, avg(cond) as cond, avg(aspd) as aspd,
        CASE
            WHEN degrees(circavg(avdir)) < 0 THEN degrees(circavg(avdir)) + 360.0
            ELSE degrees(circavg(avdir))
        END
        AS avdir
        FROM 
            (SELECT 
            deploy_key, date_trunc('hour',date_time) AS date_time, pres, temp, cond, aspd, radians(avdir) as avdir
            FROM falmouth) 
            AS temp 
    GROUP BY deploy_key, date_time;