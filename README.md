Readme for the FGS Karst Open Research Initiative  

Updated 2015-09-28:  
  
The repository will be undergoing major changes in the next three months. The following proposed reorg will probably happen as I get to them:  
  
* dbdev folder will be moved to private subversion repository, making my raw development code unavailable to the general public unless otherwise publicized  
* rkori folder will be moved to its own repository names rkori  
* other folders will be consolidated and reorganized as needed  
  
Essentially, what I will be altering is the presentation of this github repo. It is beginning to generate a bit of interest, so my goals over the next three months will be to get the code base cleaned up and in presentation/sharing quality. 

As is, the way I see the reorg happening is this: rkori (the r package for working with the actual data) will be streamlined and held in its own repository named rkori. This repository will hold analysis and other presentation quality code in RMarkDown, along with a gh-pages branch to showcase the various analyses in HTML. The raw code I use to sort and clean the raw files will be moved onto my private subversion repository and will no longer be publically available until after I am done developing it (contrast to what the spaghetti farm looks like now).  
  
At present, I am evaluating several database designs into which to migrate the data. Until a decision is made and I begin this migration, all data files have been removed from the FTP and are available by direct request only. 

I am also protyping some RMarkdown analyes and reports, as well as some java-based interactive tools at:  
http://floridageologicalsurvey.github.io/koristatatlas/  

Feel free to visit and drop me an email detailing what you think.  

As always, if you have questions, comments, contributions or need help on any subject, please feel free to contact me directly at:
seth [adot] bassett [at] dep [adot] state [adot] fl [adot] us


Please see the KORI github wiki for documentation and metadata:  
    https://github.com/FloridaGeologicalSurvey/KORI/wiki  
  
WKP-HRDB Database Download Location (NOT CURRENTLY AVAILABLE, PLEASE EMAIL ME DIRECTLY):  
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
  
R 3.2.0
    http://cran.r-project.org/


