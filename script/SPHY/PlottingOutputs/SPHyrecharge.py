# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:40:10 2023

@author: carol
"""


import os
import glob
import time
import rasterio
import rasterstats
import geopandas as gpd
import matplotlib.pyplot as plt
from itertools import islice
import pandas as pd

# Define the paths to the rasters and shapefile
raster_path = "C:/SPHY3/sphy_20230218/output_sphy_config_base14/"
glacperc_path = r"D:\\UU\\glacperc\\v2\\"
shapefile_path = r"D:\\UU\\modflow\\input\\fishnet_recharge.shp"
save_fig = 'D:/UU/figure/recharge_fig/v2/'

# Create a list of file names to loop through for the first raster
file_list1 = [f for f in glob.glob(raster_path + "SubpM*") if not f.endswith(".aux.xml")]

# Create a list of file names to loop through for the second raster
file_list2 = [f for f in glob.glob(glacperc_path + "Glacp*") if not f.endswith(".aux.xml")]

# Open the fishnet shapefile as a GeoDataFrame
fishnet = gpd.read_file(shapefile_path)
fishnet = fishnet.drop(columns=['_mean'])

# improt shapefile for plot
path = "D:\\UU\\processed_files\\shapefile\\langshihsa_basin_outline\\LangshisaBasinandSide_outline_2mDEM.shp"
basinoutline = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\RGI_withingbasin.shp"
glacier = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\location_utm.shp"
location = gpd.read_file(path)
 
path = "D:\\UU\\modflow\\result\\riv_shp_point.shp"
rivshp = gpd.read_file(path)  
rivshp['id'] = range(1, len(rivshp)+1)  

# Import the time seris to select times
path = 'D:/UU/modflow/recharge/Datetime_FileName_SPHY.csv'
tt = pd.read_csv(path)

#%%
idx1 =41
idx2 = 43
idx3 =45

ctn = 0
fig_name = 'rechARGE'
fig, axs = plt.subplots(1, 3, figsize=(12, 4))
for idx in [idx1, idx2, idx3]:
    file_path1 = file_list1[idx]
    file_path2 = file_list2[idx]
    
    # Open the raster file from raster_path1
    with rasterio.open(file_path1) as src1: # this is the subzone percolation
        # Read the raster data as a numpy array
        data1 = src1.read(1)
        grid_extent = [src1.bounds[0], src1.bounds[2], src1.bounds[1], src1.bounds[3]]
        
        data1[data1 > 1000] = 0
        data1[data1 < 0] = 0
        data1 = data1/30.417 # to  mm/day 
        data1 = data1 /(400*1000) # to o m/day

    # Open the raster file from raster_path2
    with rasterio.open(file_path2) as src2:
        # Read the raster data as a numpy array
        data2 = src2.read(1)

        data2[data2 > 1000] = 0
        data2[data2 < 0] = 0
        data2 = data2 /(400*1000)

    # Add the two rasters together
    data = data1 + data2

    # make a plot of the glacp, subp and the added result

    savetitle = 'RchSPHY_'+fig_name
    # Plot data1
    vmax = data.max()*400*1000
    vmin = 0
    im1 = axs[ctn].imshow(data*400*1000, extent=grid_extent, vmax = vmax, vmin=vmin, cmap = 'Blues')
    basinoutline.plot(ax=axs[ctn], facecolor='none', edgecolor='black')
    glacier.plot(ax=axs[ctn], facecolor='none', edgecolor='black')
    location.plot(ax=axs[ctn], markersize=1, facecolor='black', edgecolor='black')
    rivshp.plot(ax=axs[ctn], markersize=1, facecolor='black', edgecolor='black')
    cbar1 = plt.colorbar(im1, ax=axs[ctn], shrink=0.5)
    cbar1.set_label('Recharge (mm/d)')
    axs[ctn].set_title(tt['Time_Short'][idx])
    # Remove x and y tick labels
    axs[ctn].set_xticklabels([])
    axs[ctn].set_yticklabels([])
    ctn = ctn+1

plt.tight_layout()
plt.savefig(f"{save_fig}{savetitle}.png", dpi = 300)
plt.savefig(f"{save_fig}{savetitle}.pdf", dpi = 300)                  
                
 #%%$               
                
                