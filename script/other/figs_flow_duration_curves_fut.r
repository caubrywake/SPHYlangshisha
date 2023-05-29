# arthurlutz , 20141016
#script to generate flow duration curves
rm(list = ls())
library(plotrix)
library(lattice)
library(ggplot2)
library(Cairo)
library(Hmisc)
library(abind)

################################# SETTINGS #################################

# indirs
sourcedir <- c('c:/Active/2013_014_Indus/Model/SPHY_PYTHON/output_cc/')
refdir <- c('c:/Active/2013_014_Indus/Model/SPHY_PYTHON/output/final/')

#select rcp and models
rcp = "RCP8.5"
#models <- c('CanESM2_rcp45','IPSL_CM5A_LR_rcp45','inmcm4_rcp45','MRI_CGCM3_rcp45')
models <- c('CSIRO_Mk3_6_0_rcp85','IPSL_CM5A_LR_rcp85','MIROC5_rcp85','MPI_ESM_LR_rcp85')

loaddata <- T
required_tss_line_skip = 33

selected_basins = c(2,5,30,6,8)
basinnames <- c('Indus - Tarbela','Kabul - Nowshera','Satluj','Hunza - Dainyor bridge','Indus - Skardu')

# start and endyear future period
startyear <- 2071
endyear <- 2100

# start and endyear reference period
startyear_ref <- 1971
endyear_ref <- 2000

csvfile <- paste("c:\\Active\\2013_014_Indus\\Analysis\\discharge\\discharge_quantiles\\discharge_quantiles2\\",rcp,"_",startyear,"_",endyear,".csv",sep="")

#line colors
colors <- c('black','deepskyblue','firebrick','forestgreen','orange')

#legend title
legendtitle <- paste(rcp, " ",startyear,"-",endyear,sep="")

#additional lines (line=horizontal, vline=vertical)
linea <- 20
lineb <- 50
linec <- 100
lined <- 200
linee <- 500
linef <- 1000
lineg <- 5000
vlinea <- 10
vlineb <- 25
vlinec <- 50
vlined <- 75
vlinee <- 90
vlinef <- 0
vlineg <- 100


############################################################################
##process reference data
# get vector of dates with removed leap days
dates <- seq(as.Date('1961-01-01'),as.Date('2007-12-31'),by='day')
dates <- dates[-which(substr(dates,6,11)=="02-29")]
yearvec  <- as.numeric(substr(dates,1,4))
years <- as.numeric(unique(substr(dates,1,4)))
monthvec <- as.numeric(substr(dates,6,7))
months <- as.numeric(unique(substr(dates,6,7)))


#move 2 places in selected basins
selected_basins_ref = as.integer(selected_basins+2)

if (loaddata){
    setwd(paste(refdir,sep=""))
    m<-1
    qall <- read.table('TQRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    #glacr <- read.table('TGRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    #snowr <- read.table('TSRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    #rainr <- read.table('TRRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    #baser <- read.table('TBRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    
    #add year and month to tables and filter years
    qall<-cbind(yearvec,monthvec,qall)
    #glacr<-cbind(yearvec,monthvec,glacr)
    #snowr<-cbind(yearvec,monthvec,snowr)
    #rainr<-cbind(yearvec,monthvec,rainr)
    #baser<-cbind(yearvec,monthvec,baser)
    qall_ref<-qall[qall$yearvec %in% (startyear_ref:endyear_ref),]
    #glacr_ref<-glacr[glacr$yearvec %in% (startyear_ref:endyear_ref),]
    #snowr_ref<-snowr[snowr$yearvec %in% (startyear_ref:endyear_ref),]
    #rainr_ref<-rainr[rainr$yearvec %in% (startyear_ref:endyear_ref),]
    #baser_ref<-baser[baser$yearvec %in% (startyear_ref:endyear_ref),]
}


###process future data
# get vector of dates with removed leap days
dates <- seq(as.Date('2001-01-01'),as.Date('2100-12-31'),by='day')
dates <- dates[-which(substr(dates,6,11)=="02-29")]
yearvec  <- as.numeric(substr(dates,1,4))
years <- as.numeric(unique(substr(dates,1,4)))
monthvec <- as.numeric(substr(dates,6,7))
months <- as.numeric(unique(substr(dates,6,7)))


#move 2 places in selected basins
selected_basins = as.integer(selected_basins+2)

# initialize array for all data
all_data  <- qall_ref

if (loaddata){
  for (m in 1:length(models)){
  
    setwd(paste(sourcedir,"//",models[m],sep=""))
    qall <- read.table('TQRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    #glacr <- read.table('TGRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    #snowr <- read.table('TSRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    #rainr <- read.table('TRRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    #baser <- read.table('TBRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    
    	
	#add year and month to tables and filter years
	qall<-cbind(yearvec,monthvec,qall)
	#glacr<-cbind(yearvec,monthvec,glacr)
	#snowr<-cbind(yearvec,monthvec,snowr)
	#rainr<-cbind(yearvec,monthvec,rainr)
	#baser<-cbind(yearvec,monthvec,baser)
	qall<-qall[qall$yearvec %in% (startyear:endyear),]
	#glacr<-glacr[glacr$yearvec %in% (startyear:endyear),]
	#snowr<-snowr[snowr$yearvec %in% (startyear:endyear),]
	#rainr<-rainr[rainr$yearvec %in% (startyear:endyear),]
	#baser<-baser[baser$yearvec %in% (startyear:endyear),]
    
	# add data to array
	all_data <- abind(all_data,qall,along=3)
   
  }
}

# filter for selected basins
data_sel <- all_data[,selected_basins,]

#initiate dataframe for quantiles
df <- data.frame(matrix(ncol = 8, nrow = (length(models)+1)*length(selected_basins)))

# calculate quantiles
row<-1
for (a in 1:length(selected_basins))
{
  for (mod in 1:(length(models)+1))
  {
    quantiles <- quantile(data_sel[,a,mod], probs=c(0.5,0.75,0.9,0.95,0.99))
    df[row,1]<-basinnames[a]
    df[row,2]<-rcp
    if(mod==1){model <- "Reference"}
    if(mod!=1){model<-models[mod-1]}
    df[row,3]<-model
    df[row,4]<-quantiles[1]
    df[row,5]<-quantiles[2]
    df[row,6]<-quantiles[3]
    df[row,7]<-quantiles[4]
    df[row,8]<-quantiles[5]
    row<-row+1
  }
}
#write csv
write.csv(df,csvfile)



# create plots
  par(mar=c(3.5,4.75,2,1.5))
	par(mfrow=c(3,2))
  # loop over basins
  for (b in 1:length(basinnames))
    {
      #sort data
      data <- data_sel[,b,]
      for (v in 1:5)
        {
          data[,v] <- sort(data[,v], decreasing=TRUE)
        }
      probabilities <- c(1:10950) / 109.5
      data2 <- cbind(probabilities,data)
      ylabel = expression(paste(text="Daily Q (","m"^scriptscriptstyle(3)," s"^scriptscriptstyle(-1),")",sep=""))
      # Plotting
      for (z in 1:5)
      {
        print(z)
        x <- data2[,1]
        y <- data2[,(z+1)]
        if (z == 1)
          {
            plot(xy.coords(x,y), type="l", col=colors[z], xlim=c(0,100), ylim=c(min(data2[,2:6]),max(data2)), log="y", xlab="", ylab="")
            title(main=basinnames[b])
            mtext("Flow exceedance percentile", side=1, line=2, cex=0.8)
            mtext(ylabel, side=2, line=1.9, cex=0.8)
            abline(a=linea,b=0, lty=2, col="darkgrey", untf=TRUE)
            abline(a=lineb,b=0, lty=2, col="darkgrey", untf=TRUE)
            abline(a=linec,b=0, lty=2, col="darkgrey", untf=TRUE)
            abline(a=lined,b=0, lty=2, col="darkgrey", untf=TRUE)
            abline(a=linee,b=0, lty=2, col="darkgrey", untf=TRUE)
            abline(a=linef,b=0, lty=2, col="darkgrey", untf=TRUE)
            abline(a=lineg,b=0, lty=2, col="darkgrey", untf=TRUE)
            abline(a=vlinea,b=0, lty=2, col="darkgrey", v=vlinea)
            abline(a=vlinea,b=0, lty=2, col="darkgrey", v=vlineb)
            abline(a=vlinea,b=0, lty=2, col="darkgrey", v=vlinec)
            abline(a=vlinea,b=0, lty=2, col="darkgrey", v=vlined)
            abline(a=vlinea,b=0, lty=2, col="darkgrey", v=vlinee)
            abline(a=vlinea,b=0, lty=2, col="darkgrey", v=vlinef)
            abline(a=vlinea,b=0, lty=2, col="darkgrey", v=vlineg)
          }
        if (z > 1)
          {
            plot(xy.coords(x,y), type="l", col=colors[z], xlim=c(0,100), ylim=c(min(data2[,2:6]),max(data2)), log="y", axes="F",xlab="",ylab="")
          }
        if(z != length(models)+1)
        {
          par(new=T)
        }
        
       
    }
  }
plot('')
mtext(legendtitle, side=3, line=-2, cex=1)
legend(x='center',horiz=F,inset=0.01,legend=c('Reference 1971-2000',models),lty=c(1,1,1,1,1),col=colors ,cex=1.2)




   