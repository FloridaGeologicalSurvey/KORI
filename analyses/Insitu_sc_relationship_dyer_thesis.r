#Code for Dyer Thesis analysis, 
#conceptual work by Scott Barrett Dyer
#implemented in R by Seth Willis Bassett
#2015-07-17


####### CODE IN THIS BLOCK SHOULD BE RUN AT THE START OF EVERY R SESSION #######

#establish database connection
library(RPostgreSQL)

#Set Password Manually
pw = ''

db <- dbConnect(PostgreSQL(), db='wkp_hrdb_dev', host='FGS-USRV', user='postgres', password=pw
#db <- dbConnect(PostgreSQL(), db='wkp_hrdb', host='localhost', user='postgres', password=pw)

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
scott <- dbGetQuery(db, "SELECT * FROM analysis.dyer_insitu")
scott <- scott[,c(2:length(scott))]
library(reshape2)
mscott <- melt(scott, id.vars=c("date_time", "sc_salt"))
vars = c("sul_wle","tur_wle","smrr_wle","wak_wle","rev_wle","lc_wle","punch_wle","tob_wle","sc_efw")
mscott2 <- mscott[mscott$variable %in% vars,]
mscott2$value <- as.numeric(mscott2$value)
mscott2$variable <- factor(mscott2$variable)
levels(mscott2$variable) <- vars
mscott2$fac <- cut(mscott2$sc_salt, breaks=c(0,10,20,30,40))

#convert to feet
mscott2$value = mscott2$value * 3.28084



png("Median plot of insitu wle factored by SC10 salinity Dyer Thesis Daily Average.png", width = 5000, height=3000, res=300)

p <- ggplot(mscott2[!is.na(mscott2$fac),], aes(x=variable, y=value, colour=fac))
p + theme_bw() +
    stat_summary(fun.y=median, geom="line", aes(group=fac), size=1, alpha=0.7) +
    stat_summary(fun.y=median, geom="point", aes(group=fac), size=2, alpha=1) + 
    scale_colour_manual(values=c("lightblue","orange","red3"), name="Salinity\n(ppt)") + 
    xlab("Site") + 
    ylab("Water Level Elevation (Ft.)") + 
    ggtitle("Median Water Level Elevation\nFactored by Aggregate (USGS) Spring Creek Salinity\nDaily Averages, Dyer Thesis Period") + 
    scale_y_continuous(breaks=seq(0,11,0.25)) + 
    annotate("text",x="sul_wle", y=3, label="N Values\n(0,10] = 2,034\n(10,20] = 1,107\n(20,30] = 846\nNA = 261", position="right", size=4) + 
    annotate("text",x="tur_wle", y=3, label="Median Difference, [20,30) - [0,10)\nSullivan: -0.935\nTurner: -0.427\nSMRR: 0\nWakulla: -0.328\nRevell: 0.016\nLost Creek: -0.754\nPunchbowl: 3.18\nTobacco: 3.05\nSpring Creek EFH: 5.02", position="right", size=4) 
dev.off()
    
p <- ggplot(mscott2, aes(x=value, colour=variable))

p + 
    geom_density(alpha=.2, aes(fill=variable)) + 
    facet_grid(.~fac) + 
    coord_flip() 
    
    
    
    
p <- ggplot(mscott2, aes(x=date_time, y=value, colour=fac))
p + geom_point() + 
    facet_grid(variable~., scales="free_y") + 
    scale_colour_manual(values=c("blue","yellow","red"))
    
