# -*- coding: utf-8 -*-
"""
Created on Mon May 29 11:55:58 2023

@author: carol
"""

## Calculate the water balance of the watershed
# the goal here is to focus on ET and Infil
#%% Model output

## ET from maps

# to make a time series of baseflow contribution to streams
import rasterio
import numpy as np
import glob
import geopandas as gpd
from rasterio.mask import mask
import matplotlib.pyplot as plt
import pandas as pd

figdir  ='C:/SPHY3/analysis/model_output/fig/ET/'

# Specify the folder path and the mask file name
folder_path = 'C:/SPHY3/sphy_20230218/output_20230529/'  # Replace with your actual folder path

mask_file = 'D:/UU/SPHY/scratch/basinoutline.shp'  # 
mask_data = gpd.read_file(mask_file)

# Umport otehr shapefile
path = "D:\\UU\\processed_files\\shapefile\\langshihsa_basin_outline\\LangshisaBasinandSide_outline_2mDEM.shp"
basinoutline = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\RGI_withingbasin.shp"
glacier = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\location_utm.shp"
location = gpd.read_file(path)
 
path = "D:/UU\processed_files/shapefile/langshihsa_surfacestream/surfacestream_20230420_2.shp"
rivshp = gpd.read_file(path)  
rivshp['id'] = range(1, len(rivshp)+1)  

# Get the geometry of the mask as a GeoJSON-like object
mask_geometry = mask_data.geometry.values[0]

# Define the list of file extensions to exclude
exclude_extensions = ['.tss', '.csv', '.aux', '.map']

# Get a list of all raster files in the folder
raster_files = glob.glob(folder_path + '/ET*')

# Filter out files with excluded extensions
raster_files = [f for f in raster_files if not any(ext in f for ext in exclude_extensions)]

# Create lists to store raster file names and their corresponding total values
raster_file_names = []
total_values = []

# create a time array for name on figure
from datetime import datetime, timedelta

start_date = datetime(2014, 1, 1)
end_date = datetime(2021, 1, 1)

dates = []
current_date = start_date

# Iterate through the dates, adding one month at a time
while current_date < end_date:
    dates.append(current_date)
    # Increment to the next month
    if current_date.month == 12:
        current_date = current_date.replace(year=current_date.year + 1, month=1)
    else:
        current_date = current_date.replace(month=current_date.month + 1)

total_values = []
# Loop through each raster file
for i, raster_file in enumerate(raster_files):
    # Open the raster file for reading
    with rasterio.open(raster_file) as src:
        # Clip the raster to the extent of the mask
        masked_data, masked_transform = mask(src, [mask_geometry], crop=True)
        #grid_extent = [src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
        grid_extent = rasterio.plot.plotting_extent(masked_data[0], masked_transform)

        # Set masked values to NaN
        masked_data = np.where(masked_data == src.nodata, np.nan, masked_data)
        masked_data = np.squeeze(masked_data)
        # Sum the values of the raster to obtain the total
        total = (np.nansum(masked_data))
        avg = (np.nanmean(masked_data))
        # Append the raster file name and total value to the lists
        raster_file_names.append(raster_file)
        total_values.append(avg) # montlhy sum to m3/s
        
        fig, axs = plt.subplots(figsize=(6,6))
        savetitle = 'ETmap'
        # plot for perc1
        im1 = axs.imshow(masked_data, extent=grid_extent, cmap = 'Greens', vmin = 0, vmax = 3)
        mask_data.plot(ax=axs,  facecolor='none', edgecolor='black')
        glacier.plot(ax=axs, facecolor='none', edgecolor='black')
        location.plot(ax=axs, markersize=2, facecolor='black', edgecolor='black')
        rivshp.plot(ax=axs, linewidth=0.5, facecolor='none', edgecolor='black')
        cbar1 = plt.colorbar(im1, ax=axs, shrink=0.5)
        axs.set_xticklabels([])
        axs.set_yticklabels([])

        file_name = raster_file[-11:]
        date = dates[i].strftime('%Y-%m-%d')  # Format the date as desired
        plt.title(f'{date} {file_name} (Total: {total})')
        plt.savefig(f"{figdir}{savetitle}{file_name}.png", dpi = 300)
        plt.savefig(f"{figdir}{savetitle}{file_name}.pdf", dpi = 300)
        plt.show()
        

#%% Plot the resulting ET across the basin
# Import ET at AWS
import importSPHYtss as imp
path = "C:/SPHY3/sphy_20230218/output_20230529/"
dd = '01'
mm = '01'
yy = '2014'

mod  = imp.importtss(yy, mm, dd, path+ "ETaFDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
#mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
#mod = mod.resample('M').mean()
# Keep only the outlet streamflow
et = mod[['AWS']]
et  = et.resample('M').mean()

# Plot the time series
savetitle = 'ET_timeseries'
plt.plot(dates, total_values, label='Basin')
plt.plot(et.index, et.AWS, label='AWS')
# Set the x-axis label
plt.xlabel('Date')
# Set the y-axis label
plt.ylabel('Monthly average ET (mm)')
plt.legend()
# Rotate the x-axis tick labels for better readability (optional)
plt.xticks(rotation=45)

plt.savefig(f"{figdir}{savetitle}.png", dpi = 300)
plt.savefig(f"{figdir}{savetitle}.pdf", dpi = 300)
# Display the plot
plt.show()