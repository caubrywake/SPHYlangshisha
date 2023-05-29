rm(list = ls())

#vars <- c('TotR','TBaR','TGlR','TRaR','TSnR')
vars <- c('TQRA','TRRA','TSRA','TGRA','TBRA')

#routed T or F
routed <- T

for (var in vars)
{
###SETTINGS
# paths
clone <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\input\\clonescalar.map"
input <- "e:\\Active\\2013_014_Indus\\Model\\SPHY_PYTHON\\output\\final3\\"
output <- paste("e:\\Active\\2013_014_Indus\\Analysis\\discharge3\\ref\\",var,"ref.map",sep="")

# start and end timesteps
tsstart <- 4015
noofyears <- 30

###

# create first map
command <- paste("pcrcalc ",output," = ",clone," -1", sep="")
system(command)


# sum maps

ts <- tsstart
for (i in 1:noofyears)
{
	daynum <- as.integer(tsstart)
	daystring <- formatC(daynum, width=6, flag=0)
	daystring1 <- substr(daystring,1,3)
	daystring2 <- substr(daystring,4,6)
	daypcr <- paste(daystring1,".",daystring2, sep="")
	inputtair <- paste (input,var,"Y",daypcr, sep="")
	outputtair <- output
	pcrcalctaircommand <- paste("pcrcalc ",outputtair," = ",outputtair," + ",inputtair, sep="")
	
	system(pcrcalctaircommand)
	print(i)
	print(ts)
	ts <- ts + 365
}


# average maps
if(routed == F)
	{
	command <- paste("pcrcalc ",outputtair," = ",outputtair," / ",noofyears, sep="")
	}
	if(routed == T)
	{
	command <- paste("pcrcalc ",outputtair," = ",outputtair," / (",noofyears,"*365)", sep="")
	}

system(command)

}
print("Finished script execution")