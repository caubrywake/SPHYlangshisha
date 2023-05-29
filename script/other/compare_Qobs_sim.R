rm(list = ls())
library(raster)
library(sp)
library(Hmisc)
library(maptools)
library(hydroGOF)
library(plotrix)
library(lattice)
##Script to compare observed and simulated flow for a number of locations.
##arthurlutz 20161110

###INSTRUCTIONS
#Run SPHY for 2001-2007
#Report tss files for all runoff components
###INSTRUCTIONS END

###SETTINGS
indir <- "C:\\SPHY\\model\\output\\"
outdir <- "C:\\SPHY\\analysis\\discharge\\"
qobs <- "Y:\\himalayan Ganga\\sphy_dec_2016\\Himalayan_Ganga_CWC_combined.csv"
###SETTINGS END


# extract timesteps and dates to process
dates<-seq(as.Date("1986-01-01"),as.Date("2000-12-31"),"day")
#dates<- dates[-which(substr(dates,6,10)=="02-29")]
timesteps <- 1:length(dates)
datesframe <- matrix(data=NA,nrow=length(dates),ncol=4)
datesframe[,1] <- timesteps
for (i in timesteps)
	{
		datesframe[i,2] <- as.numeric(format(dates[i], "%Y"))
		datesframe[i,3] <- as.numeric(format(dates[i], "%m"))
		datesframe[i,4] <- as.numeric(format(dates[i], "%d"))
	}


##load observed Q data
qobs_read <- read.csv(qobs, header=T)

##read simulated Q data and couple to dates
qall <- paste(indir,"QallDTS.tss",sep="")
qglac <-  paste(indir,"GTotDTS.tss",sep="")
qsnow <-  paste(indir,"STotDTS.tss",sep="")
qrain <-  paste(indir,"RTotDTS.tss",sep="")
qbase <-  paste(indir,"BTotDTS.tss",sep="")

qall2 <- read.delim(qall,skip=10,sep="",header=F)
qglac2 <- read.delim(qglac,skip=10,sep="",header=F)
qsnow2 <- read.delim(qsnow,skip=10,sep="",header=F)
qrain2 <- read.delim(qrain,skip=10,sep="",header=F)
qbase2 <- read.delim(qbase,skip=10,sep="",header=F)

qall3 <- cbind(datesframe[,1:4],qall2[,2:8])
qglac3 <- cbind(datesframe[,1:4],qglac2[,2:8])
qsnow3 <- cbind(datesframe[,1:4],qsnow2[,2:8])
qrain3 <- cbind(datesframe[,1:4],qrain2[,2:8])
qbase3 <- cbind(datesframe[,1:4],qbase2[,2:8])


##loop over locations and write plot and correlation

pdf(file=paste(outdir,"plots.pdf",sep=""),width=14)

for (i in 2:6)
{
  #get obs and sim q
  obs_q <- as.data.frame(as.numeric(qobs_read[,i+2]))
  obs_q <- as.data.frame(obs_q[8:67,])
  
  sim_q <- as.data.frame(qall3[,i+4])
  sim_qbase <- as.data.frame(qbase3[,i+4])
  sim_qglac <- as.data.frame(qglac3[,i+4])
  sim_qsnow <- as.data.frame(qsnow3[,i+4])
  sim_qrain <- as.data.frame(qrain3[,i+4])
  
  
  #plot daily discharge
  #x<- cbind(sim_qbase,sim_qglac,sim_qsnow,sim_qrain)
  #areacolors <- c("Indian red1","lightskyblue", "sandybrown","palegreen3")
  #stackpoly(x,y=NULL,xlab="",ylab="", col=areacolors, stack=TRUE, xlim=c(1,2556),axis4=FALSE,cex.axis=2)
  
  #points(x=1:2556,y=obs_q[,1], type="p", pch=20,cex=0.7, col='blue')
  #fit_d <- gof(sim_q,obs_q, na.rm=T)
  
  #aggregate to monthly
  df <- cbind(datesframe[,2:3],sim_q,sim_qbase,sim_qglac,sim_qsnow,sim_qrain)
  aggdata <- aggregate(cbind(df[,1],df[,2],df[,3],df[,4],df[,5],df[,6],df[,7])~df[,2]+df[,1],data=df,FUN=mean)
  aggdata <- cbind(aggdata,obs_q)
  
  #plot and calculate correlation  
  fit_m <- gof(aggdata[,5],aggdata[,10],na.rm=T)
  x<- cbind(aggdata[,6],aggdata[,7],aggdata[,8],aggdata[,9])
  areacolors <- c("Indian red1","lightskyblue", "sandybrown","palegreen3")
  stackpoly(x,y=NULL,xlab="",ylab="", col=areacolors, stack=TRUE, xlim=c(1,60),axis4=FALSE,cex.axis=2)
  lines(x=1:60,y=aggdata[,10], type="l",col='red')
  #lines(x=1:300,y=aggdata[,5],type="l",pch=20,cex=0.7, col='blue')
  mtext(paste("NSE = ",fit_m[9,1],"; R2 = ",fit_m[17,1],"; bias = ",fit_m[6,1],sep=""),side=3,line=-1)
}
dev.off()
 
  
  

