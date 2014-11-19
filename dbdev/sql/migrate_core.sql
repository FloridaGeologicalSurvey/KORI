DELETE from core.insitu;
alter sequence core.insitu_insitu_id_seq restart with 1;

INSERT INTO core.deploy_info
SELECT * FROM public.deploy_info;

INSERT INTO core.falmouth
SELECT * FROM public.falmouth;

INSERT INTO core.insitu
SELECT * FROM public.insitu;

