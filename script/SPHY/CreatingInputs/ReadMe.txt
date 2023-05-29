In these files, I create the pcraster foricginf for sphy simulations using the langshihsa pluvio station records.

I create the mean daily, minimum daily and maximum daily temperature and the daily precipitation in different scripts. 

Creating_TempMax_maps.py, Creating_TempMean_maps.py, Creating_TempMin_maps.py:

The three temperature scripts follow a very similar strcture: 

I import the weather station timeseries (20211206_Pluvio_Langshisha.csv) and average to daily values (mean, min or max) as needed, and infil the missing values using ERA-5 values based on a linear regression. For each processing step, I export figures.
This results in a fille time series form Oct-29-2013 to Dec-31-2020 (to be extnded when new data is appended)

Using previously calculated monthly temperature gradient between the weather station diftsitrbuted throughout the basin, I create distributed temperature forcings using the weather station elevation and the dEM to calculate the change in elevation.

I then export each temperature forcing with the right extension as a .tiff. 

CreatingPrecip_maps: 

For precipitation, I use the WRF derived-orecipitation gradient by Collier et al. 2015.
Using the tipping bucket precipitation from the Langshihsa pluvio, I mutlply each precipitation by the montlhy precipitation gradient to obtain a daily ratser of precipitaton. 

TranslateForcingstoPCRaster.py:
I then convert every forcing to a pcraster format.

ClippingForcing.py: This script clips existing forcing to a smaller area and saves them under the same name. Originally create to simulated a smaller area of the Langtag baisn while using the same input as previous simulations.


