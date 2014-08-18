_Surface Network_: N/A  
_Deep Network_: Active  
_Approximate Location_: [30°14'1.302"N, 84°18'6.336"W ](https://www.google.com/maps/place/30%C2%B014'01.3%22N+84%C2%B018'06.3%22W/@30.2345557,-84.3010003,917m/data=!3m1!1e3!4m2!3m1!1s0x0:0x0)  
_Approximate Depth_: 290 ft. below top of water table  
_Estimated cross-section at sensor_: 129 ft^2 (WKPP Est, Kincaid 2009)  

![Kincaid 2009](http://i.imgur.com/F5Ask0X.png)  
_Source_: Kincaid 2009, p3  
  

_Site Characterization_:  
The B tunnel sensor sits approximately 100 yards upstream of the intersection of B and C tunnel, approximately 663 ft. south-southeast of the main Wakulla vent. The B conduit runs east-northeast from the B-C intersection and then turns north under the Wakulla river. This conduit is one of the lesser explored conduits and relatively is little known about its path.
  
This conduit is dominated by groundwater flow, and shows little sensitivity to recharge events. The predominant direction of flow at this sensor is to the southwest, with a minimum flow velocity of 5.016 cm/s, a mean flow velocity of 10.0777 cm/s, and a max flow velocity of 24.474 cm/s for all measurements. Both conductivity and temperature are relatively invariant: the minimum temperature is 20.46° C while the maximum is 20.70° C; the minimum conductivity is 0.2820 mmho/cm and the maximum conductivity is 0.3310 mmho/cm.

Note there is a known bad row recorded by this sensor at 2008-07-30 18:02:15 UTC that does not agree with any other data collected by this sensor. The pressure readings at this sensor also shows a steady decline after 2008 as the pressure transducer began to fail.

[![AVDIR](http://i.imgur.com/IjgENUz.png)](http://i.imgur.com/IjgENUz.png)  

[![ASPD](http://i.imgur.com/7n7wrfP.png)](http://i.imgur.com/7n7wrfP.png)

[![COND](http://i.imgur.com/njjvQh9.png)](http://i.imgur.com/njjvQh9.png)

[![TEMP](http://i.imgur.com/mO9MqUX.png)](http://i.imgur.com/mO9MqUX.png)


_Service History, Deep Network:_
>Falmouth 2D-ACM
>>Date Range: 2006-05-01 to 2013-12-02  
>>>Database Deploy Key: 4

__Example SQL Query__  
`--Select All Calibrated Readings`  
`SELECT * FROM falmouth WHERE deploy_key=4 AND calibration=True`

__Example R Query__  
   `library(RPostgreSQL)`  
    `con <- dbConnect(PostgreSQL(), host="host", user="user", password="password", dbname="wkp_hrdb")`  
    `b <- dbGetQuery(con, "SELECT date_time, cond, aspd, avdir, temp, calibration FROM falmouth WHERE  deploy_key=4")`  
    `plot(b$date_time, b$cond, type="p", pch=20)`  
  

![Falmouth 2D-ACM in B Tunnel](https://camo.githubusercontent.com/cd39b56bef253c36b4c4bd1407002c274db881c9/687474703a2f2f692e696d6775722e636f6d2f76636f4d5467612e6a7067)
_Photo Credits: Woodville Karst Plain Project Divers_