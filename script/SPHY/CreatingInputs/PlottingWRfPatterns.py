# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 11:20:28 2023

@author: carol
Figure of the WRF precipitation patterns

"""
#%% For precipitation
import matplotlib.pyplot as plt
import pandas as pd
import os
import rasterio
import geopandas as gpd
import rasterio.plot
import rasterio
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize


import calendar
os.chdir("D:\\UU\processed_files\\temp_maps\\20230324prec\\") #
os.environ["PROJ_LIB"] = "C:\\Users\\carol\\miniconda3\\envs\\spyder-env\\Lib\\site-packages\\pyproj\\proj_dir\\share\\proj\\"

# Location of langshisha AWS
lat = 371059 # in utm 45
lon = 3120355

# Import precipitation time series
fn = 'D:\\UU\\field_data\\processed\\Pdaily_Ls_infilledw_20120503_20210701.csv'
figdir = ("C:/SPHY3/analysis/model_output/fig/dataplot/") # directory to save figure

# Read in the data
meas = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['Time'] )
meas = meas.iloc[544:] # so its starts on the same date as temp: 29-oct-2013
# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)

# Cut # Start on Jan 1, 2014
start_date = '2014-01-01'
end_date = '2020-12-31'
meas = meas.loc[start_date:end_date]
meas = meas['Var1']*1.5

#%% Import shapefiles
path = "D:\\UU\\processed_files\\shapefile\\langshihsa_basin_outline\\LangshisaBasinandSide_outline_2mDEM.shp"
basinoutline = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\RGI_withingbasin.shp"
glacier = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\location_utm.shp"
location = gpd.read_file(path)

#%% Import the clipped wrf   
with rasterio.open('D:\\UU\\SPHY\\scratch\\wrfclipped5.tif') as src:
     # Read the metadata and data of the input raster
     metadata = src.meta
     data = src.read(1)
     bands = src.read()
     transform = src.transform
     data_extent = [src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
     rowval, colval = src.index(lat, lon)
    
# Define the number of rows and columns in the subplot grid
nrows, ncols = 4,3
# Create the figure and subplot grid
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(11, 8.5))
fig.subplots_adjust(hspace=0.25, wspace=0.01) # Adjust the horizontal and vertical spacing between subplots

# Loop through the bands and plot each one in a separate subplot
for i, band in enumerate(bands):
    # Compute the row and column indices for the current subplot
    row, col = i // ncols, i % ncols
    
    # Select the current subplot
    ax = axes[row, col]
    cmap = get_cmap('YlGn')
    norm = Normalize(vmin=band.min(), vmax=band.max())
    # Plot the current band in the subplot
    im = ax.imshow(band, cmap='YlGn', extent=data_extent, norm=norm)
    basinoutline.plot(ax=ax, facecolor='none', edgecolor='black')
    glacier.plot(ax=ax, facecolor='none', edgecolor='black')
    location.plot(ax=ax, markersize=1, facecolor='black', edgecolor='black')

    # Add labels and title to the subplot
    month = calendar.month_abbr[i+1]
    ax.set_title(month)
   # ax.set_title('Band {}'.format(i+1))
   # ax.set_xlabel('Longitude')
    #ax.set_ylabel('Latitude')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    # Set the xtick labels at a 45-degree angle
    #ax.set_yticklabels(ax.get_yticklabels(), rotation=45)
    # Add the colorbar to the subplot
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    #cbar.ax.set_ylabel('WRF Precip Gradient', rotation=270, labelpad=15)
# Add a common title to the figure
fig.suptitle('WRF Precipitation Gradient')

# Adjust the spacing between subplots and show the figure
plt.savefig(figdir + 'WRFprecipPatterns' + '.png', dpi = 300, bbox_inches='tight')
plt.show()


