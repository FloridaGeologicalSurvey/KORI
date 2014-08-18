_Surface Network_: N/A  
_Deep Network_: Active  
_Approximate Location_: [30°14'1.043"N, 84°18'6.826"W ](https://www.google.com/maps/place/30%C2%B014'01.0%22N+84%C2%B018'06.8%22W/@30.2336227,-84.3018961,2216m/data=!3m1!1e3!4m2!3m1!1s0x0:0x0)  
_Approximate Depth_: 290 ft. below top of water table  
_Estimated cross-section at sensor_: 886 ft^2 (WKPP Est, Kincaid 2009)  

![Kincaid 2009](http://i.imgur.com/yBCjL4Q.png)  
_Source_: Kincaid 2009, p3  
  

_Site Characterization_:  
The C tunnel sensor sits approximately 100 yards upstream of the intersection of B and C tunnel, approximately 730 ft. south-southeast of the main Wakulla vent. The C conduit runs south-southeast from the B-C intersection and then turns southwest. This conduit is one of the lesser explored conduits.
  
C, like B conduit, is dominated by groundwater flow, and shows little sensitivity to recharge events. The predominant direction of flow at this sensor is to the northwest, with a minimum flow velocity of 0.073 cm/s, a mean flow velocity of 2.223 cm/s, and a max flow velocity of 7.534 cm/s for all measurements. Both conductivity and temperature are relatively invariant: the minimum temperature is 20.36° C while the maximum is 20.66° C; the minimum conductivity is 0.2830 mmho/cm and the maximum conductivity is 0.4250 mmho/cm.

Note there is a presumed bad conductivity value recorded by this sensor at 2012-02-09 19:21:19 UTC that does not agree with any other data collected by this sensor. The pressure readings at this sensor also show a steady decline even during the calibration period that is similar to that of a failing pressure transducer (cf. B conduit pressure data).

[![AVDIR](http://i.imgur.com/EzTE9fs.png)](http://i.imgur.com/EzTE9fs.png)  

[![ASPD](http://i.imgur.com/k9D2Tk2.png)](http://i.imgur.com/k9D2Tk2.png)

[![COND](http://i.imgur.com/hipOCBK.png)](http://i.imgur.com/hipOCBK.png)

[![TEMP](http://i.imgur.com/gkpxSqe.png)](http://i.imgur.com/gkpxSqe.png)


_Service History, Deep Network:_
>Falmouth 2D-ACM
>>Date Range: 2006-05-01 to 2013-01-10  
>>>Database Deploy Key: 5

__Example SQL Query__  
`--Select All Calibrated Readings`  
`SELECT * FROM falmouth WHERE deploy_key=5 AND calibration=True`

__Example R Query__  
   `library(RPostgreSQL)`  
    `con <- dbConnect(PostgreSQL(), host="host", user="user", password="password", dbname="wkp_hrdb")`  
    `c <- dbGetQuery(con, "SELECT date_time, cond, aspd, avdir, temp, calibration FROM falmouth WHERE  deploy_key=5")`  
    `plot(c$date_time, c$cond, type="p", pch=20)`  
 