-- Table: deploy_info

-- DROP TABLE deploy_info;


CREATE TABLE deploy_info (
    site_id integer REFERENCES sites (site_id),
    deploy_key SERIAL CONSTRAINT deploy_key PRIMARY KEY,
    serial_number character varying,
    start_dt timestamp with time zone,
    end_dt timestamp with time zone,
    active boolean,
    device_type character varying,
    network character varying
);


ALTER TABLE deploy_info
  OWNER TO post_root;
COMMENT ON TABLE deploy_info
  IS 'Deployment table for FGS Hydrologic Sensor Network';
COMMENT ON COLUMN deploy_info.site_id IS 'Site ID, foreign key from sites table.';
COMMENT ON COLUMN deploy_info.deploy_key IS 'Deploy Key. DB Primary Key.';
COMMENT ON COLUMN deploy_info.serial_number IS 'Serial Number of Device';
COMMENT ON COLUMN deploy_info.start_dt IS 'Start Timestamp of Deployment';
COMMENT ON COLUMN deploy_info.end_dt IS 'End timestamp of deployment';
COMMENT ON COLUMN deploy_info.active IS 'Is device currently active?';
COMMENT ON COLUMN deploy_info.device_type IS 'Model of Device';
COMMENT ON COLUMN deploy_info.network IS 'FGS Sensor Network';

/* COPY For psgl STDIN
COPY deploy_info (site_id, deploy_key, serial_number, start_dt, end_dt, active, device_type, network) FROM stdin;
2	1	1665-2D	2006-05-01 17:15:00+00	2013-12-02 18:00:01+00	f	Falmouth 2D-ACM	Deep
5	2	1789-2D	2006-05-01 17:30:00+00	2008-05-14 18:45:00+00	f	Falmouth 2D-ACM	Deep
5	3	1891-2D	2008-05-18 17:45:00+00	2013-12-02 17:00:01+00	f	Falmouth 2D-ACM	Deep
3	4	1687-2D	2006-05-01 16:00:00+00	2013-12-02 18:00:00+00	f	Falmouth 2D-ACM	Deep
4	5	1688-2D	2006-05-01 15:45:00+00	2013-01-10 15:15:00+00	f	Falmouth 2D-ACM	Deep
1	6	1889-2D	2007-12-17 17:45:00+00	2009-07-08 18:15:00+00	f	Falmouth 2D-ACM	Deep
1	7	1788-2D	2011-07-12 16:06:00+00	2013-12-02 18:00:01+00	f	Falmouth 2D-ACM	Deep
1	8	1678-2D	2006-05-01 17:15:00+00	2007-07-05 18:00:00+00	f	Falmouth 2D-ACM	Deep
6	9	1893-2D	2008-05-18 18:00:00+00	2013-12-02 17:00:00+00	f	Falmouth 2D-ACM	Deep
6	10	1788-2D	2006-05-01 17:30:00+00	2008-05-14 18:45:00+00	f	Falmouth 2D-ACM	Deep
8	11	1894-2D	2010-09-17 17:45:00+00	2014-01-23 19:00:01+00	t	Falmouth 2D-ACM	Deep
9	12	1678-2D	2009-05-20 21:45:00+00	2011-11-02 15:15:00+00	f	Falmouth 2D-ACM	Deep
10	13	1674-2D	2009-05-28 17:15:00+00	2014-01-23 18:00:01+00	t	Falmouth 2D-ACM	Deep
7	14	1892-2D	2008-05-16 14:51:24+00	2009-05-24 04:08:40+00	f	Falmouth 2D-ACM	Deep
7	15	1674-2D	2006-05-01 16:45:00+00	2006-08-10 14:00:00+00	f	Falmouth 2D-ACM	Deep
7	16	1890-2D	2007-12-16 23:05:00+00	2008-03-29 09:05:00+00	f	Falmouth 2D-ACM	Deep
7	17	1669-2D	2007-02-15 15:05:00+00	2007-05-19 16:45:00+00	f	Falmouth 2D-ACM	Deep
14	18	107898	2008-12-10 18:00:07+00	2013-02-20 19:00:00+00	f	Level Troll 500	Surface
14	19	165426	2013-02-20 20:00:00+00	2014-02-24 20:00:00+00	t	Level Troll 300	Surface
11	20	107922	2008-12-15 19:45:00+00	2010-03-18 18:45:00+00	f	Level Troll 500	Surface
11	21	107917	2010-08-19 17:00:00+00	2013-02-20 17:00:00+00	f	Level Troll 500	Surface
11	22	107893	2013-02-20 18:00:00+00	2013-03-07 18:04:31+00	f	Level Troll 500	Surface
11	23	343130	2013-07-24 16:00:00+00	2014-02-24 19:00:00+00	t	Level Troll 500	Surface
13	24	107906	2008-12-15 17:15:00+00	2013-02-20 16:00:00+00	f	Level Troll 500	Surface
13	25	107906	2013-10-02 17:00:00+00	2014-02-24 17:00:00+00	t	Level Troll 500	Surface
15	26	107893	2008-12-16 19:59:59+00	2010-03-26 01:45:00+00	f	Level Troll 500	Surface
15	27	107904	2010-08-25 16:15:00+00	2011-09-16 18:45:00+00	f	Level Troll 500	Surface
15	28	166454	2012-04-11 18:15:00+00	2013-02-20 18:00:00+00	f	Aqua Troll 200 CTD	Surface
12	29	107927	2009-01-26 17:30:00+00	2012-11-11 18:27:35+00	f	Level Troll 500	Surface
18	30	107924	\N	\N	\N	\N	\N
\.
*/
