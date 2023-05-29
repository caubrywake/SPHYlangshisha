rm(list = ls())
library(Hmisc)
library(hydroGOF)
##Script to compare SPHY simulated glacier mass balance to IceSat derived glacier mass balance.
##arthurlutz 20160726

###INSTRUCTIONS
#Run SPHY for 1 October 2003 until 30 September 2008, because the IceSat data is representative for autumn 2003 - autumn 2008.
###INSTRUCTIONS END

###SETTINGS
indir <- "e:\\Active\\2014_003_HIAWARE\\model\\output\\"
outdir <- "e:\\Active\\2014_003_HIAWARE\\analysis\\sphy_glacier_mb\\"
workdir <- "c:\\workdir\\"
basin_names <- c("Hunza_Indus","Marshyangdi_bimalnagar_Ganga","Sunkosh_wangdirapids_Brahmaputra")
#Icesat observed glacier MB and SD for upstream catchments, derived by Desiree Treichler from Kääb data. See e-mail 20160627
icesat_obs <- c(-0.088,-0.21,-0.23)
icesat_sigma <- c(0.36,0.61,0.30)
csvname <- "sphy_vs_icesat" 
#paths to 3 tables based on glac_table, which contain the glaciers in each upstream catchment
dir_tables <- "e:\\Active\\2014_003_HIAWARE\\data\\glaciers\\glaciers_SPHY\\subbasins\\csv\\"
glac_tables <- c("sphy_glaciers_hunza.csv","sphy_glaciers_Marshyangdi.csv","sphy_glaciers_Sunkosh.csv")

###SETTINGS END

#get parsed argument for runid
args <- commandArgs(trailingOnly = TRUE)
id <- args[1]
if(is.na(args[1]))
{
  id <-"no_id"
}

# read sphy simulated glacier mass balance components
prec <- read.csv(paste(indir,"Prec_GLAC.csv",sep=""),header=T)
glacmelt <- read.csv(paste(indir,"GlacMelt.csv",sep=""),header=T)
snowr <- read.csv(paste(indir,"SnowR_GLAC.csv",sep=""),header=T)
perc <- read.csv(paste(indir,"GlacPerc.csv",sep=""),header=T)
glacr <- read.csv(paste(indir,"GlacR.csv",sep=""),header=T)


#loop over basins
for(i in 1:length(basin_names))
{
  # read table with glaciers
  glaciers <- read.csv(paste(dir_tables,glac_tables[i],sep=""),header=T)
  glaciers2 <- cbind(glaciers[,3],glaciers[,7])
  
  #aggregate glacids and sum fractions
  glaciers3 <- aggregate(glaciers2[,2],by=list(glaciers2[,1]),FUN=sum)
  
  
  #create df
  df <- as.data.frame(matrix(NA,ncol=7,nrow=nrow(glaciers3)))
  df[,1]<- glaciers3[,1]
  df[,2]<- glaciers3[,2]
  #loop over U-IDs
  
  row <-1
  for(x in df[,1])
  {
    #get total prec
    colnames <- colnames(prec)
    colname <- paste("X",x,sep="")
    glacid <- match(colname,colnames)
    Psum <- sum(prec[,glacid])
    df[row,3] <- Psum
    
    #get total glacmelt
    colnames <- colnames(glacmelt)
    colname <- paste("X",x,sep="")
    glacid <- match(colname,colnames)
    Msum <- sum(glacmelt[,glacid])
    df[row,4] <- Msum
    
    #get total snow runoff
    colnames <- colnames(snowr)
    colname <- paste("X",x,sep="")
    glacid <- match(colname,colnames)
    SRsum <- sum(snowr[,glacid])
    df[row,5] <- SRsum
    
    #get total percolation
    colnames <- colnames(perc)
    colname <- paste("X",x,sep="")
    glacid <- match(colname,colnames)
    Percsum <- sum(perc[,glacid])
    df[row,6] <- Percsum
    
    #get total glacier runoff
    colnames <- colnames(glacr)
    colname <- paste("X",x,sep="")
    glacid <- match(colname,colnames)
    GRsum <- sum(glacr[,glacid])
    df[row,7] <- GRsum
    
    row <- row +1
  }
  colnames(df) <- c('GLAC_ID','FRAC','PREC','GLACM','SNOWR','PERC',"GLACR")
  
  #df[,8] <- (((df[,3]+df[,4])-(df[,5]+df[,6]+df[,7]))/5)/1000
  df[,8] <- ((df[,3]-df[,7]-df[,5]-df[,6])/5)/1000
  df[,9] <- (df[,2]/sum(df[,2]))*df[,8]
  avg_mb_sim <- sum(df[,9])
  sd_mb_sim <- sd(df[,8])
  
  df2 <- matrix(NA,nrow=2,ncol=3)
  df2[1,1] <- "OBS"
  df2[2,1] <- "SIM"
  df2[1,2] <- icesat_obs[i]
  df2[2,2] <- avg_mb_sim
  df2[1,3] <- icesat_sigma[i]
  df2[2,3] <- sd_mb_sim
  colnames(df2) <- c("OBS_SIM","MB_mean","MB_sd")
  
  write.csv(df2,file=paste(outdir,csvname,"_",basin_names[i],"_",id,".csv",sep=""))
  
}


