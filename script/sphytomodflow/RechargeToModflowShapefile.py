# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:49:47 2023

@author: carol

In this script, I want to change the SPHY GW recharge to a shapefile map that I can import in modelmuse
- import gw recharge maps
- import 60m fishnet grid

- zonal statistics: assign value of gw recharge to a new field in the fishnet
- make a table with the month value and the name of the field

"""

import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import geopandas as gpd
import rasterstats 
import numpy as np
import glob
from rasterio.mask import geometry_mask
import rasterio.plot 
import matplotlib.pyplot as plt
import time

#%% 

# Define the paths to the rasters and shapefile
raster_path = r"C:\\SPHY3\\sphy_20230218\\output_20230325\\"
shapefile_path = r"D:\\UU\\modflow\\input\\fishnet_recharge.shp"
save_fig = 'D:/UU/figure/recharge_fig/'
# Create a list of file names to loop through
file_list = [f for f in glob.glob(raster_path + "GwreM*") if not f.endswith(".aux.xml")]

# Open the fishnet shapefile as a GeoDataFrame
fishnet = gpd.read_file(shapefile_path)
fishnet = fishnet.drop(columns=['_mean'])

vmin = 0
vmax = 200
counter = 1
start_time = time.time()

# Loop through the raster files
for file_path in file_list:
    # Open the raster file
    with rasterio.open(file_path) as src:
        # Read the raster data as a numpy array
        data = src.read(1)

        data[data > 1000] = 0
        data[data < 0] = 0
        data = data /(400*1000)
        
        # Extract the mean value of the raster over each polygon of the fishnet
        stats = rasterstats.zonal_stats(
        fishnet.geometry,
        data,
        affine=src.transform,
        nodata=src.nodata,
        stats=["mean"],
        )
        
        file_name = os.path.basename(file_path)
        fig_name = 'GW' + file_name[-5:].replace('.', '')  
        """
        plt.title('Groundwater Recharge, m/d, '+ fig_name)
         # Plot the raster
        plt.imshow(data, cmap='viridis', vmin=vmin, vmax=vmax)
        plt.colorbar() 
        # Save the plot as a png file
        plt.savefig(save_fig+fig_name+'.png', dpi=300, bbox_inches='tight')
        plt.close()
        """      
        # Add the mean value to the fishnet GeoDataFrame
        file_name = os.path.basename(file_path)
        fishnet[fig_name] = [stat['mean'] for stat in stats]
        elapsed_time = time.time() - start_time
        counter = counter + 1
        print(f"Time elapsed: {elapsed_time:.2f} seconds, n = {counter}")
        
      

# Save the updated fishnet shapefile as a new file
fishnet.to_file("D:\\UU\\modflow\\recharge\\recharge_fishnet_20230403.shp")


#%% I also want to create a list of month and duration associated with the file name
"""
#%% Lets try this  - mutliprocessing
import multiprocessing
from functools import partial

# Define the function that will process each raster file
def process_raster(file_path, fishnet):
    # Open the raster file
    with rasterio.open(file_path) as src:
        # Read the raster data as a numpy array
        data = src.read(1)
        # Set values above 1000 to 0
        data[data > 1000] = 0
        data[data < 0] = 0

        # Extract the mean value of the raster over each polygon of the fishnet
        stats = rasterstats.zonal_stats(
        fishnet.geometry,
        data,
        affine=src.transform,
        nodata=src.nodata,
        stats=["mean"],
    )

    # Add the mean value to the fishnet GeoDataFrame
    file_name = os.path.basename(file_path)
    fishnet[file_name] = [stat['mean'] for stat in stats]

# Define the paths to the rasters and shapefile
raster_path = r"C:\\SPHY3\\sphy_20230218\\output_20230325\\"
shapefile_path = r"D:\\UU\\modflow\\input\\fishnet_recharge.shp"

# Create a list of file names to loop through
file_list = [f for f in glob.glob(raster_path + "GwreM*") if not f.endswith(".aux.xml")]

# Open the fishnet shapefile as a GeoDataFrame
fishnet = gpd.read_file(shapefile_path)
fishnet = fishnet.drop(columns=['_mean'])

# Create a partial function to pass the fishnet to each worker
partial_process_raster = partial(process_raster, fishnet=fishnet)

# Create a pool of workers and process each raster file in parallel
with multiprocessing.Pool() as pool:
    pool.map(partial_process_raster, file_list)

# Save the updated fishnet shapefile as a new file
fishnet.to_file("D:\\UU\\modflow\\recharge\\output.shp")

# 
"""