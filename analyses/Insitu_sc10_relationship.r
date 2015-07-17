#Analysis by Seth Willis Bassett and Scott Barrett Dyer
#This analysis illustrates the relationship between the salinity at spring creek 10 and the surface water elevation
#Results indicate that WLE in karst windows are higher when SC10 is siphoning salt water
#The accompanying SQL code needs to be run for this analysis to work properly



####### CODE IN THIS BLOCK SHOULD BE RUN AT THE START OF EVERY R SESSION #######

#establish database connection
library(RPostgreSQL)
db <- dbConnect(PostgreSQL(), db='wkp_hrdb_dev', host='FGS-USRV', user='postgres', password='incorrectLitho')
#db <- dbConnect(PostgreSQL(), db='wkp_hrdb', host='localhost', user='postgres', password='incorrectLitho')

#load rkori package
library(rkori)
setwd("c:/rdata")

#set system environment in R to the proper time zone
#this should be run every single R session
Sys.setenv(TZ='UTC')
setwd("C:/rdata")
########  END BLOCK ########

########## LIBRARY IMPORTS FOR THIS CODEBLOCK #######
library(ggplot2)
library(ggthemes)
require(gridExtra)
library(lubridate)
library(scales)
library(RColorBrewer)


########## END LIBRARY IMPORTS    ############# 
#set password manually
pw = ''
db <- dbConnect(PostgreSQL(), db='wkp_hrdb_dev', host='FGS-USRV', user='postgres', password=pw)

#query
insitu <- dbGetQuery(db, "SELECT * from analysis.insitu_salt_hourly WHERE elev_ft > 0 AND date_time >= \'2009-01-01 00:00:00\' AND date_time <\'2014-01-01 00:00:00\' AND site_name != \'St. Marks River Rise (Surface)\';")

#dyer thesis period
#insitu <- dbGetQuery(db, "SELECT * from analysis.insitu_salt_hourly WHERE elev_ft > 0 AND date_time >= \'2008-01-01 00:00:00\' AND date_time <\'2010-04-01 00:00:00\' AND site_name != \'St. Marks River Rise (Surface)\';")

#factor
insitu$fac <- cut(insitu$salt, breaks=c(0,10,20,30,40))
levs <- c("Sullivan Sink (Surface)","Turner Sink (Surface)","Vent (Surface)","Revell Sink (Surface)","Lost Creek (Surface)","Tobacco Sink (Surface)")
insitu$site_name <- factor(insitu$site_name, levels=levs)

#colours
cols <- c("lightblue","orange","pink","red1")

png("Insitu WLE coloured by SC10 salinity, Hourly Averages 2009-2013.png", width = 12000, height=6000, res=600)
p <- ggplot(insitu, aes(x=date_time, y=elev_ft, colour=fac))
p + theme_bw() + 
    geom_point(size=0.25, alpha=1/3) + 
    facet_grid(site_name~.) + 
    ggtitle("Insitu Water Level Elevations\nColoured by SC10 salinity\nHourly Averages, 2009-2013") + 
    ylab("Water Level Elevation (Ft.)") + 
    xlab("Timestamp (UTC)") + 
    scale_x_datetime(breaks="1 months") + 
    scale_y_continuous(breaks=seq(0,20,1)) + 
    scale_colour_manual(values =cols, name="Salinity\n(PSU)") +
    guides(colour=guide_legend(override.aes = list(size=4, alpha=1))) +
    theme(legend.position="right", axis.text.x = element_text(angle=90, size=8, vjust= 0.5), axis.text.y = element_text(size=4), plot.title = element_text(face="bold", size=14))
dev.off()  
    

png("Median plot of insitu wle factored by SC10 salinity 2009-2013 hourly averages.png", width = 5000, height=3000, res=300)
p <- ggplot(insitu, aes(x=site_name, y=elev_ft, colour=fac))
p + theme_bw() +
    stat_summary(fun.y=median, geom="line", aes(group=fac), size=1, alpha=0.7) +
    stat_summary(fun.y=median, geom="point", aes(group=fac), size=2, alpha=1) +
    scale_y_continuous(breaks=c(seq(4,8,0.1))) + 
    ggtitle("Median Insitu WLE\nFactored by Salinity at Spring Creek\nHourly Averages, 2009-2013") + 
    xlab("Site") + 
    ylab("Elevation (Ft.)") + 
    theme(legend.position="right", axis.text.x = element_text(angle=90, size=8, vjust= 0.5), axis.text.y = element_text(size=10), plot.title = element_text(face="bold", size=18)) +
    scale_colour_manual(values =cols, name="Salinity\n(PSU)") + 
    annotate("text",x="Sullivan Sink (Surface)", y=4.6, label="N Values\n(0,10] = 79,888\n(10,20] = 13,544\n(20,30] = 73,978\n(30,40] = 7,926\nNA = 28,769", position="right", size=4) + 
    annotate("text",x="Turner Sink (Surface)", y=4.6, label="Median Difference, [30,40) - [0,10)\nSullivan: 0.0497\nTurner: 0.7185\nWakulla: 0.26625\nRevell=0.5984\nLost Creek=1.9166\nTobacco=2.544", position="right", size=4) 
    
dev.off()

png("Density plot of insitu wle factored by SC10 salinity 2009-2013 hourly averages.png", width = 5000, height=3000, res=300)
p <- ggplot(insitu[!is.na(insitu$fac),], aes(x=elev_ft, fill=fac))
p + theme_bw() +
    geom_density(alpha=.3, aes(fill=fac)) + 
    facet_grid(.~site_name) +
    coord_flip(xlim=c(1,10)) + 
    scale_x_continuous(breaks=c(seq(1,10,0.25))) + 
    theme(legend.position="right", axis.text.x = element_text(angle=90, size=8, vjust= 0.5), axis.text.y = element_text(size=10), plot.title = element_text(face="bold", size=18)) + 
    ggtitle("Density Plot of WLE (FT) At Surface Insitu Sites\nFactored by Spring Creek Salinity (PSU)\nHourly Averages, 2009-2013") +
    xlab("Elevation (Ft.)") + 
    ylab("Density")  +
    scale_fill_manual(values =cols, name="Salinity\n(PSU)")
dev.off()

#Calibration
png("Calibration Plot of Insitu Sensors 2009-2013 hourly averages.png", width = 5000, height=3000, res=300)
cal <- dbGetQuery(db, "SELECT s.site_name, i.date_time, i.calibration FROM insitu i INNER JOIN deploy_info d USING (deploy_key) INNER JOIN sites s USING (site_id) WHERE date_time >= \'2009-01-01 00:00:00\' AND date_time <\'2014-01-01 00:00:00\' AND site_name != \'St. Marks River Rise (Surface)\';")
levs <- c("Sullivan Sink (Surface)","Turner Sink (Surface)","Vent (Surface)","Revell Sink (Surface)","Lost Creek (Surface)","Tobacco Sink (Surface)")
cal$site_name <- factor(cal$site_name, levels=levs)

pcal <- ggplot(cal, aes(x=date_time, y=site_name, colour=calibration))
pcal + theme_bw() + 
    geom_point(size=0.5) + 
    scale_x_datetime(breaks="2 months") + 
    theme(legend.position="right", axis.text.x = element_text(angle=90, size=8, vjust= 0.5), axis.text.y = element_text(size=10), plot.title = element_text(face="bold", size=18)) + 
    ggtitle("Insitu Calibration Status") + 
    scale_colour_manual(values =c("red","darkgreen"), name="Calibrated") + 
    ylab("Site") + 
    xlab("Date")
dev.off())
    

