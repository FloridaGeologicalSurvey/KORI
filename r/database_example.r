library(RPostgreSQL)

#set pw and host
host <- "FGS-USRV"
pw <- ""

#establish connection
con <- dbConnect(PostgreSQL(), host="FGS-USRV", user="wkp_user", password=pw, dbname="wkp_hrdb")

#send query to DB
all <- dbGetQuery(con, "select deploy_key, cond, aspd, avdir, temp, date_time from falmouth where date_time BETWEEN DATE \'2012-06-25\' and DATE \'2012-06-28\'")


###### using the base plot package ########

#convert deploy_keys to factors
all$dk_factor <- as.factor(all$deploy_key)

#plot
plot(all$date_time, all$aspd, type="p", pch=20, col=all$dk_factor)


########  using ggplot2  ############
#ggplot2 plots
library(ggplot2)

#convert deploy keys to characters
all$dk <- as.character(all$deploy_key)

#base plot
p <- ggplot(all, aes(date_time))

#set colours
colours = c("1" = "red", "3" = "green", "4" = "blue", "7" = "orange", "9" = "darkgray", "11"="purple", "13" = "burlywood")
labs = c("1" = "AD", "3" = "AK", "4" = "B", "7" = "D", "9" = "K", "11"="REV", "13" = "SC10")

#aspd plot, comments for direct file output
#png("SC10_Debby_ASPD.png", width= 12000, height = 6000, res=600)
p + 
	geom_line(aes(y=aspd, colour=dk), alpha=.65) + 
	scale_colour_manual(name="Sensor", values=colours, labels=labs) + 
	xlab("Date") + 
	ylab("Flow Velocity (cm/s)") + 
	ggtitle("Falmouth Sensor Network Response, TS Debby") + 
	scale_x_datetime(breaks = "1 day") + 
	theme(axis.text.x=element_text(angle=90, vjust= .5))
#dev.off()

#temp plot, comments for direct file output
#png("SC10_Debby_TEMP.png", width= 12000, height = 6000, res=600)
p + 
	geom_line(aes(y=temp, colour=dk), alpha=.65) + 
	scale_colour_manual(name="Sensor", values=colours, labels=labs) + 
	xlab("Date") + 
	ylab("Temp (C)") + 
	ggtitle("Falmouth Sensor Network Response, TS Debby") + 
	scale_x_datetime(breaks = "1 day") + 
	theme(axis.text.x=element_text(angle=90, vjust= .5))
#dev.off()

#cond plot, comments for direct file output
#png("SC10_Debby_COND.png", width= 12000, height = 6000, res=600)
p + 
	geom_line(aes(y=cond, colour=dk), alpha=.65) + 
	scale_colour_manual(name="Sensor", values=colours, labels=labs) + 
	xlab("Date") + 
	ylab("Conductivity (mmho/cm)") + 
	ggtitle("Falmouth Sensor Network Response, TS Debby") + 
	scale_x_datetime(breaks = "1 day") + 
	theme(axis.text.x=element_text(angle=90, vjust= .5))
#dev.off()

