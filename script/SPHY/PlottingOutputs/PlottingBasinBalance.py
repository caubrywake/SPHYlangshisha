# -*- coding: utf-8 -*-
"""
Created on Mon May 29 14:42:14 2023

@author: carol
"""

## Baisn wide annual mass balance

# component:
    # Rainfall, snowfall, ET, rainfal runoff, snowmelt runoff, glacier runoff, baseflow. 
    
    # improt each component and get basin sum for each
    

import rasterio
import numpy as np
import glob
import geopandas as gpd
from rasterio.mask import mask
import matplotlib.pyplot as plt
import pandas as pd

figdir  ='C:/SPHY3/analysis/model_output/fig/basinbalance/'

# Specify the folder path and the mask file name
folder_path = 'C:/SPHY3/sphy_20230218/output_20230529/'  # Replace with your actual folder path

# Improt the shapefile for the plot and mask
mask_file = 'D:/UU/SPHY/scratch/basinoutline.shp'  # 
mask_data = gpd.read_file(mask_file)

# Import otehr shapefile
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

#%% create a time array for name on figure
from datetime import datetime

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

#%% ET
# Get a list of all raster files in the folder
raster_files = glob.glob(folder_path + '/ET*')

# Filter out files with excluded extensions
raster_files = [f for f in raster_files if not any(ext in f for ext in exclude_extensions)]

# Create lists to store raster file names and their corresponding total values
raster_file_names = []
ET = []

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
        total = round(np.nansum(-masked_data))
        avg = (np.nanmean(masked_data))
        # Append the raster file name and total value to the lists
        raster_file_names.append(raster_file)
        ET.append(total) # montlhy sum to m3/s

#%% Rainfall
# Get a list of all raster files in the folder
raster_files = glob.glob(folder_path + '/RainF*')

# Filter out files with excluded extensions
raster_files = [f for f in raster_files if not any(ext in f for ext in exclude_extensions)]

# Create lists to store raster file names and their corresponding total values
raster_file_names = []
RainF = []

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
        total = round(np.nansum(masked_data))
        avg = (np.nanmean(masked_data))
        # Append the raster file name and total value to the lists
        raster_file_names.append(raster_file)
        RainF.append(total) # montlhy sum to m3/s        

#%% Snowfall
# Get a list of all raster files in the folder
raster_files = glob.glob(folder_path + '/SnowF*')

# Filter out files with excluded extensions
raster_files = [f for f in raster_files if not any(ext in f for ext in exclude_extensions)]

# Create lists to store raster file names and their corresponding total values
raster_file_names = []
SnowF = []

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
        total = round(np.nansum(masked_data))
        avg = (np.nanmean(masked_data))
        # Append the raster file name and total value to the lists
        raster_file_names.append(raster_file)
        SnowF.append(total) # montlhy sum to m3/s        
                
#%% Rainfall Runoff
# Get a list of all raster files in the folder
raster_files = glob.glob(folder_path + '/Rainr*')

# Filter out files with excluded extensions
raster_files = [f for f in raster_files if not any(ext in f for ext in exclude_extensions)]

# Create lists to store raster file names and their corresponding total values
raster_file_names = []
RainR = []

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
        total = round(np.nansum(-masked_data))
        avg = (np.nanmean(masked_data))
        # Append the raster file name and total value to the lists
        raster_file_names.append(raster_file)
        RainR.append(total) # montlhy sum to m3/s        

#%% Snowmelt Runoff
# Get a list of all raster files in the folder
raster_files = glob.glob(folder_path + '/Snowr*')

# Filter out files with excluded extensions
raster_files = [f for f in raster_files if not any(ext in f for ext in exclude_extensions)]

# Create lists to store raster file names and their corresponding total values
raster_file_names = []
SnowR = []

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
        total = round(np.nansum(-masked_data))
        avg = (np.nanmean(masked_data))
        # Append the raster file name and total value to the lists
        raster_file_names.append(raster_file)
        SnowR.append(total) # montlhy sum to m3/s                 

#%% Glacier melt Runoff
# Get a list of all raster files in the folder
raster_files = glob.glob(folder_path + '/glacr/Glacr*')

# Filter out files with excluded extensions
raster_files = [f for f in raster_files if not any(ext in f for ext in exclude_extensions)]

# Create lists to store raster file names and their corresponding total values
raster_file_names = []
GlacR = []

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
        total = round(np.nansum(-masked_data))
        avg = (np.nanmean(masked_data))
        # Append the raster file name and total value to the lists
        raster_file_names.append(raster_file)
        GlacR.append(total) # montlhy sum to m3/s    

#%% Baseflow
# Get a list of all raster files in the folder
raster_files = glob.glob(folder_path + '/Baser*')

# Filter out files with excluded extensions
raster_files = [f for f in raster_files if not any(ext in f for ext in exclude_extensions)]

# Create lists to store raster file names and their corresponding total values
raster_file_names = []
BaseR = []

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
        total = round(np.nansum(-masked_data))
        avg = (np.nanmean(masked_data))
        # Append the raster file name and total value to the lists
        raster_file_names.append(raster_file)
        BaseR.append(total) # montlhy sum to m3/s    
#%% Change in storage?


#%% Plot in a barplot
savetitle = 'basinbalance_mth'
cet = (76/255, 153/255, 0/255)
crainf = (0/255, 0/255, 102/255)
csnowf = (102/255, 178/255, 255/255)
crainr = (102/255, 0/255, 204/255)
csnowr = (192/255, 192/255, 192/255)
cglacr = (96/255, 96/255, 96/255)
cbaser = (255/255, 128/255, 0/255)

positive_values = []
negative_values = [] 

positive_values = [RainF, SnowF]
negative_values = [ET, BaseR, RainR, SnowR, GlacR]

# Calculate the number of time steps
num_steps = len(positive_values[0])

# Set the y-axis limits manually to include negative values
y_min = min(min(negative_values))
y_max = max(max(positive_values))
plt.ylim(-2.1e6, 3.5e6)

# Create the stack plot with baseline set to "zero"
plt.stackplot(range(num_steps), positive_values, labels=['RainF', 'SnowF'], colors=[crainf, csnowf], baseline="zero")
plt.stackplot(range(num_steps), negative_values, labels=['ET',  'BaseR','RainR', 'SnowR', 'GlacR'], colors=[cet,  cbaser, crainr, csnowr, cglacr,], baseline="zero")

# Add a legend
plt.legend()

# Add a y-label
plt.ylabel('Values')

# Display the plot
plt.show()

# y
plt.savefig(f"{figdir}{savetitle}.png", dpi = 300)
plt.savefig(f"{figdir}{savetitle}.pdf", dpi = 300)
plt.tight_layout()
plt.show()

# Display the plot
plt.show()