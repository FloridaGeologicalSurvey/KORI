--creates a view that gives the average daily values for the falmouth tables
CREATE OR REPLACE VIEW falmouth_daily AS 
 SELECT temp.deploy_key, temp.date_time, avg(temp.pres) AS pres, avg(temp.temp) AS temp, avg(temp.cond) AS cond, avg(temp.aspd) AS aspd, 
        CASE
            WHEN degrees(circavg(temp.avdir)) < 0::double precision THEN degrees(circavg(temp.avdir)) + 360.0::double precision
            ELSE degrees(circavg(temp.avdir))
        END AS aspd
   FROM ( SELECT falmouth.deploy_key, date_trunc('day'::text, falmouth.date_time) AS date_time, falmouth.pres, falmouth.temp, falmouth.cond, falmouth.aspd, radians(falmouth.avdir::double precision) AS avdir
           FROM falmouth) temp
  GROUP BY temp.deploy_key, temp.date_time
  ORDER BY temp.date_time;