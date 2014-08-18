_Surface Network_: N/A  
_Deep Network_: Active  
_Approximate Location_: [30°13'41.972"N, 84°18'17.283"W](https://www.google.com/maps/place/30%C2%B013'42.0%22N+84%C2%B018'17.3%22W/@30.2283252,-84.3048008,2216m/data=!3m1!1e3!4m2!3m1!1s0x0:0x0)  
_Approximate Depth_: 290 ft. below top of water table  
_Estimated cross-section at sensor_: Not Available

_Site Characterization_:  
The AK tunnel sensor sits about 100 yards upstream from the A-K junction in A tunnel, approximately 2,650 ft south-southwest of the main vent of Wakulla springs. This conduit runs south to north, roughly parallel to the K tunnel, with the direction of flow running to the north. The extent of A conduit has been well explored.

A conduit shows a moderate response in flow velocity to recharge events, indicating that it is affected to some degree by run off. The minimum flow velocity of this conduit across all deployments and calibration states was 0.006 cm/s, a mean flow velocity of 5.309 cm/s, and a max flow velocity of 25.734 cm/s. Conductivity is relatively invariant, with a minimum reading of 0.1800 mmho/cm and a maximum reading of 1.0990 mmho/cm. 

The temperature of the water in the conduit as represented in the database is somewhat problematic, and caution is advised when using the temperature data from the original deployment. The original Falmouth 2D-ACM (Deploy Key 2) was replaced with a new unit (Deploy Key 3) on 2008-05-18 due to a failing temperature transducer (Kincaid 2009, 3). The failing sensor can clearly be seen in the pattern of falling temperature values for the 2006-2008 period. 

[![AVDIR](http://i.imgur.com/V8ZxyEW.png)](http://i.imgur.com/V8ZxyEW.png)
  
[![AVDIR](http://i.imgur.com/ZePgvhZ.png)](http://i.imgur.com/ZePgvhZ.png)

[![ASPD](http://i.imgur.com/zS75yxF.png)](http://i.imgur.com/zS75yxF.png)

[![COND](http://i.imgur.com/6YNEWo2.png)](http://i.imgur.com/6YNEWo2.png)

[![TEMP](http://i.imgur.com/LQHvsV8.png)](http://i.imgur.com/LQHvsV8.png)


_Service History, Deep Network:_
>Falmouth 2D-ACM
>>Date Range: 2006-05-01 to 2008-05-14 (2007 files currently missing)  
>>>Database Deploy Key: 2  
  
>>Date Range: 2008-05-18 to 2013-12-02  
>>>Database Deploy Key: 3  

__Example SQL Query__  
`--Select All Calibrated Readings`  
`SELECT * FROM falmouth WHERE (deploy_key=2 OR deploy_key=3) AND calibration=True`

__Example R Query__  
   `library(RPostgreSQL)`  
    `con <- dbConnect(PostgreSQL(), host="host", user="user", password="password", dbname="wkp_hrdb")`  
    `ad <- dbGetQuery(con, "SELECT date_time, cond, aspd, avdir, temp, calibration FROM falmouth WHERE deploy_key=2 OR deploy_key=3"`  
    `plot(ad$date_time, ad$cond, type="p", pch=20)`  
  
