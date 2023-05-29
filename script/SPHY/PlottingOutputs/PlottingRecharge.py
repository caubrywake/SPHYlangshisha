# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 10:27:16 2023

@author: carol
"""

# plotmodelled gw recharge vs percolation?
# First, look into the location i already have time series for
# make a time series at 4 locations:
    
# gwrecharge (Gwre) vs subzone percolation vs glacier pecolation (Subp + GlacP)
# (C:\SPHY3\sphy_20230218\output_sphy_config_base14\GwreM001 ) vs (C:\SPHY3\sphy_20230218\output_sphy_config_base14\SubpM003) + (C:\SPHY3\sphy_20230218\output_sphy_config_base14\GlacpM000)

import os
os.chdir ('C:/SPHY3/script/SPHY/ModelEval')
# Plotting streamflow component
#import hydrostats as hs
import importSPHYtss as imp
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
from datetime import datetime
import hydroeval as he

figdir = ("C:/SPHY3/analysis/model_output/fig/recharge/v3/") # directory to save figure
plt.close('all')

path = 'C:/SPHY3/sphy_20230218/output_sphy_config_base16_2/'
dd = '01'
mm = '01'
yy = '2014'

min_val = -10
max_val =1500

#%%
# Import gw recharge
mod  = imp.importtss(yy, mm, dd, path+ "/GwreDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
gwre = mod.where((mod > min_val) & (mod < max_val), np.nan)

## Import subzone percolation
mod  = imp.importtss(yy, mm, dd, path+"/SubpDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
subp = mod.where((mod > min_val) & (mod < max_val), np.nan)

## Import modelled baseflow
mod  = imp.importtss(yy, mm, dd, path+"/BaserDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
baser = mod.where((mod > min_val) & (mod < max_val), np.nan)

## Import rootzone percolation
mod  = imp.importtss(yy, mm, dd, path+"/RootpDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
rootp = mod.where((mod > min_val) & (mod < max_val), np.nan)

## Import infiltration
mod  = imp.importtss(yy, mm, dd, path+"/InfilDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
infil = mod.where((mod > min_val) & (mod < max_val), np.nan)

# import ET and Preci[
mod  = imp.importtss(yy, mm, dd, path+ "/ETaFDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
etac = mod.where((mod > min_val) & (mod < max_val), np.nan)

mod  = imp.importtss(yy, mm, dd, path+ "/PrecFDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
precip = mod.where((mod > min_val) & (mod < max_val), np.nan)

mod  = imp.importtss(yy, mm, dd, path+ "/RainRDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
rainr = mod.where((mod > min_val) & (mod < max_val), np.nan)

mod  = imp.importtss(yy, mm, dd, path+ "/RootRDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
rootr= mod.where((mod > min_val) & (mod < max_val), np.nan)


# GlacP glacier id 2  (Langshihsa glacier)
## Import Glac percolation .csv
path = "C:/SPHY3/sphy_20230218/output_sphy_config_base16/"
fn = path+"GlacPerc.csv"

# Read in th data
GlacP= pd.read_csv(fn)
# Combine the date and time columns into a single datetime column
GlacP['datetime'] = pd.to_datetime(GlacP['Unnamed: 0'])

# Set the index of the DataFrame to the datetime column
GlacP.set_index('datetime', inplace=True)
glacp = GlacP.resample('D').mean()

#%% Plot timeseries

# Create a figure with two subplots, for AWS and gw1
savetitle = "RechargeSPHY_TS_2017_2018_1"
fig, axes = plt.subplots(figsize=(5,3))


startdate = '2017-05-15'
enddate = '2017-11-01'
start_date = dt.datetime.strptime(startdate, '%Y-%m-%d')
end_date = dt.datetime.strptime(enddate, '%Y-%m-%d')
# Plot for the first subplot: all

#axes[0].plot(infil.index, infil['AWS'], label='Infiltration', color = (0/255, 102/255, 0), linewidth=2)

axes.bar(precip.index, precip['AWS'],label='Precipitation', color=( 102/255,178/255, 255/255), linewidth=2) 
#axes[0].plot(rootp.index, rootp['AWS'], label='Rootzone Percolation',color = (124/255, 87/255,0) , linewidth=2) 
axes.plot(subp.index, subp['AWS'], label='Subzone Percolation', color='black', linewidth=2)
axes.plot(gwre.index, gwre['AWS'], label='GW recharge', color='red', linewidth=2)

axes.plot(glacp.index, glacp['2'], label='Glacier Percolation', color=(130/255, 130/255, 130/255), linewidth=2)
#axes[0].plot(rootr.index, rootr['AWS'], label='rootzone runoff', color='red', linewidth=2)
#axes[0].plot(rootr.index,rainr['AWS'], label='rainfall runoff', color='blue', linewidth=2)


axes.set_xlim(start_date, end_date)
axes.set_xlabel('Year')
axes.set_ylabel('SPHY Fluxes (mm/day)')
axes.set_title('Groundwater fluxes, AWS')
axes.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
axes.tick_params(rotation=30)
#axes[0].grid(which='major')
axes.set_ylim(ymin=0, ymax=35)
# Adjust layout and show the plot
plt.tight_layout()
plt.savefig(f"{figdir}{savetitle}.png", dpi = 300)
plt.savefig(f"{figdir}{savetitle}.pdf", dpi = 300)
plt.show()


# Plot for the second subplot: infil, percolation
# Plot for the third subplot: percolation, baseflow
savetitle = "RechargeSPHY_TS_2017_2018_2"
fig, axes = plt.subplots(figsize=(3,2))
startdate = '2017-05-01'
enddate = '2019-12-31'
start_date = dt.datetime.strptime(startdate, '%Y-%m-%d')
end_date = dt.datetime.strptime(enddate, '%Y-%m-%d')
#axes[1].plot(infil.index, infil['AWS'], label='Infiltration', color = (0/255, 102/255, 0), linewidth=2)
#axes[1].bar(precip.index, precip['AWS'],label='Precipitation', color=( 102/255,178/255, 255/255), linewidth=2) 
#axes[1].plot(rootp.index, rootp['AWS'], label='Rootzone Percolation',color = (124/255, 87/255,0) , linewidth=2) 
axes.plot(subp.index, subp['AWS'], label='Subzone Percolation', color='black', linewidth=2)
axes.plot(gwre.index, gwre['AWS'], label='GW recharge', color='red', linewidth=2)
#axes[1].plot(glacp.index, glacp['2'], label='Glacier Percolation', color=(160/255, 160/255, 160/255), linewidth=2)

axes.set_xlim(start_date, end_date)
axes.set_xlabel('Year')
axes.set_ylabel('SPHY Fluxes (mm/day)')
#axes[1].set_title('Groundwater fluxes, GW 1')
#axes[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
axes.tick_params(rotation=30)
#axes[1].grid(which='major')
axes.set_ylim(ymin=0, ymax=6)

# Adjust layout and show the plot
plt.tight_layout()
plt.savefig(f"{figdir}{savetitle}.png", dpi = 300)
plt.savefig(f"{figdir}{savetitle}.pdf", dpi = 300)
plt.show()

#%%
# Filter data between two dates
start_date = pd.to_datetime('2019-07-01')
end_date = pd.to_datetime('2020-07-01')
filtered_df = subp.loc[start_date:end_date]

# Calculate sum of 'AWS' column in filtered data
total_aws_sum = filtered_df['AWS'].sum()
filtered_df2 = gwre.loc[start_date:end_date]

# Calculate sum of 'AWS' column in filtered data
total_aws_sum = filtered_df['AWS'].sum()
total_aws_sum2 = filtered_df2['AWS'].sum()
print("Total AWS sum between", start_date, "and", end_date, ":", total_aws_sum)
print("Total AWS sum between", start_date, "and", end_date, ":", total_aws_sum2)
#%%

gwre['AWS'].sum()
glacp['2'].sum()



#%%% Now if I wanted to make it as a map of recharge

# Import the GW rechareb maps I like
#%% Import shapefiles

import os
import glob
import time
import rasterio
import rasterstats
import geopandas as gpd

path = "D:\\UU\\processed_files\\shapefile\\langshihsa_basin_outline\\LangshisaBasinandSide_outline_2mDEM.shp"
basinoutline = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\RGI_withingbasin.shp"
glacier = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\location_utm.shp"
location = gpd.read_file(path)
 
path = "D:/UU\processed_files/shapefile/langshihsa_surfacestream/surfacestream_20230420_2.shp"
rivshp = gpd.read_file(path)  
rivshp['id'] = range(1, len(rivshp)+1)  


##
# For sept 1 and March 1
id1 = '2017-06-01' #  1277
id2 = '2017-08-01' # 1339
id3 = '2017-11-01' #1430


# Define the paths to the rasters and shapefile
file_path1 = "C:/SPHY3/sphy_20230218/output_sphy_config_base16_2/SubpM001.277"
file_path11 = "D:\\UU\\glacperc\\v4\\GlacPM001.277"

file_path2 = "C:/SPHY3/sphy_20230218/output_sphy_config_base16_2/SubpM001.339"
file_path22 = "D:\\UU\\glacperc\\v4\\GlacPM001.369"

file_path3 = "C:/SPHY3/sphy_20230218/output_sphy_config_base16_2/SubpM001.430"
file_path33 = "D:\\UU\\glacperc\\v4\\GlacPM001.430"

save_fig = 'D:/UU/figure/recharge_fig/v4/'

with rasterio.open(file_path1) as src1:
        grid_extent = [src1.bounds[0], src1.bounds[2], src1.bounds[1], src1.bounds[3]]
        # Read the raster data as a numpy array
        subp1 = src1.read(1)

    # Open the raster file from raster_path2
with rasterio.open(file_path11) as src2:
        # Read the raster data as a numpy array
        glacp1  = src2.read(1)
        
with rasterio.open(file_path2) as src1:
        grid_extent = [src1.bounds[0], src1.bounds[2], src1.bounds[1], src1.bounds[3]]
        # Read the raster data as a numpy array
        subp2 = src1.read(1)

    # Open the raster file from raster_path2
with rasterio.open(file_path22) as src2:
        # Read the raster data as a numpy array
        glacp2  = src2.read(1)
        
with rasterio.open(file_path3) as src1:
        grid_extent = [src1.bounds[0], src1.bounds[2], src1.bounds[1], src1.bounds[3]]
        # Read the raster data as a numpy array
        subp3 = src1.read(1)

    # Open the raster file from raster_path2
with rasterio.open(file_path33) as src2:
        # Read the raster data as a numpy array
        glacp3  = src2.read(1)
        
        
    # Add the two rasters together
perc1 = subp1 + glacp1
perc2 = subp2 + glacp2
perc3 = subp3 + glacp3

# Convert ndarray to DataFrame
perc1_df = pd.DataFrame(perc1)
perc2_df = pd.DataFrame(perc2)
perc3_df = pd.DataFrame(perc3)

# Remove values above/below threshold
min_val = 0 
max_val = 1000
perc1_df = perc1_df.where((perc1_df > min_val), 0)
perc1_df = perc1_df.where((perc1_df < max_val), np.nan)

perc3_df = perc3_df.where((perc3_df > min_val), 0)
perc3_df = perc3_df.where((perc3_df < max_val), np.nan)

perc2_df = perc2_df.where((perc2_df > min_val), 0)
perc2_df = perc2_df.where((perc2_df < max_val), np.nan)

# Convert DataFrame back to ndarray
perc1 = perc1_df.values
perc2 = perc2_df.values
perc3 = perc3_df.values


fig, axs = plt.subplots(1,3, figsize=(10,2))
savetitle = 'Recharge_Maps'
# plot for perc1
im1 = axs[0].imshow(perc1, extent=grid_extent, cmap = 'Blues', vmin = 0, vmax = 3)
basinoutline.plot(ax=axs[0], facecolor='none', edgecolor='black')
glacier.plot(ax=axs[0], facecolor='none', edgecolor='black')
location.plot(ax=axs[0], markersize=2, facecolor='black', edgecolor='black')
rivshp.plot(ax=axs[0], linewidth=0.5, facecolor='none', edgecolor='black')
cbar1 = plt.colorbar(im1, ax=axs[0], shrink=0.9)
#cbar1.set_label('Recharge (m/d)')
axs[0].set_title(id1)
axs[0].set_xticklabels([])
axs[0].set_yticklabels([])
# plot for perc2
im2 = axs[1].imshow(perc2, extent=grid_extent, cmap = 'Blues', vmin = 0, vmax = 10)
basinoutline.plot(ax=axs[1], facecolor='none', edgecolor='black')
glacier.plot(ax=axs[1], facecolor='none', edgecolor='black')
location.plot(ax=axs[1], markersize=2, facecolor='black', edgecolor='black')
rivshp.plot(ax=axs[1], linewidth=0.5, facecolor='none', edgecolor='black')
cbar2 = plt.colorbar(im2, ax=axs[1], shrink=0.9)
#cbar2.set_label('Recharge (m/d)')
axs[1].set_title(id2)
axs[1].set_xticklabels([])
axs[1].set_yticklabels([])
# plot for perc3
im3 = axs[2].imshow(perc3, extent=grid_extent,  cmap = 'Blues', vmin = 0, vmax = 0.1)
basinoutline.plot(ax=axs[2], facecolor='none', edgecolor='black')
glacier.plot(ax=axs[2], facecolor='none', edgecolor='black')
location.plot(ax=axs[2], markersize=2, facecolor='black', edgecolor='black')
rivshp.plot(ax=axs[2], linewidth=0.5, facecolor='none', edgecolor='black')
cbar3 = plt.colorbar(im3, ax=axs[2], shrink=0.9)
cbar3.set_label('Recharge (mm/d)')
axs[2].set_title(id3)
axs[2].set_xticklabels([])
axs[2].set_yticklabels([])

plt.savefig(f"{figdir}{savetitle}.png", dpi = 300)
plt.savefig(f"{figdir}{savetitle}.pdf", dpi = 300)
plt.tight_layout()
plt.show()




