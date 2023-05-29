# arthurlutz , 20141013
#script to generate hydrographs averaged over multiple years
rm(list = ls())
library(plotrix)
library(lattice)
library(ggplot2)
library(Cairo)
library(Hmisc)
library(gdata)
library(abind)
################################# SETTINGS #################################

# indirs
sourcedir <- c('c:/Active/2013_014_Indus/Model/SPHY_PYTHON/output_cc/')
refdir <- c('c:/Active/2013_014_Indus/Model/SPHY_PYTHON/output/final/')

#models <- c('CanESM2_rcp45','IPSL_CM5A_LR_rcp45','inmcm4_rcp45','MRI_CGCM3_rcp45')
models <- c('CSIRO_Mk3_6_0_rcp85','IPSL_CM5A_LR_rcp85','MIROC5_rcp85','MPI_ESM_LR_rcp85')

			   
loaddata <- T
required_tss_line_skip = 33
#polycols = c(rgb(0,0.0,0.85), rgb(0.85,0.0,0.0), rgb(0.0,0.85,0.0), rgb(0.8,0.0,0.8))
polycols = c(rgb(255,153,153, maxColorValue=255), rgb(153,255,255, maxColorValue=255), rgb(255,153,51,  maxColorValue=255), rgb(0,153,0,  maxColorValue=255))

selected_basins = c(2,5,30,6,8)
basinnames <- c('Indus - Tarbela','Kabul - Nowshera','Satluj','Hunza - Dainyor bridge','Indus - Skardu')

# pdfout
pdfout <- F
pdfpath <- 'C:/Active/2013_014_Indus/Analysis/discharge/plots/'

startyear <- 2001
endyear <- 2100

startyear_ref <- 1961
endyear_ref <- 2000



############################################################################
##process reference data
# get vector of dates with removed leap days
dates <- seq(as.Date('1961-01-01'),as.Date('2007-12-31'),by='day')
dates <- dates[-which(substr(dates,6,11)=="02-29")]
yearvec  <- as.numeric(substr(dates,1,4))
years <- as.numeric(unique(substr(dates,1,4)))

# initialize polygon border array
polyborarr = array(NA,dim=c((endyear_ref-startyear_ref)+1,5,length(selected_basins),1))

#move 2 places in selected basins
selected_basins_ref = as.integer(selected_basins+1)

if (loaddata){
    setwd(paste(refdir,sep=""))
    m<-1
    qall <- read.table('TQRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    glacr <- read.table('TGRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    snowr <- read.table('TSRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    rainr <- read.table('TRRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    baser <- read.table('TBRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    
    #add year to tables and filter years
    qall<-cbind(yearvec,qall)
    glacr<-cbind(yearvec,glacr)
    snowr<-cbind(yearvec,snowr)
    rainr<-cbind(yearvec,rainr)
    baser<-cbind(yearvec,baser)
    qall<-qall[qall$yearvec %in% (startyear_ref:endyear_ref),]
    glacr<-glacr[glacr$yearvec %in% (startyear_ref:endyear_ref),]
    snowr<-snowr[snowr$yearvec %in% (startyear_ref:endyear_ref),]
    rainr<-rainr[rainr$yearvec %in% (startyear_ref:endyear_ref),]
    baser<-baser[baser$yearvec %in% (startyear_ref:endyear_ref),]
    
    #update yearvec
    yearvec2 <- qall[,1]
    
    # aggregate data to years
    qall_yr  <- aggregate(x=qall,by=list(yearvec2),FUN=mean)[,-1];
    glacr_yr <- aggregate(x=glacr,by=list(yearvec2),FUN=mean)[,-1];
    snowr_yr <- aggregate(x=snowr,by=list(yearvec2),FUN=mean)[,-1];
    rainr_yr <- aggregate(x=rainr,by=list(yearvec2),FUN=mean)[,-1];
    baser_yr <- aggregate(x=baser,by=list(yearvec2),FUN=mean)[,-1];
    
    # create stacked polygon data
    polyborarr[,1,,m] <- 0;
    polyborarr[,2,,m] <- as.matrix(baser_yr[,selected_basins_ref]) + polyborarr[,1,,m]
    polyborarr[,3,,m] <- as.matrix(glacr_yr[,selected_basins_ref]) + polyborarr[,2,,m]
    polyborarr[,4,,m] <- as.matrix(snowr_yr[,selected_basins_ref]) + polyborarr[,3,,m]
    polyborarr[,5,,m] <- as.matrix(rainr_yr[,selected_basins_ref]) + polyborarr[,4,,m]

    polyborarr_ref <- polyborarr
}
poly_borders_ref = apply(polyborarr_ref,MARGIN=c(1,2,3),FUN=mean)

###process future data
# get vector of dates with removed leap days
dates <- seq(as.Date('2001-01-01'),as.Date('2100-12-31'),by='day')
dates <- dates[-which(substr(dates,6,11)=="02-29")]
yearvec  <- as.numeric(substr(dates,1,4))
years <- as.numeric(unique(substr(dates,1,4)))

# initialize polygon border array
polyborarr = array(NA,dim=c(length(years),5,length(selected_basins),length(models)))

#move 2 places in selected basins
selected_basins = as.integer(selected_basins+1)

if (loaddata){
  for (m in 1:length(models)){
  
    setwd(paste(sourcedir,"//",models[m],sep=""))
    qall <- read.table('TQRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    glacr <- read.table('TGRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    snowr <- read.table('TSRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    rainr <- read.table('TRRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    baser <- read.table('TBRADTS.tss',skip=required_tss_line_skip, header=F)[,-1]
    
    	
	#add year and month to tables and filter years
	qall<-cbind(yearvec,qall)
	glacr<-cbind(yearvec,glacr)
	snowr<-cbind(yearvec,snowr)
	rainr<-cbind(yearvec,rainr)
	baser<-cbind(yearvec,baser)
	qall<-qall[qall$yearvec %in% (startyear:endyear),]
	glacr<-glacr[glacr$yearvec %in% (startyear:endyear),]
	snowr<-snowr[snowr$yearvec %in% (startyear:endyear),]
	rainr<-rainr[rainr$yearvec %in% (startyear:endyear),]
	baser<-baser[baser$yearvec %in% (startyear:endyear),]
    
	
    # aggregate data to years
    qall_yr  <- aggregate(x=qall,by=list(yearvec),FUN=mean)[,-1];
    glacr_yr <- aggregate(x=glacr,by=list(yearvec),FUN=mean)[,-1];
    snowr_yr <- aggregate(x=snowr,by=list(yearvec),FUN=mean)[,-1];
    rainr_yr <- aggregate(x=rainr,by=list(yearvec),FUN=mean)[,-1];
    baser_yr <- aggregate(x=baser,by=list(yearvec),FUN=mean)[,-1];

    # create stacked polygon data
    polyborarr[,1,,m] <- 0;
    polyborarr[,2,,m] <- as.matrix(baser_yr[,selected_basins]) + polyborarr[,1,,m]
    polyborarr[,3,,m] <- as.matrix(glacr_yr[,selected_basins]) + polyborarr[,2,,m]
    polyborarr[,4,,m] <- as.matrix(snowr_yr[,selected_basins]) + polyborarr[,3,,m]
    polyborarr[,5,,m] <- as.matrix(rainr_yr[,selected_basins]) + polyborarr[,4,,m]
  }
}


poly_borders = apply(polyborarr,MARGIN=c(1,2,3),FUN=mean)
#poly_borders_max = apply(polyborarr,MARGIN=c(1,2,3),FUN=max)
#poly_borders_min = apply(polyborarr,MARGIN=c(1,2,3),FUN=min)

#concatenate reference and future
poly_borders_all <- abind(poly_borders_ref,poly_borders,along=1)
poly_borders_max <- apply(polyborarr,MARGIN=c(1,2,3),FUN=max)
poly_borders_min <- apply(polyborarr,MARGIN=c(1,2,3),FUN=min)

# create pdf
if (pdfout){
  for (m in 1:length(models))
  {
  	poly_borders = polyborarr[,,,m]
  
  pdf(file=paste(pdfpath,"//",models[m],"_Q.pdf",sep=""), width=0, height=0, paper='a4r',pointsize=7,colormodel='srgb')
  layout(mat=matrix(1,ncol=1,nrow=1),heights=lcm(7), widths=lcm(15))
  
  
  par(mar=c(3.5,4.75,2,1.5))
	par(mfrow=c(5,1))
  # loop over basins
  for (b in 1:length(basinnames)){
  
    # Plotting
   
    plotperiod <- 1:dim(poly_borders_all)[1]
    ym = max(poly_borders_max[,,b])
   	ym = ym * 1.1
    
    # initialize plot
    ylabel = expression(paste(text="Q (","m"^scriptscriptstyle(3)," s"^scriptscriptstyle(-1),")",sep=""))
    plot(NA, xlim=c(plotperiod[1],tail(plotperiod,1)), ylim=c(0,ym), ylab=ylabel, xlab= '',xaxs='i',xaxt='n',yaxs='i',main=paste('Annual Q ',basinnames[b]," ",startyear_ref,"-",endyear,sep=""))
    axis(1,at=seq(0,140,10),tck=-0.02,labels=seq(1960,2100,10),col="black")
    axis(1,at=seq(0,140,1),tck=-0.0075,labels=NA,col="black")
    
    # plot the polygons
    polyx = c(1:dim(poly_borders_all)[1],dim(poly_borders_all)[1]:1)
    for (i in 1:(dim(poly_borders_all)[2]-1)){
      polygon(polyx,c(poly_borders_all[,i,b],rev(poly_borders_all[,i+1,b])),col=polycols[i],border=polycols[i]);
    }
	axis(1,at=c(-1e99,1e99),labels=NA);axis(2,at=c(-1e99,1e99),labels=NA);axis(3,at=c(-1e99,1e99),labels=NA);axis(4,at=c(-1e99,1e99),labels=NA)
    
	mp<-matrix(c(41:140),nrow=100,ncol=1)
	#mtext(text = xlabels, side = 1, at = mp, line = 0.7, cex=0.75)
  
	
	#error bars
	max <- as.matrix(poly_borders_max[,5,b])
	min <- as.matrix(poly_borders_min[,5,b])
	mean <- as.matrix(poly_borders[,5,b])
	
	error.pos <- matrix(c(max-mean))
	error.neg <- matrix(c(mean-min))
	# Plot the vertical lines of the error bars
	# The vertical bars are plotted at the midpoints
	segments(mp, mean - error.neg, mp, mean + error.pos, lwd=1)
	
	# Now plot the horizontal bounds for the error bars
	# 1. The lower bar
	segments(mp - 0.1, mean - error.neg, mp + 0.1, mean - error.neg, lwd=1)
	# 2. The upper bar
	segments(mp - 0.1, mean + error.pos, mp + 0.1, mean + error.pos, lwd=1)
  
  #lines
	#lines(x=polyx[1:140], y=mean, type="l", col="red")
  #lines(x=polyx[1:12], y=poly_borders_ref[,5,b], type="l", col="blue")
  
    # add legend
    #legend(x='top',horiz=T,inset=0.01,legend=c('Base flow','Glacier melt','Snow melt','Rainfall'),fill=polycols,bty='n',cex=1)
    
  }
  # end basin loop
	
	#plot('')
	#legend(x='center',horiz=F,inset=0.01,legend=c('Base flow','Glacier melt','Snow melt','Rainfall'),fill=polycols,bty='n',cex=1.2)
	
	dev.off()
	
  } # end pdfout if


  
}

# read data


#loop over RCPs
RCP <- unique(data[,"RCP"])
for (rcp in RCP)
{
  filename <- paste(rcp,"_combined_hydrographs.pdf",sep="")
  Cairo(file=filename, 
        bg="white",
        type="pdf",
        units="in", 
        width=8, 
        height=4, 
        pointsize=12, 
        dpi=300)
  par(mfrow=c(2,4),oma=c(0,0,0,0),mar=c(2.5,3,1.5,1), tck=-0.025, mgp=c(3,0.5,0))
  for (i in c(rivers))
  {


#loop over river outlets and create plots
data.river <- subset(data,River==i)
data.river <- subset(data.river,RCP==rcp)

x.monthno<-data.river[,2]
x<-data.river[,c(11,13,15,17)]
if(rcp == "REF")
{x<-data.river[,c(10,12,14,16)]}
areacolors <- c("Indian red1","lightskyblue", "sandybrown","palegreen3")
xlabels <-data.river[,1]
ylabel <- expression(paste("Q (m"^"3","s"^"-1",")"))
xlims<-c(0.75,12.25)
ylims<-c(0,max(data.river[,c(6,8)])*1.075)

#plot

     

stackpoly(x,y=NULL,main=i,xlab="",ylab="", xaxlab=c(rep("", 12)), col=areacolors, stack=TRUE, xlim=xlims,ylim=ylims,axis4=FALSE,cex.axis=2)
REF.line <- data.river[,6]
FUT.line <- data.river[,7]

lines(x=x.monthno, y=REF.line, type="l", col="blue")
mp<-matrix(c(1:12),nrow=12,ncol=1)
mtext(text = xlabels, side = 1, at = mp, line = 0.7, cex=0.75)
mtext(text = ylabel, side = 2, line = 1.5, cex=0.75)

if(rcp != "REF")
{
  lines(x=x.monthno, y=FUT.line, type="l", col="red")

#error bars
max <- as.matrix(data.river[,8])
min <- as.matrix(data.river[,9])
mean <- as.matrix(data.river[,7])

error.pos <- matrix(c(max-mean))
error.neg <- matrix(c(mean-min))
# Plot the vertical lines of the error bars
# The vertical bars are plotted at the midpoints
segments(mp, mean - error.neg, mp, mean + error.pos, lwd=1)

# Now plot the horizontal bounds for the error bars
# 1. The lower bar
segments(mp - 0.1, mean - error.neg, mp + 0.1, mean - error.neg, lwd=1)
# 2. The upper bar
segments(mp - 0.1, mean + error.pos, mp + 0.1, mean + error.pos, lwd=1)

}
}
  dev.off()
}


