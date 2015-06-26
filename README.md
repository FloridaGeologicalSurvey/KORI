Readme for the FGS Karst Open Research Initiative  

Updated 2015-06-26 Message from Seth (developer & maintainer of the KORI repository and all around nice guy):  
I am in the process of substantially revising the wiki in preparation for a few performance measurables that are due next week. The focus is on creating a user guide and tutorials for the database itself and the rkori package for R 3.1.2. Expect substantial revisions and additions to these sections of the wiki over the next few days, with smaller additions coming in the next weeks.

In data news, the current copy of the database on the FTP is my _dev version that includes a fair amount of the insitu surface sensor data. As of 2015-06-24, the insitu and insitu_wle tables should be treated with a high degree of caution: I'm only about halfway through loading the insitu data and have not had a chance to check the values in the database against the values in the raw files. The calculated WLE's use the average daily barometric pressure from the Tallahassee airport; I'm still waiting on Scott to cross check these values.

I hope to have the insitu data loaded and verified and the WLE data calculated out and the accompanying documentation generated in the next month or two. Work has been busy and I have a bunch of other projects clamoring for my attention - I'm hoping when my boss and I work to generate new performance goals for the coming year I can get a bit more focus on this project and really push development along.

At this point, treat any values you see in the database with suspicion - only yesterday I found a problem with some of the B conduit data (see the latest issue on the issues page. 

As always, if you have questions, comments, contributions or need help on any subject, please feel free to contact me directly at:
seth [dot] bassett [at] dep [dot] state [dot] fl [dot] us


Please see the KORI github wiki for documentation and metadata:  
    https://github.com/FloridaGeologicalSurvey/KORI/wiki  
  
WKP-HRDB Database Download Location:  
    ftp://ftp.dep.state.fl.us/pub/outgoing/fgs/KORI/  

WKP-HRDB Database general installation notes:  
    https://github.com/FloridaGeologicalSurvey/KORI/wiki/Woodville-Karst-Plain-Hydrologic-Research-Database-(WKP-HRDB)
    

FTP Files (refer to installation notes above):  
    wkp_hrdb.backup  -- Native PostgreSQL compressed backup of the WKP-HRDB  
    wkp_hrdb.sql -- Raw SQL dump of the WKP-HRDB  
    wkp_hrdb.sql.zip -- .zip compressed copy of wkp_hrdb.sql  
  
Required Software:  
  
PostgreSQL 9.1.14  
    http://www.postgresql.org/download/  
    http://www.postgresql.org/docs/9.1/static/  
  
Python 2.7.6  
    https://www.python.org/download/releases/2.7.6/  
    https://docs.python.org/2/  
  
psycopg2 2.5.2  
    http://initd.org/psycopg/download/  
    http://initd.org/psycopg/docs/  
  
pandas 0.13.1  
    https://pypi.python.org/pypi/pandas/0.13.1/#downloads  
    http://pandas.pydata.org/pandas-docs/version/0.13.1/  
  
R 3.1.2  
    http://cran.r-project.org/


