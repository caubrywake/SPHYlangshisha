##Script to make yearly netcdf files from daily PCraster grids
##arthurlutz 20151114
rm(list=ls(all=TRUE))
library(RNetCDF)
library(raster)

###SETTINGS

indir <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\input\\"
outdir <- "e:\\Forcing\\Indus\\APHRODITE_corrected\\netcdf\\"
vars <- c('prec')
dummy <- raster("e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\input\\prec\\prec0000.001")
startyear <- 1971
endyear <- 2000


###SETTINGS END

##list dates/timesteps to process
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
dates<-datesframe[which(datesframe[,2] >= startyear & datesframe[,2] <= endyear),]

##extract dimensions/extent/resolution/cellcenters
griddims <- dim(dummy)
extent <- extent(dummy)
resolution <- (extent[2]-extent[1])/griddims[2]

grid_metadata <- as.data.frame(matrix(ncol=2,nrow=griddims[1]*griddims[2]))
m<-1
for (i in 1:griddims[2]){
  for (y in 1: griddims[1])
  {
    grid_metadata[m,1]<-extent[1]+i*resolution-0.5*resolution
    grid_metadata[m,2]<-extent[3]+y*resolution-0.5*resolution
    m <- m+1
  }
}
colnames(grid_metadata)<-c("xcenter","ycenter")

##initiate array to store daily data
Pdata <- array(NA,dim=c(griddims[2],griddims[1],365))


##loop over variables
for (var in vars)
{
  
##loop over years
for(year in startyear:endyear)
{
  yeardays <- datesframe[which(datesframe[,2] == year),] 
  #loop over days and fill array with data from daily grids
  for (i in 1:365)
  {
    timestep <- sprintf("%07d", yeardays[i,1])
    pcrno <- paste(substr(timestep,1,4),".",substr(timestep,5,7),sep="")
    print(paste(yeardays[i,2],"-",yeardays[i,3],"-",yeardays[i,4],sep=""))
    grid <- flip(raster(paste(indir,var,"\\",var,pcrno,sep="")),direction='y')
    tempPdata <- t(as.matrix(grid))
    Pdata[,,i]<-tempPdata
  }


################################################## Create NetCDF Output ##################################################
  
  # create new netcdf file ("clobber=TRUE" overwrites existing files!)
  new <- create.nc(paste(outdir,var,"_",year,".nc",sep=""),clobber=TRUE);
   
  # define the dimensions
  dim.def.nc(new,dimname="latitude", dimlength=griddims[2],unlim=FALSE);
  dim.def.nc(new,dimname="longitude",dimlength=griddims[1],unlim=FALSE);
  #dim.def.nc(new,dimname="y0", dimlength=griddims[1],unlim=FALSE);
  #dim.def.nc(new,dimname="x0", dimlength=griddims[2],unlim=FALSE);
  dim.def.nc(new,dimname="time",dimlength=365,unlim=FALSE);
  

  ## define the variables and attributes
#longitude
  var.def.nc(new,varname="longitude",vartype="NC_FLOAT",dimensions=c("longitude"));
att.put.nc(new,variable="longitude",name="long_name",type="NC_CHAR",value="Longitude");
att.put.nc(new,variable="longitude",name="_CoordinateAxisType",type="NC_CHAR",value="Lon");
att.put.nc(new,variable="longitude",name="units",type="NC_CHAR",value="degrees_east");

#latitude
  var.def.nc(new,varname="latitude",vartype="NC_FLOAT", dimensions=c("latitude"));
att.put.nc(new,variable="latitude",name="long_name",type="NC_CHAR",value="Latitude");
att.put.nc(new,variable="latitude",name="_CoordinateAxisType",type="NC_CHAR",value="Lat");
att.put.nc(new,variable="latitude",name="units",type="NC_CHAR",value="degrees_north");

#time
var.def.nc(new,varname="time",vartype="NC_FLOAT",dimensions=c("time"));
att.put.nc(new,variable="time",name="long_name",type="NC_CHAR",value="time");
att.put.nc(new,variable="time",name="units",type="NC_CHAR",value=paste("days since ",year-1,"-12-31 12:0:0",sep=""))
att.put.nc(new,variable="time",name="calendar",type="NC_CHAR",value="noleap")

#variable
if(var == "prec")
{
  var.def.nc(new,varname="P",vartype="NC_FLOAT",dimensions=c("latitude","longitude","time"));
  att.put.nc(new,variable="P",name="standard_name",type="NC_CHAR",value="precipitation");
  att.put.nc(new,variable="P",name="long_name",type="NC_CHAR",value="Daily precipitation sum (mm)");
  att.put.nc(new,variable="P",name="units",type="NC_CHAR",value="mm");
  att.put.nc(new,variable="P",name="_FillValue",type="NC_FLOAT",value=-9999);  
}
if(var == "tavg")
{
  var.def.nc(new,varname="Tavg",vartype="NC_FLOAT",dimensions=c("latitude","longitude","time"));
  att.put.nc(new,variable="Tavg",name="standard_name",type="NC_CHAR",value="air_temperature");
  att.put.nc(new,variable="Tavg",name="long_name",type="NC_CHAR",value="Daily mean air temperature (degree Celsius)");
  att.put.nc(new,variable="Tavg",name="units",type="NC_CHAR",value="degree_Celsius");
  att.put.nc(new,variable="Tavg",name="_FillValue",type="NC_FLOAT",value=-9999);  
}
if(var == "tmax")
{
  var.def.nc(new,varname="Tmax",vartype="NC_FLOAT",dimensions=c("latitude","longitude","time"));
  att.put.nc(new,variable="Tmax",name="standard_name",type="NC_CHAR",value="maximum_air_temperature");
  att.put.nc(new,variable="Tmax",name="long_name",type="NC_CHAR",value="Daily maximum air temperature (degree Celsius)");
  att.put.nc(new,variable="Tmax",name="units",type="NC_CHAR",value="degree_Celsius");
  att.put.nc(new,variable="Tmax",name="_FillValue",type="NC_FLOAT",value=-9999);  
}
if(var == "tmin")
{
  var.def.nc(new,varname="Tmin",vartype="NC_FLOAT",dimensions=c("latitude","longitude","time"));
  att.put.nc(new,variable="Tmin",name="standard_name",type="NC_CHAR",value="minimum_air_temperature");
  att.put.nc(new,variable="Tmin",name="long_name",type="NC_CHAR",value="Daily minimum air temperature (degree Celsius)");
  att.put.nc(new,variable="Tmin",name="units",type="NC_CHAR",value="degree_Celsius");
  att.put.nc(new,variable="Tmin",name="_FillValue",type="NC_FLOAT",value=-9999);  
}


#projection
  var.def.nc(new,varname="UTM_Projection",vartype="NC_CHAR",dimensions=NA);
att.put.nc(new,variable="UTM_Projection",name="grid_mapping_name", type="NC_CHAR", value="universal_transverse_mercator")
att.put.nc(new,variable="UTM_Projection",name="utm_zone_number", type="NC_FLOAT", value="45")
att.put.nc(new,variable="UTM_Projection",name="semi_major_axis", type="NC_FLOAT", value="6378137")
att.put.nc(new,variable="UTM_Projection",name="inverse_flattening", type="NC_FLOAT", value="298.257")
att.put.nc(new,variable="UTM_Projection",name="_CoordinateTransformType", type="NC_CHAR", value="Projection")
att.put.nc(new,variable="UTM_Projection",name="_CoordinateAxisTypes", type="NC_CHAR", value="GeoX GeoY")
  
#var.def.nc(new,varname="x0",vartype="NC_DOUBLE",dimensions=c("x0"));
#var.def.nc(new,varname="y0",vartype="NC_DOUBLE", dimensions=c("y0"));
#var.def.nc(new,varname="P",vartype="NC_DOUBLE",dimensions=c("y0","x0","day"));  

# define the "desciption" attributes of the variables
  #att.put.nc(new,variable="x0",name="standard_name",type="NC_CHAR",value="projection_x_coordinate");
  #att.put.nc(new,variable="y0",name="standard_name",type="NC_CHAR",value="projection_y_coordinate");

  #att.put.nc(new,variable="x0",name="long_name",type="NC_CHAR",value="x distance on the projection plane from the origin");
  #att.put.nc(new,variable="y0",name="long_name",type="NC_CHAR",value="y distance on the projection plane from the origin");

#att.put.nc(new,variable="P",name="grid_mapping",type="NC_CHAR",value="UTM_Projection");
  #att.put.nc(new,variable="x0",name="units",type="NC_CHAR",value="m");
  #att.put.nc(new,variable="y0",name="units",type="NC_CHAR",value="m");
  

  #att.put.nc(new,variable="x0",name="_FillValue",type="NC_DOUBLE",value=-9999);
  #att.put.nc(new,variable="y0",name="_FillValue",type="NC_DOUBLE",value=-9999);

    
  # close and reopen the netcdf file to enable write access
  close.nc(new)
  new <- open.nc(paste(outdir,var,"_",year,".nc",sep=""), write=TRUE);
  
  # put the parameter data into the netcdf variables 
  var.put.nc(new,variable="longitude",data=sort(unique(grid_metadata$ycenter)));
  var.put.nc(new,variable="latitude",data=rev(sort(unique(grid_metadata$xcenter))));
  var.put.nc(new,variable="time",data=c(1:365));
  
  if(var == "prec")
  {
  var.put.nc(new,variable="P",data=Pdata);  
  }
if(var == "tavg")
{
  var.put.nc(new,variable="Tavg",data=Pdata);  
}
if(var == "tmax")
{
  var.put.nc(new,variable="Tmax",data=Pdata);  
}
if(var == "tmin")
{
  var.put.nc(new,variable="Tmin",data=Pdata);  
}




  # Add global attributes to the NetCDF file
  att.put.nc(new, "NC_GLOBAL", "title", "NC_CHAR", "Upper Indus basin corrected precipitation dataset")
  att.put.nc(new, "NC_GLOBAL", "institution", "NC_CHAR", "FutureWater - www.futurewater.nl")
  att.put.nc(new, "NC_GLOBAL", "references", "NC_CHAR", "-")
  att.put.nc(new, "NC_GLOBAL", "comment", "NC_CHAR", "This NetCDF file has been generated using the RNetCDF library in R");
  att.put.nc(new, "NC_GLOBAL", "creator", "NC_CHAR", "A.F. Lutz (FutureWater)");
  att.put.nc(new, "NC_GLOBAL", "disclaimer", "NC_CHAR", "FutureWater")
  att.put.nc(new, "NC_GLOBAL", "history", "NC_CHAR", paste("Original NetCDF file created on ",Sys.Date(),sep=""));
           
 
  # final operations
  sync.nc(new);                     # Sync edited data to disk
  close.nc(new);                    # Close the netcdf file
}
}