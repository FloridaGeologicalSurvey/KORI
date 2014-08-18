_Surface Network_: N/A  
_Deep Network_: Active  
_Approximate Location_: [30°13'57.064"N, 84°18'16.68"W](https://www.google.com/maps/place/30%C2%B013'57.1%22N+84%C2%B018'16.7%22W/@30.2325173,-84.3046333,2216m/data=!3m2!1e3!4b1!4m2!3m1!1s0x0:0x0)  
_Approximate Depth_: 270 ft. below top of water table  
_Estimated cross-section at sensor_: 2404 ft^2 (WKPP Est, Kincaid 2009)  

![Kincaid 2009](http://i.imgur.com/UNkW3ag.png)  
_Source_: Kincaid 2009, p3  
  

_Site Characterization_:  
The AD tunnel sensor sits in the A tunnel about 100 yards upstream of the intersection of A and D tunnels; this location is approximately 1,200 ft. southwest of the main Wakulla vent. The A conduit runs south from the A-D intersection. This conduit is one of the better explored conduits and leads the the Q-terminus, which is the southern limit of exploration. 
  
This conduit shows a strong response to recharge events. The predominant direction of flow at this sensor is to the northwest, with a minimum flow velocity of 0.019 cm/s, a mean flow velocity of 6.921 cm/s, and a max flow velocity of 37.935 cm/s for all measurements. Conductivity is relatively invariant, with a minimum reading of 0.1850 mmho/cm and a maximum reading of 1.0480 mmho/cm. The temperature of the water in the conduit shows a strong response to recharge events, with a minimum temperature of 18.54° C and a maximum of 22.20° C; additionally, a clear seasonal pattern can be seen in the temperature data from this sensor.

The pressure readings at this sensor also shows a steady decline after 2008 as the pressure transducer began to fail, a pattern that is typical in the deep network sensors that go long periods without servicing.

[![AVDIR](http://i.imgur.com/p4VQFb6.png)](http://i.imgur.com/p4VQFb6.png)  

[![ASPD](http://i.imgur.com/yDPmPUT.png)](http://i.imgur.com/yDPmPUT.png)

[![COND](http://i.imgur.com/OyLZKVw.png)](http://i.imgur.com/OyLZKVw.png)

[![TEMP](http://i.imgur.com/76adgVL.png)](http://i.imgur.com/76adgVL.png)


_Service History, Deep Network:_
>Falmouth 2D-ACM
>>Date Range: 2006-05-01 to 2013-12-02  
>>Database Deploy Key: 1

__Example SQL Query__  
`--Select All Calibrated Readings`  
`SELECT * FROM falmouth WHERE deploy_key=1 AND calibration=True`

__Example R Query__  
   `library(RPostgreSQL)`  
    `con <- dbConnect(PostgreSQL(), host="host", user="user", password="password", dbname="wkp_hrdb")`  
    `ad <- dbGetQuery(con, "SELECT date_time, cond, aspd, avdir, temp, calibration FROM falmouth WHERE  deploy_key=1")`  
    `plot(ad$date_time, ad$cond, type="p", pch=20)`  
  

