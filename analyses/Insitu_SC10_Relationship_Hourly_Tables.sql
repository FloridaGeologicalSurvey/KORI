CREATE TABLE analysis.insitu_salt_hourly
    (
    site_name,
    date_time,
    elev_ft
    )
    AS
    SELECT
        nested.site_name, nested.date_time, round(avg(nested.elev_ft),4) elev_ft
    FROM
        (SELECT site_name, date_trunc('hour',date_time) AS date_time, elev_ft FROM rinsitu_wle) AS nested 
    GROUP BY site_name, date_time 
    ORDER BY date_time, site_name;

CREATE TABLE analysis.sc10_salt_hourly
    (
    date_time,
    salt
    )
    AS
    SELECT
        nested.date_time, round(avg(nested.val),4) salt
    FROM
        (SELECT date_trunc('hour',date_time) AS date_time, val FROM rfalmouth_salt WHERE site_name='Spring Creek 10 (Deep)' AND var = 'salt') AS nested 
    GROUP BY date_time 
    ORDER BY date_time;
    
ALTER TABLE analysis.insitu_salt_hourly ADD COLUMN salt numeric(5,2);
UPDATE analysis.insitu_salt_hourly i SET salt = (SELECT salt FROM analysis.sc10_salt_hourly s WHERE s.date_time = i.date_time);

COMMENT ON TABLE analysis.insitu_salt_hourly IS 'Average hourly insitu WLE measures matched against average salinity at SC10';
COMMENT ON TABLE analysis.sc10_salt_hourly IS 'Average hourly salinity reading at SC10';
