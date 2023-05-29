# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:00:38 2023

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
# Define the paths to the rasters and shapefile
raster_path = "C:/SPHY3/sphy_20230218/output_sphy_config_base16_2/"
glacperc_path = r"D:\\UU\\glacperc\\v4\\"
shapefile_path = r"D:\\UU\\modflow\\input\\fishnet_recharge.shp"
save_fig = 'D:/UU/figure/recharge_fig/v4/'

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
vmin = 0
vmax = 10
counter =0
start_time = time.time()

# Specify the number of files you want to process
num_files = 84 # for 36 files for now!!!
# Loop through the raster files in file_list1 and file_list2 simultaneously
for file_path1, file_path2 in islice(zip(file_list1, file_list2), num_files):
    
    #file_path1 = "C:/SPHY3/sphy_20230218/output_sphy_config_base14/SubpM000.212"
    #file_path2 = "D:\\UU\\glacperc\\v2\\GlacpM000.212"
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

    # Extract the mean value of the raster over each polygon of the fishnet
    stats = rasterstats.zonal_stats(
        fishnet.geometry,
        data,
        affine=src1.transform,
        nodata=src1.nodata,
        stats=["mean"],
    )

    file_name1 = os.path.basename(file_path1)
    fig_name = 'GW' + file_name1[-5:].replace('.', '')  

    # Add the mean value to the fishnet GeoDataFrame
    fishnet[fig_name] = [stat['mean'] for stat in stats]
    elapsed_time = time.time() - start_time
    counter = counter + 1
    print(f"Time elapsed: {elapsed_time:.2f} seconds, n = {counter}")
    
    # make a plot of the glacp, subp and the added result
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    savetitle = 'RchSPHY_'+fig_name
    # Plot data1
    vmax = data.max()*400*1000
    vmin = 0
    im1 = axs[0].imshow(data1*400*1000, extent=grid_extent, vmax = vmax, vmin=vmin)
    basinoutline.plot(ax=axs[0], facecolor='none', edgecolor='black')
    glacier.plot(ax=axs[0], facecolor='none', edgecolor='black')
    location.plot(ax=axs[0], markersize=1, facecolor='black', edgecolor='black')
    rivshp.plot(ax=axs[0], markersize=1, facecolor='black', edgecolor='black')
    cbar1 = plt.colorbar(im1, ax=axs[0], shrink=0.5)
    cbar1.set_label('Recharge (mm/d)')
    axs[0].set_title('Subp '+fig_name)
    # Remove x and y tick labels
    axs[0].set_xticklabels([])
    axs[0].set_yticklabels([])
    # Plot data2
    im2 = axs[1].imshow(data2*400*1000, extent=grid_extent, vmax = vmax, vmin=vmin)
    basinoutline.plot(ax=axs[1], facecolor='none', edgecolor='black')
    glacier.plot(ax=axs[1], facecolor='none', edgecolor='black')
    location.plot(ax=axs[1], markersize=1, facecolor='black', edgecolor='black')
    rivshp.plot(ax=axs[1], markersize=1, facecolor='black', edgecolor='black')
    cbar2 = plt.colorbar(im2, ax=axs[1], shrink=0.5)
    cbar2.set_label('Recharge (mm/d)')
    axs[1].set_title('Glacp '+fig_name)
    # Remove x and y tick labels
    axs[1].set_xticklabels([])
    axs[1].set_yticklabels([])
    # Plot data (data1 + data2)
    im = axs[2].imshow(data*400*1000, extent=grid_extent, vmax = vmax, vmin=vmin)
    basinoutline.plot(ax=axs[2], facecolor='none', edgecolor='black')
    glacier.plot(ax=axs[2], facecolor='none', edgecolor='black')
    location.plot(ax=axs[2], markersize=1, facecolor='black', edgecolor='black')
    rivshp.plot(ax=axs[2], markersize=1, facecolor='black', edgecolor='black')
    cbar = plt.colorbar(im, ax=axs[2], shrink=0.5)
    cbar.set_label('Recharge (mm/d)')
    axs[2].set_title('Glacp + Subp '+fig_name)
    # Remove x and y tick labels
    axs[2].set_xticklabels([])
    axs[2].set_yticklabels([])
    # Adjust subplot layout
    plt.tight_layout()
    plt.savefig(f"{save_fig}{savetitle}.png", dpi = 300)
    plt.savefig(f"{save_fig}{savetitle}.pdf", dpi = 300)
    # Show the plot
    plt.show()

# keep only first 84 (2014-2020)

fishnet = fishnet.iloc[:, :86]
# Save the updated fishnet shapefile as a new file
fishnet.to_file("D:\\UU\\modflow\\recharge\\recharge_fishnet_20230420_1.shp")



"""
#%% Plot a time series of the recharge

# Define the paths to the rasters and shapefile
raster_path = "C:/SPHY3/sphy_20230218/output_sphy_config_base14/"
glacperc_path = r"D:\\UU\\glacperc\\v2\\"
shapefile_path = r"D:\\UU\\modflow\\input\\fishnet_recharge.shp"
save_fig = 'D:/UU/figure/recharge_fig/v2/'

# Create a list of file names to loop through for the first raster
file_list1 = [f for f in glob.glob(raster_path + "SubpM*") if not f.endswith(".aux.xml")]

# Create a list of file names to loop through for the second raster
file_list2 = [f for f in glob.glob(glacperc_path + "Glacp*") if not f.endswith(".aux.xml")]

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
vmin = 0
vmax = 10
counter =0
start_time = time.time()

# Specify the number of files you want to process
num_files = 168 # for 36 files for now!!!
# Loop through the raster files in file_list1 and file_list2 simultaneously
for file_path1, file_path2 in islice(zip(file_list1, file_list2), num_files):
    
    #file_path1 = "C:/SPHY3/sphy_20230218/output_sphy_config_base14/SubpM000.212"
    #file_path2 = "D:\\UU\\glacperc\\v2\\GlacpM000.212"
    # Open the raster file from raster_path1
    with rasterio.open(file_path1) as src1: # this is the subzone percolation
        # Read the raster data as a numpy array
        data1 = src1.read(1)
        grid_extent = [src1.bounds[0], src1.bounds[2], src1.bounds[1], src1.bounds[3]]
        
        data1[data1 > 1000] = 0
        data1[data1 < 0] = 0
        data1 = data1/30 
        data1 = data1 /(400*1000) # to m/day

    # Open the raster file from raster_path2
    with rasterio.open(file_path2) as src2:
        # Read the raster data as a numpy array
        data2 = src2.read(1)

        data2[data2 > 1000] = 0
        data2[data2 < 0] = 0
        data2 = data2 /(400*1000)

    # Add the two rasters together
    data = data1 + data2


    file_name1 = os.path.basename(file_path1)
    fig_name = 'GW' + file_name1[-5:].replace('.', '')  

  # extract the values at specific locations
  
  
    # make a plot of the glacp, subp and the added result
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    savetitle = 'RchSPHY_'+fig_name
    # Plot data1
    vmax = data.max()*400*1000
    vmin = 0
    im1 = axs[0].imshow(data1*400*1000, extent=grid_extent, vmax = vmax, vmin=vmin)
    basinoutline.plot(ax=axs[0], facecolor='none', edgecolor='black')
    glacier.plot(ax=axs[0], facecolor='none', edgecolor='black')
    location.plot(ax=axs[0], markersize=1, facecolor='black', edgecolor='black')
    rivshp.plot(ax=axs[0], markersize=1, facecolor='black', edgecolor='black')
    cbar1 = plt.colorbar(im1, ax=axs[0], shrink=0.5)
    cbar1.set_label('Recharge (mm/d)')
    axs[0].set_title('Subp '+fig_name)
    # Remove x and y tick labels
    axs[0].set_xticklabels([])
    axs[0].set_yticklabels([])
    # Plot data2
    im2 = axs[1].imshow(data2*400*1000, extent=grid_extent, vmax = vmax, vmin=vmin)
    basinoutline.plot(ax=axs[1], facecolor='none', edgecolor='black')
    glacier.plot(ax=axs[1], facecolor='none', edgecolor='black')
    location.plot(ax=axs[1], markersize=1, facecolor='black', edgecolor='black')
    rivshp.plot(ax=axs[1], markersize=1, facecolor='black', edgecolor='black')
    cbar2 = plt.colorbar(im2, ax=axs[1], shrink=0.5)
    cbar2.set_label('Recharge (mm/d)')
    axs[1].set_title('Glacp '+fig_name)
    # Remove x and y tick labels
    axs[1].set_xticklabels([])
    axs[1].set_yticklabels([])
    # Plot data (data1 + data2)
    im = axs[2].imshow(data*400*1000, extent=grid_extent, vmax = vmax, vmin=vmin)
    basinoutline.plot(ax=axs[2], facecolor='none', edgecolor='black')
    glacier.plot(ax=axs[2], facecolor='none', edgecolor='black')
    location.plot(ax=axs[2], markersize=1, facecolor='black', edgecolor='black')
    rivshp.plot(ax=axs[2], markersize=1, facecolor='black', edgecolor='black')
    cbar = plt.colorbar(im, ax=axs[2], shrink=0.5)
    cbar.set_label('Recharge (mm/d)')
    axs[2].set_title('Glacp + Subp '+fig_name)
    # Remove x and y tick labels
    axs[2].set_xticklabels([])
    axs[2].set_yticklabels([])
    # Adjust subplot layout
    plt.tight_layout()
    plt.savefig(f"{save_fig}{savetitle}.png", dpi = 300)
    plt.savefig(f"{save_fig}{savetitle}.pdf", dpi = 300)
    # Show the plot
    plt.show()
    """