# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 20:19:25 2023

@author: carol
"""
## Minimum temp instead

import matplotlib.pyplot as plt
import pandas as pd
import rasterio as rs
import numpy as np
import statistics
import os

figdir = ("C:/SPHY3/analysis/model_output/fig/dataplot/") # directory to save figure
os.chdir("D:\\UU\processed_files\\temp_maps\\20230323tmin\\") # directory to save maps
fn ='C:\\SPHY3\\analysis\\data_processed\\LSaws_Ta_filledwithERA_20132021min.csv' # time series
dempath = 'D:\\UU\\SPHY\\scratch\\v2\\dem_filled.tif' # dem location
start_date = '2017-01-01'
end_date = '2018-01-01'

csv_out = 'C:\\SPHY3\\analysis\\data_processed\\temp_min_output.csv'

#%% Import temperature time serie
# Read in the data
LS = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
LS['datetime'] = pd.to_datetime(LS['datetime'] )
dates = pd.DataFrame({'datetime': LS.index})

LS.set_index('datetime', inplace=True)

# Cut to specific date
LS = LS.loc[start_date:end_date]

# %% Open the file for reading
with rs.open(dempath)  as src:
    # Do something with the file, such as reading metadata or data
  src_crs = {'init':'EPSG:32645'}
  print(src.meta)
  dem= src.read(1)
"""
# Get spatial transform and dimensions
transform = src.transform
width = src.width
height = src.height
  
# Define x and y extent
xmin, ymin = transform * (0, height)
xmax, ymax = transform * (width, 0)
extent = [xmin, xmax, ymin, ymax]

# Plot DEM with colorbar
plt.imshow(dem, cmap='terrain', extent=extent)
plt.colorbar(label='Elevation (m)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
"""
#%% Elevation of the weather station
base_elevation = 4452

# Calculate the change in elevation from the chosen pixel to all other pixels
elev_diff = dem - base_elevation

# Create an empty raster
const_val = np.full(dem.shape, 1) # 

# Subset a section of the data as test
df = LS
#df = df.to_frame()

# ctreate alibrary of monlthy temperature gradients derived form network of station in basin
multipliers = {
    1: -0.0057,
    2: -0.0063,
    3: -0.007,
    4: -0.0066,
    5: -0.0054,
    6:-0.0051,
    7: -0.0047,
    8: -0.0050,
    9:-0.0048,
    10: -0.0055,
    11: -0.0056,
    12: -0.0055
}

avg_multiplier = statistics.mean(multipliers.values()) # average value for default if month are not represneted

# Define an empty list to hold reference values (sanity check)
multiplier_list = []
avgraster_list = []
ls_filled_values = []

# Loop over the rows in the dataframe
counter = 1
for date, row in df.iterrows():
    # Extract the month from the date
    month = date.month
 
    # Get the multiplier corresponding to the month
    multiplier = multipliers.get(month, -0.0057)
 
    # Calculate the raster for this date
    raster = const_val * row['LS_filled'] + (elev_diff * multiplier)
 
    # Calculate the raster for this date
    raster = const_val * row['LS_filled'] + (elev_diff*-0.0056)
    ls_filled_values.append(row['LS_filled']) # check to make sure it matches with LS filled value
    
    # Append the multiplier value to the list
    multiplier_list.append(multipliers[month])
    
    # Append the multiplier value to the list
    avg_value = np.mean(raster)
    avgraster_list.append(avg_value)
    
    # Define the metadata for the output raster
    meta = src.meta.copy()
    meta.update(count=1)

    # Define the output filename
    # Define the output filename
    output_filename = f"tmax{counter:07}.tif"
    output_filename = output_filename.replace('.tif', '')
    output_filename = output_filename[:8] + '.' + output_filename[8:]
    counter += 1
    
    # Write the output raster to disk
    with rs.open(output_filename, 'w', **meta) as out:
        out.write(raster, 1)

concat = pd.DataFrame({'datetime': LS.index, 'ls_filled':ls_filled_values, 'avgraster':avgraster_list, 'multiplier':multiplier_list})
concat.set_index('datetime', inplace=True)
df_concat = pd.concat([df, concat], axis =1)
df_concat.to_csv(csv_out)

