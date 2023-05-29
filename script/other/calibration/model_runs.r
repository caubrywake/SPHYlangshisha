rm(list = ls())

library(hydroGOF)
##Script to run SPHY model X times with random sampling of glacier parameters from defined parameter ranges,
##including comparison of model output to IceSat data
##arthurlutz 20160726

###SETTINGS
modeldir <- "e:\\Active\\2014_003_HIAWARE\\model\\"
compare_script <- "e:\\Active\\2014_003_HIAWARE\\scripts\\calib_glaciers\\compare_mb.r"
workdir <- "c:\\workdir\\"
params <- c("DDFG","DDFDG")
template <- "e:\\Active\\2014_003_HIAWARE\\scripts\\calib_glaciers\\sphy_config_glaciers.tpl"
statsdir <- "e:\\Active\\2014_003_HIAWARE\\analysis\\sphy_glacier_mb\\"
ranges_start <- c(4,1)
ranges_end <- c(8,5)
no_of_runs <- 1
basin_names <- c("Hunza_Indus","Marshyangdi_bimalnagar_Ganga","Sunkosh_wangdirapids_Brahmaputra")
csvout <- paste(statsdir,"modelrun_results.csv",sep="")
###SETTINGS END

###INSTRUCTION
#copy sphy_config.cfg to same directory with name sphy_config_snow.tpl
#replace parameters in .tpl file that should be varied with &name_of_parameter&
###INSTRUCTION END


#generate table with randomly sampled parameter combinations
df <- as.data.frame(matrix(NA,nrow=no_of_runs,ncol=length(params)+12))
for(i in 1:no_of_runs)
{
  for(a in 1:length(params))
  {
    df[i,a] <- runif(1,min=min(ranges_start[a]),max=max(ranges_end[a]))
  }
}
  
#loop over parameter combinations
for(i in 1:nrow(df))
{
  #modify sphy config file
  template_lines <- readLines(template)
  for(a in 1:length(params))
  {
    template_lines <- gsub(pattern=paste("&",params[a],"&",sep=""),replace=df[i,a],x=template_lines)
  }
  writeLines(template_lines,paste(modeldir,"sphy_config.cfg",sep=""))
  
  ##run model
  setwd(modeldir)
  print(paste("Starting sphy model run ",i,sep=""))
  command <- paste("python ",modeldir,"sphy.py",sep="")
  system(command, wait=T)
  
  ##compare model output to MODIS observed
  print(paste("Starting comparison with IceSat for sphy model run ",i,sep=""))
  command <- paste("RScript ",compare_script," ",i,sep="")
  system(command, wait=T)
  print(paste("Comparison with IceSat for sphy model run ",i," finished.",sep=""))
  
  ##read observed and simulated MB and add to dataframe
  for (x in 1:length(basin_names))
  {
    sim <- read.csv(paste(statsdir,"sphy_vs_icesat_",basin_names[x],"_",i,".csv",sep=""))
    df[i,length(params)+x*4-3]<-sim[1,3]
    df[i,length(params)+x*4-2]<-sim[1,4]
    df[i,length(params)+x*4-1]<-sim[2,3]
    df[i,length(params)+x*4]<-sim[2,4]
   }
  colnames(df) <- c(params,paste("MBobs_mean_",basin_names[1],sep=""),paste("MBobs_sd_",basin_names[1],sep=""),paste("MBsim_mean_",basin_names[1],sep=""),paste("MBsim_sd_",basin_names[1],sep=""),paste("MBobs_mean_",basin_names[2],sep=""),paste("MBobs_sd_",basin_names[2],sep=""),paste("MBsim_mean_",basin_names[2],sep=""),paste("MBsim_sd_",basin_names[2],sep=""),paste("MBobs_mean_",basin_names[3],sep=""),paste("MBobs_sd_",basin_names[3],sep=""),paste("MBsim_mean_",basin_names[3],sep=""),paste("MBsim_sd_",basin_names[3],sep=""))
  write.csv(df,file=csvout)
  
}
