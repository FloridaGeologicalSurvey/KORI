--postgresql magic incantation to generate grant statements for all public views
SELECT 'GRANT SELECT ON ' || quote_ident(schemaname) || '.' || quote_ident(viewname) || ' TO wkp_user;'
	FROM pg_views
	WHERE schemaname = 'public';

