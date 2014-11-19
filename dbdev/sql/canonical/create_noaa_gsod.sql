CREATE TABLE extra.noaa_gsod
(
    gsod_id SERIAL CONSTRAINT gsod_key PRIMARY KEY,
    site_id INTEGER REFERENCES sites (site_id),
    station INTEGER,
    wban INTEGER,
    yearmoda TIMESTAMP WITH TIME ZONE,
    temp NUMERIC(4,1),
    temp_count INTEGER,
    dewp NUMERIC(4,1),
    dewp_count INTEGER,
    slp NUMERIC(5,1),
    slp_count INTEGER,
    stp NUMERIC(5,1),
    stp_count INTEGER,
    visib NUMERIC(3,1),
    visib_count INTEGER,
    wdsp NUMERIC(3,1),
    wdsp_count INTEGER,
    mxspd NUMERIC(4,1),
    gust NUMERIC(4,1),
    max_temp NUMERIC(4,1),
    max_temp_flag BOOLEAN,
    min_temp Numeric(4,1),
    min_temp_flag BOOLEAN,
    prcp NUMERIC(4,1),
    prcp_flag CHAR(1),
    sndp NUMERIC(4,1),
    frshtt INTEGER
);
ALTER TABLE extra.noaa_gsod
    OWNER TO postgres;
COMMENT ON TABLE extra.noaa_gsod IS 'NOAA Global Summaries of the Day values';


COMMENT ON COLUMN extra.noaa_gsod.gsod_id IS 'Table Primary Key';
COMMENT ON COLUMN extra.noaa_gsod.site_id IS 'Foreign key from sites table';
COMMENT ON COLUMN extra.noaa_gsod.station IS 'Station number (WMO/DATSAV3 number)for the location.';
COMMENT ON COLUMN extra.noaa_gsod.wban IS 'WBAN number where applicable';
COMMENT ON COLUMN extra.noaa_gsod.yearmoda IS 'Timestamp, UTC';
COMMENT ON COLUMN extra.noaa_gsod.temp IS 'Mean temperature for the day in degrees (F)';
COMMENT ON COLUMN extra.noaa_gsod.temp_count IS 'Number of observations used in calculating mean temperature';
COMMENT ON COLUMN extra.noaa_gsod.dewp IS 'Mean dew point for the day in degrees (F)';
COMMENT ON COLUMN extra.noaa_gsod.dewp_count IS 'Number of observations used in calculating mean dew point.';
COMMENT ON COLUMN extra.noaa_gsod.slp IS 'Mean sea level pressure for the day (millibars)';
COMMENT ON COLUMN extra.noaa_gsod.slp_count IS 'Number of observations used in calculating mean sea level pressure.';
COMMENT ON COLUMN extra.noaa_gsod.stp IS 'Mean station pressure for the day (millibars)';
COMMENT ON COLUMN extra.noaa_gsod.stp_count IS 'Number of observations used in calculating mean station pressure.';
COMMENT ON COLUMN extra.noaa_gsod.visib IS 'Mean visibility for the day (miles)';
COMMENT ON COLUMN extra.noaa_gsod.visib_count IS 'Number of observations used in calculating mean visibility.';
COMMENT ON COLUMN extra.noaa_gsod.wdsp IS 'Mean wind speed for the day (knots)';
COMMENT ON COLUMN extra.noaa_gsod.wdsp_count IS 'Number of observations used in calculating mean wind speed.';
COMMENT ON COLUMN extra.noaa_gsod.mxspd IS 'Maximum sustained wind speed reported (knots)';
COMMENT ON COLUMN extra.noaa_gsod.gust IS 'Maximum wind gust reported for the day (knots)';
COMMENT ON COLUMN extra.noaa_gsod.max_temp IS 'Maximum temperature reported during the day (F) --time of max temp report varies by country and region, so this will sometimes not be the max for the calendar day.';
COMMENT ON COLUMN extra.noaa_gsod.max_temp_flag IS 'FALSE indicates max temp was taken from the explicit max temp report and not from the hourly data. TRUE indicates max temp was derived from the hourly data (i.e., highest hourly or synoptic-reported temperature).';
COMMENT ON COLUMN extra.noaa_gsod.min_temp IS 'Minimum temperature reported during the day (F) --time of min temp report varies by country and region, so this will sometimes not be the min for the calendar day.';
COMMENT ON COLUMN extra.noaa_gsod.min_temp_flag IS 'FALSE indicates min temp was taken from the explicit min temp report and not from the hourly data. TRUE indicates min temp was derived from the hourly data (i.e., lowest hourly or synoptic-reported temperature).';
COMMENT ON COLUMN extra.noaa_gsod.prcp IS 'Total precipitation (rain and/or melted snow) reported during the day (Inches); will usually not end with the midnight observation--i.e., may include latter part of previous day. .00 indicates no measurable precipitation (includes a trace)';
COMMENT ON COLUMN extra.noaa_gsod.prcp_flag IS 'A = 1 report of 6-hour precipitation amount. B = Summation of 2 reports of 6-hour precipitation amount. C = Summation of 3 reports of 6-hour precipitation amount. D = Summation of 4 reports of 6-hour precipitation amount. E = 1 report of 12-hour precipitation amount. F = Summation of 2 reports of 12-hour precipitation amount. G = 1 report of 24-hour precipitation amount. H = Station reported 0 as the amount for the day (eg, from 6-hour reports), but also reported at least one occurrence of precipitation in hourly observations--this could indicate a trace occurred, but should be considered as incomplete data for the day. I = Station did not report any precip data for the day and did not report any occurrences of precipitation in its hourly observations--it is still possible that precip occurred but was not reported.';
COMMENT ON COLUMN extra.noaa_gsod.sndp IS 'Snow depth in inches to tenths--last report for the day if reported more than once.';
COMMENT ON COLUMN extra.noaa_gsod.frshtt IS 'Indicators (1 = yes, 0 = no/not reported) for the occurrence during the day of: Fog (F - 1st digit). Rain or Drizzle (R - 2nd digit). Snow or Ice Pellets (S - 3rd digit). Hail (H - 4th digit). Thunder (T - 5th digit). Tornado or Funnel Cloud (T - 6th digit).';