# -*- coding: utf-8 -*-
"""

Plot the tiff file that are inputs for SPHY

Created on Fri May 26 13:34:06 2023

@author: carol
"""

import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
from rasterio.plot import show
from mpl_toolkits.axes_grid1 import make_axes_locatable

#%% Import shapefiles
# Set the file paths for the GeoTIFF files and shapefile

soil_thickness = 'C:/SPHY3/sphy_20230218/input_20230322/soil/soilthickness.map'
sandratio = 'C:/SPHY3/sphy_20230218/input_20230322/soil/sand_ratio_top2.map'
clayratio = 'C:/SPHY3/sphy_20230218/input_20230322/soil/clay_ratio_top2.map'
organicratio = 'C:/SPHY3/sphy_20230218/input_20230322/soil/organic_ratio_top2.map'

# Import shapefile
path = "D:\\UU\\processed_files\\shapefile\\langshihsa_basin_outline\\LangshisaBasinandSide_outline_2mDEM.shp"
basinoutline = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\RGI_withingbasin.shp"
glacier = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\location_utm.shp"
location = gpd.read_file(path)
 
path = "D:/UU\processed_files/shapefile/langshihsa_surfacestream/surfacestream_20230420_2.shp"
rivshp = gpd.read_file(path)  
rivshp['id'] = range(1, len(rivshp)+1)  

# Saving directory
save_fig = 'D:/UU/figure/inputs/'

with rasterio.open(soil_thickness) as src1:
        grid_extent = [src1.bounds[0], src1.bounds[2], src1.bounds[1], src1.bounds[3]]
        # Read the raster data as a numpy array
        soilthick = src1.read(1)
with rasterio.open(sandratio) as src1:
        grid_extent = [src1.bounds[0], src1.bounds[2], src1.bounds[1], src1.bounds[3]]
        # Read the raster data as a numpy array
        sand = src1.read(1)
with rasterio.open(clayratio) as src1:
        grid_extent = [src1.bounds[0], src1.bounds[2], src1.bounds[1], src1.bounds[3]]
        # Read the raster data as a numpy array
        clay = src1.read(1)        
with rasterio.open(organicratio) as src1:
        grid_extent = [src1.bounds[0], src1.bounds[2], src1.bounds[1], src1.bounds[3]]
        # Read the raster data as a numpy array
        organic = src1.read(1)
        
# plot figure        
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
savetitle = 'Soil_Maps'

# Plot for Soil thickness
im1 = axs[0, 0].imshow(soilthick, extent=grid_extent, cmap='Blues')
basinoutline.plot(ax=axs[0, 0], facecolor='none', edgecolor='black')
glacier.plot(ax=axs[0, 0], facecolor='none', edgecolor='black')
location.plot(ax=axs[0, 0], markersize=2, facecolor='black', edgecolor='black')
rivshp.plot(ax=axs[0, 0], linewidth=0.5, facecolor='none', edgecolor='black')
cbar1 = plt.colorbar(im1, ax=axs[0, 0], shrink=0.6)
cbar1.set_label('(mm)')
axs[0, 0].set_title('Soil Thickness')
axs[0, 0].set_xticklabels([])
axs[0, 0].set_yticklabels([])

# Plot for Sand ratio
im2 = axs[0, 1].imshow(sand, extent=grid_extent, cmap='Oranges')
basinoutline.plot(ax=axs[0, 1], facecolor='none', edgecolor='black')
glacier.plot(ax=axs[0, 1], facecolor='none', edgecolor='black')
location.plot(ax=axs[0, 1], markersize=2, facecolor='black', edgecolor='black')
rivshp.plot(ax=axs[0, 1], linewidth=0.5, facecolor='none', edgecolor='black')
cbar2 = plt.colorbar(im2, ax=axs[0, 1], shrink=0.6)
cbar2.set_label('(%)')
axs[0, 1].set_title('Sand Content')
axs[0, 1].set_xticklabels([])
axs[0, 1].set_yticklabels([])

# Plot for Clay ratio
im3 = axs[1, 0].imshow(clay, extent=grid_extent, cmap='Reds')
basinoutline.plot(ax=axs[1, 0], facecolor='none', edgecolor='black')
glacier.plot(ax=axs[1, 0], facecolor='none', edgecolor='black')
location.plot(ax=axs[1, 0], markersize=2, facecolor='black', edgecolor='black')
rivshp.plot(ax=axs[1, 0], linewidth=0.5, facecolor='none', edgecolor='black')
cbar3 = plt.colorbar(im3, ax=axs[1, 0], shrink=0.6)
cbar3.set_label('(%)')
axs[1, 0].set_title('Clay Content')
axs[1, 0].set_xticklabels([])
axs[1, 0].set_yticklabels([])

# Plot for Organic ratio
im4 = axs[1, 1].imshow(organic, extent=grid_extent, cmap='Greens')
basinoutline.plot(ax=axs[1, 1], facecolor='none', edgecolor='black')
glacier.plot(ax=axs[1, 1], facecolor='none', edgecolor='black')
location.plot(ax=axs[1, 1], markersize=2, facecolor='black', edgecolor='black')
rivshp.plot(ax=axs[1, 1], linewidth=0.5, facecolor='none', edgecolor='black')
cbar4 = plt.colorbar(im4, ax=axs[1, 1], shrink=0.6)
cbar4.set_label('(%)')
axs[1, 1].set_title('Organic Matter Content')
axs[1, 1].set_xticklabels([])
axs[1, 1].set_yticklabels([])

# Adjust the spacing between subplots
plt.subplots_adjust(wspace=0, hspace=0)
plt.tight_layout()

# Save the figure as PNG and PDF
plt.savefig(save_fig + savetitle + '.png', dpi=300)
plt.savefig(save_fig + savetitle + '.pdf')

# Display the plot
plt.show()