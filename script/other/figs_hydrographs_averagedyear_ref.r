# arthurlutz , 20141013
#script to generate hydrographs averaged over multiple years
rm(list = ls())
library(plotrix)
library(lattice)
library(ggplot2)
library(Cairo)
library(Hmisc)

################################# SETTINGS #################################

# indirs
sourcedir <- c('c:/Active/2013_014_Indus/Model/SPHY_PYTHON/output/')

#models <- c('CanESM2_rcp45','CSIRO_Mk3_6_0_rcp85','IPSL_CM5A_LR_rcp45','IPSL_CM5A_LR_rcp85','MIROC5_rcp85','MPI_ESM_LR_rcp85','MRI_CGCM3_rcp45')
models <- c('final')

			   
loaddata <- T
required_tss_line_skip = 33
#polycols = c(rgb(0,0.0,0.85), rgb(0.85,0.0,0.0), rgb(0.0,0.85,0.0), rgb(0.8,0.0,0.8))
polycols = c(rgb(255,153,153, maxColorValue=255), rgb(153,255,255, maxColorValue=255), rgb(255,153,51,  maxColorValue=255), rgb(0,153,0,  maxColorValue=255))

selected_basins = c(2,5,30,6,8)
basinnames <- c('Indus - Tarbela','Kabul - Nowshera','Satluj','Hunza - Dainyor bridge','Indus - Skardu')

# pdfout
pdfout <- F
pdfpath <- 'C:/Active/2013_014_Indus/Analysis/discharge/plots/'

startyear <- 1971
endyear <- 2000

xlabels <- c('J','F','M','A','M','J','J','A','S','O','N','D')

############################################################################

# get vector of dates with removed leap days
dates <- seq(as.Date('1961-01-01'),as.Date('2007-12-31'),by='day')
dates <- dates[-which(substr(dates,6,11)=="02-29")]
yearvec  <- as.numeric(substr(dates,1,4))
years <- as.numeric(unique(substr(dates,1,4)))
monthvec <- as.numeric(substr(dates,6,7))
months <- as.numeric(unique(substr(dates,6,7)))

# initialize polygon border array
polyborarr = array(NA,dim=c(length(months),5,length(selected_basins),length(models)))

#move 2 places in selected basins
selected_basins = as.integer(selected_basins+2)

if (loaddata){
  for (m in 1:length(models)){
  
    setwd(paste(sourcedir,"//",models[m],sep=""))
    qall <- read.table('TQRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    glacr <- read.table('TGRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    snowr <- read.table('TSRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    rainr <- read.table('TRRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    baser <- read.table('TBRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
	
	#add year and month to tables and filter years
	qall<-cbind(yearvec,monthvec,qall)
	glacr<-cbind(yearvec,monthvec,glacr)
	snowr<-cbind(yearvec,monthvec,snowr)
	rainr<-cbind(yearvec,monthvec,rainr)
	baser<-cbind(yearvec,monthvec,baser)
	qall<-qall[qall$yearvec %in% (startyear:endyear),]
	glacr<-glacr[glacr$yearvec %in% (startyear:endyear),]
	snowr<-snowr[snowr$yearvec %in% (startyear:endyear),]
	rainr<-rainr[rainr$yearvec %in% (startyear:endyear),]
	baser<-baser[baser$yearvec %in% (startyear:endyear),]
    
	#update monthvec
	monthvec <- qall[,2]
	
    # aggregate data to months
    qall_mo  <- aggregate(x=qall,by=list(monthvec),FUN=mean)[,-1];
    glacr_mo <- aggregate(x=glacr,by=list(monthvec),FUN=mean)[,-1];
    snowr_mo <- aggregate(x=snowr,by=list(monthvec),FUN=mean)[,-1];
    rainr_mo <- aggregate(x=rainr,by=list(monthvec),FUN=mean)[,-1];
    baser_mo <- aggregate(x=baser,by=list(monthvec),FUN=mean)[,-1];

    # create stacked polygon data
    polyborarr[,1,,m] <- 0;
    polyborarr[,2,,m] <- as.matrix(baser_mo[,selected_basins]) + polyborarr[,1,,m]
    polyborarr[,3,,m] <- as.matrix(glacr_mo[,selected_basins]) + polyborarr[,2,,m]
    polyborarr[,4,,m] <- as.matrix(snowr_mo[,selected_basins]) + polyborarr[,3,,m]
    polyborarr[,5,,m] <- as.matrix(rainr_mo[,selected_basins]) + polyborarr[,4,,m]
  }
}


poly_borders = apply(polyborarr,MARGIN=c(1,2,3),FUN=mean)

# create pdf
if (pdfout){
  for (m in 1:length(models))
  {
  	poly_borders = polyborarr[,,,m]
  
  pdf(file=paste(pdfpath,"//",models[m],"_Q.pdf",sep=""), width=0, height=0, paper='a4r',pointsize=7,colormodel='srgb')
  layout(mat=matrix(1,ncol=1,nrow=1),heights=lcm(7), widths=lcm(15))
  
  
   par(mar=c(3.5,4.75,2,1.5))
	par(mfrow=c(2,3))
  # loop over basins
  for (b in 1:length(basinnames)){
  
    # Plotting
   
    plotperiod <- 1:dim(qall_mo)[1]
    ym = max(poly_borders[,,b])
   	ym = ym * 1.2
    
    # initialize plot
    ylabel = expression(paste(text="Q (","m"^scriptscriptstyle(3)," s"^scriptscriptstyle(-1),")",sep=""))
    plot(NA, xlim=c(plotperiod[1],tail(plotperiod,1)), ylim=c(0,ym), ylab=ylabel, xlab= '',xaxs='i',xaxt='n',yaxs='i',main=paste('Q ',basinnames[b]," 1971-2000",sep=""))
    axis(1,at=seq(1,12,1),tck=-0.02,labels=xlabels,col="black")
    axis(1,at=seq(0,100,1),tck=-0.0075,labels=NA,col="black")
    
    # plot the polygons
    polyx = c(1:dim(poly_borders)[1],dim(poly_borders)[1]:1)
    for (i in 1:(dim(poly_borders)[2]-1)){
      polygon(polyx,c(poly_borders[,i,b],rev(poly_borders[,i+1,b])),col=polycols[i],border=polycols[i]);
    }
	axis(1,at=c(-1e99,1e99),labels=NA);axis(2,at=c(-1e99,1e99),labels=NA);axis(3,at=c(-1e99,1e99),labels=NA);axis(4,at=c(-1e99,1e99),labels=NA)
    
	mp<-matrix(c(1:12),nrow=12,ncol=1)
	#mtext(text = xlabels, side = 1, at = mp, line = 0.7, cex=0.75)
	
    # add legend
    #legend(x='top',horiz=T,inset=0.01,legend=c('Base flow','Glacier melt','Snow melt','Rainfall'),fill=polycols,bty='n',cex=1)
    
    } # end basin loop
	
	plot('')
	legend(x='center',horiz=F,inset=0.01,legend=c('Base flow','Glacier melt','Snow melt','Rainfall'),fill=polycols,bty='n',cex=1.2)
	
	dev.off()
	
  } # end pdfout if


  
}


