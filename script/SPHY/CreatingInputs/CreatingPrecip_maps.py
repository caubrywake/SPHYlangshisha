# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 10:47:02 2023

@author: carol
"""

#%% For precipitation
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import rasterio
from rasterio import Affine as A
from rasterio.warp import reproject, Resampling
import numpy as np
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
import geopandas as gpd

os.chdir("D:/UU/processed_files/temp_maps/20230419_3prec/") #

os.environ["PROJ_LIB"] = "C:\\Users\\carol\\miniconda3\\envs\\spyder-env\\Lib\\site-packages\\pyproj\\proj_dir\\share\\proj\\"

# Import precipitation time series
fn = 'C:/SPHY3/analysis/data_processed/PdailyCorr_Ls_infilledw_20120503_20210701_withspinup.csv'
figdir = ("C:/SPHY3/analysis/model_output/fig/dataplot/") # directory to save figure

# Read in the data
meas = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['date'] )
meas = meas.iloc[544:] # so its starts on the same date as temp: 29-oct-2013
# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)

# Filter the DataFrame for the date range
start_date = '2015-01-01'
end_date = '2015-12-31'

# Filter the DataFrame for the date range
start_date = '2015-01-01'
end_date = '2015-12-31'
df_filtered = meas.loc[start_date:end_date]

# Multiply the values in the 'meas' column by 1.2
df_filtered['Pcorr'] = df_filtered['Pcorr'] * 1.2

# Update the original DataFrame with the filtered and updated values
meas.update(df_filtered)


# Cut # Start on Jan 1, 2014 ##################################
start_date = '2014-01-01'
end_date = '2020-12-31'


meas = meas.loc[start_date:end_date]
meas = meas['Pcorr']
meas = meas*1.5
# Label and variable names

annual_val = meas.resample('A').sum()
annual_val
label1 = 'Daily Precipitation [mm]'
figtitle = 'Precipitation Pluvio @ LS, infilled, *1.5'
savetitle = 'Pluvio_LS'

# Full period
plt.plot(meas.index, meas, color  ='black')

# Graph settings
plt.xlabel('Year')
plt.ylabel(label1)
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

plt.show()

#%% Import shapefiles
path = "D:\\UU\\processed_files\\shapefile\\langshihsa_basin_outline\\LangshisaBasinandSide_outline_2mDEM.shp"
basinoutline = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\RGI_withingbasin.shp"
glacier = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\location_utm.shp"
location = gpd.read_file(path)
#%%  Plot 


# Location of langshisha AWS
#latitude = 28.20265
# longitude = 85.68619
#lat = -172279 # in equal ambers 
#lon = -857040
lat = 371059 # in tum 45
lon = 3120355

 #%% Import the clipped wrf   
with rasterio.open('D:\\UU\\SPHY\\scratch\\wrfclipped5.tif') as src:
     # Read the metadata and data of the input raster
     metadata = src.meta
     data = src.read(1)
     bands = src.read()
    # Get the pixel coordinates of the reprojected point
     rowval, colval = src.index(lat, lon)
     transform = src.transform
     data_extent = [src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
     rowval, colval = src.index(lat, lon)
     
# Create a dictionary where the keys are month numbers (1-12) and the values are band numbers (0-based index)
month_to_band = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11}

df = meas
df = df.to_frame()  
    # Define an empty list to hold reference values (sanity check)
value_norm_list = [] # result should change every month
precip_wrf_value_list = [] # average value of the tmeprature acorss the dem
value_wrf_list = [] # this should be the same as the inital time series input

counter = 1

# Iterate over each row in the DataFrame

for date, row in df.iterrows():
    # to test
  #   first_row = df.iloc[[80]]  # select the first row of the DataFrame
  #  date = first_row.index[0]  # extract the date from the DataFrame index
  #  row = first_row.iloc[0]  # extract the row values as a Series

    month = date.month  # Extract the month number from the date
    band = month_to_band[month]  # Get the corresponding band number from the dictionary
    raster = bands[band]  # Extract the corresponding band from the raster
    value = raster[rowval, colval]
    # normalize the raster to the value
    norm_raster = raster*(1/value)
    val = row['Pcorr']
    precip_wrf = norm_raster * val
    
    # sanity checks
    value_norm =  norm_raster[rowval, colval] # this should be 1
    precip_wrf_value = precip_wrf[rowval, colval] # this should be the same as the precip value  row[Var1]
    value_wrf = raster [rowval, colval] 
    # sanity checks
    value_norm_list.append(value_norm) 
    precip_wrf_value_list.append(precip_wrf_value)
    value_wrf_list.append(value_wrf)
     
        # Write the result to a new raster file
    filename = f"prec{counter:07}.tif"
    filename = filename.replace('.tif', '')
    filename = filename[:8] + '.' + filename[8:]
    counter += 1
    
    metadata['count'] = 1 # Set the number of bands to 1
    with rasterio.open(filename, 'w', **metadata) as dst:
            dst.write(precip_wrf, 1)
            
            
             
concat = pd.DataFrame({'datetime':meas.index, 'ls_precip':precip_wrf_value_list, 'wrfvalue':value_wrf_list, 'wrf_norm':value_norm_list})
concat.set_index('datetime', inplace=True)
df_concat = pd.concat([meas, concat], axis =1)
df_concat.to_csv('D:\\UU\\field_data\\processed\\Pdaily_processed_sanitycheck.csv')

## ectra code to make a figue to test if it worked
# Create a figure with three subplots
"""    
    df = meas

    first_row = df.iloc[[80]]  # select the first row of the DataFrame
    date = first_row.index[0]  # extract the date from the DataFrame index
    row = first_row.iloc[0]  # extract the row values as a Series

    month = date.month  # Extract the month number from the date
    band = month_to_band[month]  # Get the corresponding band number from the dictionary
    raster = bands[band]  # Extract the corresponding band from the raster
    value = raster[rowval, colval]
    # normalize the raster to the value
    norm_raster = raster*(1/value)
    val = row
    precip_wrf = norm_raster * val
    
    # sanity checks
    value_norm =  norm_raster[rowval, colval] # this should be 1
    precip_wrf_value = precip_wrf[rowval, colval] # this should be the same as the precip value  row[Var1]
    value_wrf = raster [rowval, colval] 
    # sanity checks
    value_norm_list.append(value_norm) 
    precip_wrf_value_list.append(precip_wrf_value)
    value_wrf_list.append(value_wrf)
     
        # Write the result to a new raster file
    filename = f"prec{counter:07}.tif"
    filename = filename.replace('.tif', '')
    filename = filename[:8] + '.' + filename[8:]
    counter += 1
    
    metadata['count'] = 1 # Set the number of bands to 1
    with rasterio.open(filename, 'w', **metadata) as dst:
            dst.write(precip_wrf, 1)

norms = [Normalize(vmin=raster.min(), vmax=raster.max()), Normalize(vmin=norm_raster.min(), vmax=norm_raster.max()), Normalize(vmin=precip_wrf.min(), vmax=precip_wrf.max())]
cmaps = [get_cmap('coolwarm'), get_cmap('coolwarm'), get_cmap('coolwarm')]

# Create a figure with three subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

# Plot the first raster in the first subplot
im1 = axes[0, 0].imshow(raster, extent=data_extent, cmap=cmaps[0], norm=norms[0])
basinoutline.plot(ax=axes[0, 0], facecolor='none', edgecolor='black')
glacier.plot(ax=axes[0,0], facecolor='none', edgecolor='black')
location.plot(ax=axes[0,0], markersize=1, facecolor='black', edgecolor='black')
axes[0, 0].set_title('WRF pattern')

# Plot the second raster in the second subplot
im2 = axes[0, 1].imshow(norm_raster, cmap=cmaps[1], extent=data_extent, norm=norms[1])
basinoutline.plot(ax=axes[0, 1], facecolor='none', edgecolor='black')
glacier.plot(ax=axes[0,1], facecolor='none', edgecolor='black')
location.plot(ax=axes[0,1], markersize=1, facecolor='black', edgecolor='black')
axes[0, 1].set_title('WRF pattern normalized to precip')

# Plot the third raster in the third subplot
im3 = axes[1, 0].imshow(precip_wrf, cmap=cmaps[2], extent=data_extent, norm=norms[2])
basinoutline.plot(ax=axes[1, 0], facecolor='none', edgecolor='black')
glacier.plot(ax=axes[1,0], facecolor='none', edgecolor='black')
location.plot(ax=axes[1,0], markersize=1, facecolor='black', edgecolor='black')
axes[1, 0].set_title('Normalized WRF * precip')

# Remove the fourth subplot in the bottom-right corner
fig.delaxes(axes[1, 1])

# Add colorbars to the subplots
cbar1 = fig.colorbar(im1, ax=axes[0, 0], fraction=0.03, pad=0.04)
cbar1.ax.set_ylabel('Precip gradient', rotation=270, labelpad=15)
cbar2 = fig.colorbar(im2, ax=axes[0, 1], fraction=0.03, pad=0.04)
cbar2.ax.set_ylabel('Norm precip gradient', rotation=270, labelpad=15)
cbar3 = fig.colorbar(im3, ax=axes[1, 0], fraction=0.03, pad=0.04)
cbar3.ax.set_ylabel('Precip', rotation=270, labelpad=15)

axes[0,0].set_xticklabels([])
axes[0,0].set_yticklabels([])
axes[0,1].set_xticklabels([])
axes[0,1].set_yticklabels([])
axes[1,0].set_xticklabels([])
axes[1,0].set_yticklabels([])

plt.savefig(figdir + 'PrecipMaos_fromWRF' + '.png', dpi = 300, bbox_inches='tight')
plt.show()
"""
   
       