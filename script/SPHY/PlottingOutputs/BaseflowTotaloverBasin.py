# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:07:50 2023

@author: carol
"""

# compate baseflowto riv leakage + drainage


# make the sum of the monthly baseflow maps, clipped to the basin area

# to make a time series of baseflow contribution to streams
import rasterio
import numpy as np
import glob
import geopandas as gpd
from rasterio.mask import mask
import matplotlib.pyplot as plt
import pandas as pd

fig_dir  ='D:\\UU\\figure\\modflow_recharge\\20230420\\'
# Specify the folder path and the mask file name
folder_path = 'C:/SPHY3/sphy_20230218/output_sphy_config_base16_2/'  # Replace with your actual folder path
mask_file = 'D:/UU/SPHY/scratch/basinoutline.shp'  # Replace with your actual mask file name
mask_data = gpd.read_file(mask_file)
# Get the geometry of the mask as a GeoJSON-like object
mask_geometry = mask_data.geometry.values[0]

# Define the list of file extensions to exclude
exclude_extensions = ['.tss', '.csv', '.aux', '.map']

# Get a list of all raster files in the folder
raster_files = glob.glob(folder_path + '/BTot*')

# Filter out files with excluded extensions
raster_files = [f for f in raster_files if not any(ext in f for ext in exclude_extensions)]

# Create lists to store raster file names and their corresponding total values
raster_file_names = []
total_values = []


# Loop through each raster file
for raster_file in raster_files:
    # Open the raster file for reading
    with rasterio.open(raster_file) as src:
        # Clip the raster to the extent of the mask
        masked_data, masked_transform = mask(src, [mask_geometry], crop=True)
        
        # Set masked values to NaN
        masked_data = np.where(masked_data == src.nodata, np.nan, masked_data)
       
        # Sum the values of the raster to obtain the total
        total = np.nansum(masked_data)
        # Append the raster file name and total value to the lists
        raster_file_names.append(raster_file)
        total_values.append(total/30) # montlhy sum to m3/s
        
        plt.imshow(masked_data[0], cmap='gray')
        
        plt.colorbar()
        plt.title(f'{raster_file} (Total: {total})')
        plt.show()
        
'''        
# Create a dataframe from the lists
df = pd.DataFrame({'Raster_File': raster_file_names, 'Total_Value': total_values})
df.to_csv(fig_dir+'/SPHY_Basin_BaseflowSum.csv')
'''