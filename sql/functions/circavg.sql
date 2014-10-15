--Function to find the circular mean
--Necessary for averaging falmouth.avdir values
--blatantly stolen from http://stackoverflow.com/questions/10225357/custom-postgresql-aggregate-for-circular-average

CREATE OR REPLACE FUNCTION f_circavg (float[], float)
  RETURNS float[] AS
$body$
SELECT ARRAY[$1[1] + sin($2), $1[2] + cos($2)];
$body$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION f_circavg_final (float[])
  RETURNS float AS
$body$
SELECT degrees(atan2($1[1], $1[2]));
$body$ LANGUAGE sql;

CREATE AGGREGATE circavg (float)
( sfunc     = f_circavg
 ,stype     = float[]
 ,finalfunc = f_circavg_final
 ,initcond  = '{0,0}'
);