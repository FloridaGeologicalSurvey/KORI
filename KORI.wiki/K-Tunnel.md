_Surface Network_: N/A  
_Deep Network_: Active  
_Approximate Location_: [30°13'42.483"N, 84°18'19.114"W](https://www.google.com/maps/place/30%C2%B013'42.5%22N+84%C2%B018'19.1%22W/@30.228467,-84.3053094,2216m/data=!3m2!1e3!4b1!4m2!3m1!1s0x0:0x0)  
_Approximate Depth_: 290 ft. below top of water table  
_Estimated cross-section at sensor_: Not Available

_Site Characterization_:  
K Tunnel sensor sits about 100 yards upstream from the A-K junction in the K tunnel, approximately 2,650 ft south-southwest of the main vent of Wakulla springs. This conduit runs south to north, roughly parallel to the A conduit, and the direction of flow is south to north. The extent of K conduit has been well explored. 

K conduit shows a moderate response in flow velocity and temperature to recharge events, indicating that it is affected to some degree by run off. The minimum flow velocity of this conduit across all deployments and calibration states was 0.021 cm/s, a mean flow velocity of 3.614 cm/s, and a max flow velocity of 12.219 cm/s. Conductivity is relatively invariant, with a minimum reading of 0.1660 mmho/cm and a maximum reading of 0.9460 mmho/cm. 

The temperature of the water in the conduit as represented in the database is somewhat problematic, and caution is advised when using the temperature data from the original deployment. The original Falmouth 2D-ACM (Deploy Key 9) was replaced with a new unit (Deploy Key 10) on 2008-05-18 due to a failing temperature transducer (Kincaid 2009, 3). The failing sensor can clearly be seen in the pattern of falling temperature values for the 2006-2008 period. The data from the second deployment (Deploy Key 9) indicates that the temperature of this conduit varies according to recharge, with a minimum temperature of 16.14° C and a maximum temperature of 20.51° C.

[![AVDIR](http://i.imgur.com/oEFOWGY.png)](http://i.imgur.com/oEFOWGY.png)
  
[![AVDIR](http://i.imgur.com/ABAM1gk.png)](http://i.imgur.com/ABAM1gk.png)

[![ASPD](http://i.imgur.com/tVnVTI7.png)](http://i.imgur.com/tVnVTI7.png)

[![COND](http://i.imgur.com/sWkX4XF.png)](http://i.imgur.com/sWkX4XF.png)

[![TEMP](http://i.imgur.com/1IvfKiV.png)](http://i.imgur.com/1IvfKiV.png)


_Service History, Deep Network:_
>Falmouth 2D-ACM
>>Date Range: 2006-05-01 to 2008-05-14 (2007 files currently missing)  
>>>Database Deploy Key: 10  
  
>>Date Range: 2008-05-18 to 2013-12-02  
>>>Database Deploy Key: 9  

__Example SQL Query__  
`--Select All Calibrated Readings`  
`SELECT * FROM falmouth WHERE (deploy_key=2 OR deploy_key=3) AND calibration=True`

__Example R Query__  
   `library(RPostgreSQL)`  
    `con <- dbConnect(PostgreSQL(), host="host", user="user", password="password", dbname="wkp_hrdb")`  
    `ad <- dbGetQuery(con, "SELECT date_time, cond, aspd, avdir, temp, calibration FROM falmouth WHERE deploy_key=2 OR deploy_key=3"`  
    `plot(ad$date_time, ad$cond, type="p", pch=20)`  
  
