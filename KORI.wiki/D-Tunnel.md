_Surface Network_: N/A  
_Deep Network_: Active  
_Approximate Location_: [30°13'58.645"N, 84°18'16.757"W](https://www.google.com/maps/place/30%C2%B013'58.6%22N+84%C2%B018'16.8%22W/@30.2329568,-84.3046547,2298m/data=!3m1!1e3!4m2!3m1!1s0x0:0x0)  
_Approximate Depth_: 290 ft. below top of water table  
_Estimated cross-section at sensor_: 504 ft^2 (WKPP Est, Kincaid 2009)  

![Kincaid 2009](http://i.imgur.com/PtbIpMg.png)  
_Source_: Kincaid 2009, p3  
__Note: This cross-section and estimate applies only to records with a deploy key of 6__
  

_Site Characterization_:  
D Tunnel sensor sits about 100 yards upstream from the A-D junction, approximately 1,000 ft southwest of the main vent of Wakulla springs. This conduit runs north-northwest to south-southeast. The extent of D conduit is relatively unexplored. 

Of all of the deep network sensors, the deployment history of the D location is the most complex. A sensor was originally deployed in this location on 2006-05-01 (Deploy Key 8). The sensor was subsequently replaced by the divers on 2007-12-17 due to a malfunction (Deploy Key 6). The replacement sensor subsequently stopped transmitting data on 2009-07-08, and the sensor was replaced yet again on 2011-07-12 (Deploy Key 7). 

Caution is advised when using the directional data from these meters; the average direction of flow measurements from the three meters indicates that small changes in the location of the sensor within the conduit produced large changes in the direction of flow measured by the sensor. Additionally, these sensors should be reading a direction of flow from north or northwest to the south - currently, only the deploy key 6 readings show readings that approach the proper direction of flow. An issue has been opened in the issue tracker related to this problem: [see issue #3.](https://github.com/FloridaGeologicalSurvey/KORI/issues/3) 
 

D conduit shows a relative indifference to recharge events, indicating that it is primarily composed of groundwater. The minimum flow velocity of this conduit across all deployments and calibration states was 0.004 cm/s, a mean flow velocity of 1.549 cm/s, and a max flow velocity of 4.413 cm/s. Conductivity is also invariant, with a minimum reading of 0.2630 mmho/cm and a maximum reading of .3640 mmho/cm. The temperature of the water in the conduit shows a range of only 0.5° C, with a minimum temperature of 20.49° C and a maximum of 20.83° C.

[![AVDIR](http://i.imgur.com/WpduDxg.png)](http://i.imgur.com/WpduDxg.png)
  
[![AVDIR](http://i.imgur.com/ncI5AR1.png)](http://i.imgur.com/ncI5AR1.png)

[![AVDIR](http://i.imgur.com/nVP7H6Y.png)](http://i.imgur.com/nVP7H6Y.png)

[![ASPD](http://i.imgur.com/QlxD9E3.png)](http://i.imgur.com/QlxD9E3.png)

[![COND](http://i.imgur.com/qmQwfMw.png)](http://i.imgur.com/qmQwfMw.png)

[![TEMP](http://i.imgur.com/eINKVyd.png)](http://i.imgur.com/eINKVyd.png)


_Service History, Deep Network:_
>Falmouth 2D-ACM
>>Date Range: 2006-05-01 to 2006-12-05 (2007 files currently missing)  
>>>Database Deploy Key: 8  
  
>>Date Range: 2007-12-17 to 2009-07-08  
  
>>>Database Deploy Key: 6  
  
>>Date Range: 2011-07-12 to 2013-12-02  
>>>Database Deploy Key: 7  


__Example SQL Query__  
`--Select All Calibrated Readings`  
`SELECT * FROM falmouth WHERE (deploy_key=6 OR deploy_key=7 OR deploy_key=8) AND calibration=True`

__Example R Query__  
   `library(RPostgreSQL)`  
    `con <- dbConnect(PostgreSQL(), host="host", user="user", password="password", dbname="wkp_hrdb")`  
    `ad <- dbGetQuery(con, "SELECT date_time, cond, aspd, avdir, temp, calibration FROM falmouth WHERE deploy_key=6 OR deploy_key=7 OR deploy_key=8"`  
    `plot(ad$date_time, ad$cond, type="p", pch=20)`  
  
