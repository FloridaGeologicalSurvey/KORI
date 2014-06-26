library(chron)
library(lattice)

header= c('datetime','avn','ave','aspd','avdir','atlt','cond','temp','pres','hdng','batt','vx','vy','tx','ty','hx','hy','hz','vn','ve','stemp','sv1','vab','vcd','vef','vgh','id','dev_deply_ky','salt','depth','sv2')
fClasses = c("char","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric")

loadFalmouth <- function(fName){
fClasses = c("Date","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric","numeric")
f = read.csv(fName, header=T, sep=",", colClasses = fClasses)

day=cut(f$datetime, breaks="days")
month=months(f$datetime)
month = factor(month, levels=c("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"), labels=c("Jan", "Feb", "Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"), ordered=T)
year = cut(f$datetime, breaks="years")
f = data.frame(f, day, month, year)
return(f)
}

condplot <- function(f, sName, interval) {
bwTitle = paste(sName, "COND by year by Month,",interval)
bwplot(f$cond~f$month|f$year, ylab="COND (mmho/cm)", xlab="Month", main=bwTitle, layout=c(8,1), aspect = 8/8, scales=list(x=list(rot=90)))
}

aspdplot <- function(f, sName, interval) {
bwTitle = paste(sName, "ASPD by year by Month,", interval)
bwplot(f$aspd~f$month|f$year, ylab="ASPD (cm/s)", xlab="Month", main=bwTitle, layout=c(8,1), aspect = 8/8, scales=list(x=list(rot=90)))
}

tempplot <- function(f, sName, interval) {
bwTitle = paste(sName, "TEMP by year by Month,", interval)
bwplot(f$temp~f$month|f$year, ylab="TEMP (C)", xlab="Month", main=bwTitle, layout=c(8,1), aspect = 8/8, scales=list(x=list(rot=90)))
}
interval = "1 Day Average"

######
ad <- loadFalmouth("AD")
sName = "AD"


fName = "COND_AD.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
condplot(ad, sName, interval)
dev.off()

fName = "TEMP_AD.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(ad, sName, interval)
dev.off()

fName = "ASPD_AD.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(ad, sName, interval)
dev.off()
rm(ad)

####### D Tunnel
d <- loadFalmouth("d")
sName = "D"


fName = "COND_D.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
condplot(d, sName, interval)
dev.off()

fName = "TEMP_D.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(d, sName, interval)
dev.off()

fName = "ASPD_D.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(d, sName, interval)
dev.off()
rm(d)


######
ak <- loadFalmouth("ak")
sName = "AK"

fName = "COND_AK.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
condplot(ak, sName, interval)
dev.off()

fName = "TEMP_AK.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(ak, sName, interval)
dev.off()

fName = "ASPD_AK.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(ak, sName, interval)
dev.off()
rm(ak)

#######
b <- loadFalmouth("b")
sName = "B"


fName = "COND_B.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
bwplot(b$cond~b$month|b$year, ylab="COND (mmho/cm)", xlab="Month", main="B COND, 1 Day Average", layout=c(8,1), aspect = 8/8, scales=list(x=list(rot=90)), ylim=c(.25,.35))
dev.off()

fName = "TEMP_B.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(b, sName, interval)
dev.off()

fName = "ASPD_B.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(b, sName, interval)
dev.off()
rm(b)

#######
c <- loadFalmouth("c")
sName = "C"


fName = "COND_C.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
bwplot(c$cond~c$month|c$year, ylab="COND (mmho/cm)", xlab="Month", main="C COND, 1 Day Average", layout=c(8,1), aspect = 8/8, scales=list(x=list(rot=90)), ylim=c(.2,.6))
dev.off()

fName = "TEMP_C.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(c, sName, interval)
dev.off()

fName = "ASPD_C.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(c, sName, interval)
dev.off()
rm(c)


####### K Tunnel
k <- loadFalmouth("k")
sName = "K"


fName = "COND_K.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
condplot(k, sName, interval)
dev.off()

fName = "TEMP_K.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(k, sName, interval)
dev.off()

fName = "ASPD_K.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(k, sName, interval)
dev.off()
rm(k)

####### Revell
rev <- loadFalmouth("Revell")
sName = "Revell"


fName = "COND_Revell.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
condplot(rev, sName, interval)
dev.off()

fName = "TEMP_Revell.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(rev, sName, interval)
dev.off()

fName = "ASPD_Revell.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(rev, sName, interval)
dev.off()
rm(rev)

#######
sc1 <- loadFalmouth("SC1")
sName = "SC1"

### SC1
fName = "COND_SC1.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
condplot(sc1, sName, interval)
dev.off()

fName = "TEMP_SC1.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(sc1, sName, interval)
dev.off()

fName = "ASPD_SC1.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(sc1, sName, interval)
dev.off()
rm(sc1)


####### SC10
sc10 <- loadFalmouth("SC10")
sName = "SC10"


fName = "COND_SC10.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
condplot(sc10, sName, interval)
dev.off()

fName = "TEMP_SC10.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(sc10, sName, interval)
dev.off()

fName = "ASPD_SC10.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(sc10, sName, interval)
dev.off()
rm(sc10)

###### VENT
vent <- loadFalmouth("Vent")
sName = "Vent"

fName = "COND_Vent.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
condplot(vent, sName, interval)
dev.off()

fName = "TEMP_Vent.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
tempplot(vent, sName, interval)
dev.off()

fName = "ASPD_Vent.tif"
tiff(file=fName, bg="white",  height=500, width= 1500, antialias = "cleartype")
aspdplot(vent, sName, interval)
dev.off()
rm(vent)


