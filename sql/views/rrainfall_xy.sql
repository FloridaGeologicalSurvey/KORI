CREATE OR REPLACE VIEW rrainfall_xy AS
    select s.site_name, s.localx, s.localy, ghcn.date_time, ghcn.prcp FROM extra.noaa_ghcn INNER JOIN public.sites as S using (site_id);
    