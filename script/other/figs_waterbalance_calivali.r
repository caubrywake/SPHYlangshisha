rm(list = ls())
library(raster)
library(reshape2)
library(ggplot2)
library(hydroGOF)

###settings
calculateP <- F
calculateET <- F
calculateSubl <- T
catchdir <- "e:\\Active\\2013_014_Indus\\Data\\runoff\\subcatchments\\"
precdir <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\input\\prec\\"
modeloutputdir <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\output\\final2\\"
qall <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\output\\final2\\TQRADTS.tss"
qglac <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\output\\final2\\TGRADTS.tss"
qsnow <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\output\\final2\\TSRADTS.tss"
qrain <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\output\\final2\\TRRADTS.tss"
qbase <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\output\\final2\\TBRADTS.tss"
glacfrac <- raster("e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\input\\glacfrac.map")
outdir <- "e:\\Active\\2013_014_Indus\\Data\\paper_figs\\waterbalance\\"
qobs <- read.csv("e:\\Active\\2013_014_Indus\\Data\\runoff\\calivali_runoff_obs.csv")
sitenames <- c('Besham Qila - Indus','Mangla - Jhelum','Dainyor Bridge - Hunza','Tarbela - Indus','Marala - Chenab', 'Nowshera - Kabul')
#sitenames <- c('Besham Qila - Indus')

startdates <- c('2000-01-01','1976-04-01','1966-01-01','1976-04-01','1976-04-01','1976-04-01')
enddates <- c('2007-12-31','2007-12-31','2004-12-31','2007-12-31','2007-12-31','2007-12-31')
colids <- c(1,3,6,2,4,5)
dummygrid <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\input\\clonezero.map"
workdir <- "C:\\workdir\\"
ndays<-c(31,28,31,30,31,30,31,31,30,31,30,31)
monthly_lookup <- read.csv("e:\\Active\\2013_014_Indus\\Scripts\\runoff\\monthly_output_timesteps.csv",header=F)

###settings end

# extract timesteps and dates to process
dates<-seq(as.Date("1961-01-01"),as.Date("2007-12-31"),"day")
dates<- dates[-which(substr(dates,6,10)=="02-29")]
timesteps <- 1:17155
datesframe <- matrix(data=NA,nrow=17155,ncol=4)
datesframe[,1] <- timesteps
for (i in timesteps)
	{
		datesframe[i,2] <- as.numeric(format(dates[i], "%Y"))
		datesframe[i,3] <- as.numeric(format(dates[i], "%m"))
		datesframe[i,4] <- as.numeric(format(dates[i], "%d"))
	}
#dates<-datesframe[which(datesframe[,2] >= startyear & datesframe[,2] <= endyear),]


##load observed Q data, remove leap days and couple to timesteps
qobs2 <- qobs[-which(qobs[,3]==2 & qobs[,4]==29),]
qobs3 <- matrix(data=NA,nrow=nrow(qobs2),ncol=1)
qobs3[,1] <- 1:17155
qobs4 <- cbind(qobs3,qobs2)

#load simulated Q data and couple to dates
qall2 <- read.delim(qall,skip=33,sep="",header=F)
qglac2 <- read.delim(qglac,skip=33,sep="",header=F)
qsnow2 <- read.delim(qsnow,skip=33,sep="",header=F)
qrain2 <- read.delim(qrain,skip=33,sep="",header=F)
qbase2 <- read.delim(qbase,skip=33,sep="",header=F)

qall3 <- cbind(datesframe[,1:4],qall2[,2:31])
qglac3 <- cbind(datesframe[,1:4],qglac2[,2:31])
qsnow3 <- cbind(datesframe[,1:4],qsnow2[,2:31])
qrain3 <- cbind(datesframe[,1:4],qrain2[,2:31])
qbase3 <- cbind(datesframe[,1:4],qbase2[,2:31])

#couple obs and sim data and calculate daily and monthly correlation coefficients


df <- matrix(data=NA,nrow=length(sitenames),ncol=4)
df_m <- matrix(data=NA,nrow=length(sitenames),ncol=4)
for (i in 1:length(sitenames))
{
  data <- cbind(qobs4[,1:5],qobs4[,5+i],qall3[,4+colids[i]])
  startts <- as.numeric(qobs4[qobs4[,2] == startdates[i], 1])
  endts <- as.numeric(qobs4[qobs4[,2] == enddates[i], 1])
  data <- data[-which(data[,1] < startts | data[,1] > endts),]
  cor <- gof(obs=data[,6],sim=data[,7])
  df[i,1]<-sitenames[i]
  df[i,2]<-cor[9]
  df[i,3]<-cor[16]
  df[i,4]<-cor[6]
  
  ##monthly
  aggdata <- aggregate(cbind(data[,6],data[,7])~data[,3]+data[,4], data=data,FUN=mean)
  cor <- gof(obs=aggdata[,3],sim=aggdata[,4])
  df_m[i,1]<-sitenames[i]
  df_m[i,2]<-cor[9]
  df_m[i,3]<-cor[16]
  df_m[i,4]<-cor[6]
 }
colnames(df)<-c('site','NSE','Pearson','Pbias')
write.csv(df,file=paste(outdir,"correlation_daily.csv",sep=""))
colnames(df_m)<-c('site','NSE','Pearson','Pbias')
write.csv(df_m,file=paste(outdir,"correlation_monthly.csv",sep=""))


##loop over sites
for(i in 1:length(sitenames))
{
   ##calculate average sim (incl contributions) and obs flow per month in mm
  data <- cbind(qobs4[,1:5],qobs4[,5+i],qall3[,4+colids[i]],qglac3[,4+colids[i]],qsnow3[,4+colids[i]],qrain3[,4+colids[i]],qbase3[,4+colids[i]])
  startts <- as.numeric(qobs4[qobs4[,2] == startdates[i], 1])
  endts <- as.numeric(qobs4[qobs4[,2] == enddates[i], 1])
  data <- data[-which(data[,1] < startts | data[,1] > endts),]
  aggdata <- aggregate(cbind(data[,6],data[,7],data[,8],data[,9],data[,10],data[,11])~data[,4], data=data,FUN=mean)
  
  ##load catchment map to get area
  zone <- raster(paste(catchdir,"subcatchment",colids[i],".map",sep=""))
  zone[zone != 1] <- NA
  #area incl glacfrac
  area_incl <- zonal(zone,zone,fun='sum')[2]
  
  ##convert m3/s to mm/month
  aggdata[,2:7] <- aggdata[,2:7] * (((3600*24*30.42)/1000) / area_incl)
  
  colnames(aggdata)<-c('month','qobs','qsim','qglac','qsnow','qrain','qbase')
  write.csv(aggdata,file=paste(outdir,sitenames[i],"Q.csv",sep=""))
  
  
  ##area without glacfrac
  areamap <- zone-glacfrac
  area <- zonal(areamap,zone,fun='sum')[2]
  
  
  ##calculate monthly P
  if(calculateP==T)
    {
  ##initiate dataframe to store data
  df <- matrix(data=NA,nrow=12,ncol=3)
  pzonal<-c()
  for(x in 1:12)
  {
    #create grid to sum precipitation to
    command <- paste("pcrcalc ",workdir,"psum.map = ",dummygrid,sep="")
    system(command)
    
    #filter data for month
    data_m <- data[-which(data[,4] != x),]
    
    for (z in 1:nrow(data_m))
    {
      timestep <- sprintf("%07d", data_m[z,1])
      pcrno <- paste(substr(timestep,1,4),".",substr(timestep,5,7),sep="")
      command <- paste("pcrcalc ",workdir,"psum.map = ",workdir,"psum.map + ",precdir,"prec",pcrno,sep="")
      system(command)
    }
    psum <- raster(paste(workdir,"psum.map",sep=""))
    pavg <- (psum / nrow(data_m)) * ndays[x]
    pzonal[x] <- zonal(pavg,zone,fun='mean')[2]
  }
  df[,1]<-sitenames[i]
  df[,2]<-1:12
  df[,3]<-pzonal[1:12]
  write.csv(df,file=paste(outdir,i,"Pavg.csv",sep=""))
  }
  
  ##calculate monthly ETa
  if(calculateET==T)
  {
  df <- matrix(data=NA,nrow=12*length(sitenames),ncol=3)
  etazonal<-c()
  for(x in 1:12)
  {
    #create grid to sum ETa to
    command <- paste("pcrcalc ",workdir,"etasum.map = ",dummygrid,sep="")
    system(command)
    
    timesteps <- monthly_lookup[-which(monthly_lookup[,3] != x),]
    
    for(z in 1:nrow(timesteps))
    {
      timestep <- sprintf("%06d", timesteps[z,1])
      pcrno <- paste(substr(timestep,1,3),".",substr(timestep,4,6),sep="")
      command <- paste("pcrcalc ",workdir,"etasum.map = ",workdir,"etasum.map + ",modeloutputdir,"TETaM",pcrno,sep="")
      system(command)
    }
    etasum <- raster(paste(workdir,"etasum.map",sep=""))
    etaavg <- etasum/nrow(timesteps)
    eta_spatsum <- zonal(etaavg,zone,fun='sum')[2]
    etazonal[x] <- eta_spatsum/area
  
  }
  df[,1]<-sitenames[i]
  df[,2]<-1:12
  df[,3]<-etazonal[1:12]
  write.csv(df,file=paste(outdir,i,"ETaavg.csv",sep=""))
  
  }
  
  ##calculate monthly Sublimation
  if(calculateSubl==T)
  {
  df <- matrix(data=NA,nrow=12*length(sitenames),ncol=3)
  subzonal<-c()
  for(x in 1:12)
  {
    #create grid to sum sublimation to
    command <- paste("pcrcalc ",workdir,"subsum.map = ",dummygrid,sep="")
    system(command)
    
    timesteps <- monthly_lookup[-which(monthly_lookup[,3] != x),]
    
    for(z in 1:nrow(timesteps))
    {
      timestep <- sprintf("%06d", timesteps[z,1])
      pcrno <- paste(substr(timestep,1,3),".",substr(timestep,4,6),sep="")
      command <- paste("pcrcalc ",workdir,"subsum.map = ",workdir,"subsum.map + ",modeloutputdir,"TSUaM",pcrno,sep="")
      system(command)
    }
    subsum <- raster(paste(workdir,"subsum.map",sep=""))
    subavg <- subsum/nrow(timesteps)
    sub_spatsum <- zonal(subavg,zone,fun='sum')[2]
    subzonal[x] <- sub_spatsum/area
  
  }
  df[,1]<-sitenames[i]
  df[,2]<-1:12
  df[,3]<-subzonal[1:12]
  write.csv(df,file=paste(outdir,i,"SUaavg.csv",sep=""))
  
  }
  
}

