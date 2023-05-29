# -*- coding: utf-8 -*-
"""
PLOTTING MODELLED RECHARGE

This script imports the boundary conditions of the modflow model and extracts the recharge values, 
and plots them in both a time series and map (for a given set of time steps)

Created on Tue Apr  4 16:48:07 2023

@author: carol
"""
import matplotlib.pyplot as plt

import flopy

import pandas as pd
import rasterio
import geopandas as gpd
import rasterio.features

import glob
import datetime

#%% Set paths
modelname = "mod5_21.nam"
cbcname = 'mod5_21'
modelpath  = "D:\\UU\\modflow\\20230413\\"
fig_dir  ='D:\\UU\\figure\\modflow_recharge\\20230413\\'

"""
modelname = "mod4_02.nam"
cbcname = 'mod4_02'
modelpath  = "D:\\UU\\modflow\\20230408\\"
fig_dir  ='D:\\UU\\figure\\modflow_recharge\\20230408\\'
"""

#%% Load model DEm to have elevation of cells
model_ws = modelpath
ml = flopy.modflow.Modflow.load(
    modelname,
    model_ws=modelpath,
    verbose=False,
    check=False,
    exe_name="mfnwt",
)

dem =ml.dis.top.array 

#%% Import shapefiles
path = "D:\\UU\\processed_files\\shapefile\\langshihsa_basin_outline\\LangshisaBasinandSide_outline_2mDEM.shp"
basinoutline = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\RGI_withingbasin.shp"
glacier = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\location_utm.shp"
location = gpd.read_file(path)
     
#%% improt dem
with rasterio.open('D:\\UU\\modflow\\result\\grid_raster.tif') as src:
     # Read the metadata and data of the input raster
     metadata_dem = src.meta
     grid = src.read(1)
     grid_extent = [src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
    # Get the affine transformation matrix
     transform = src.transform
# Get 4 locations to look at heads across the basin
#loc1: outlet
#loc 2: GW1

#loc 3 Glacier toe: row 200, 150
#loc 4:  near glacier top  : row 200, 500 
    # Define the UTM point coordinates
pt = location.iloc[1]
x, y = pt.geometry.x, pt.geometry.y
row1, col1 = rasterio.transform.rowcol(transform, x, y)

    # Define the UTM point coordinates
pt = location.iloc[0]
x, y = pt.geometry.x, pt.geometry.y
row2, col2 = rasterio.transform.rowcol(transform, x, y)

row3, col3 = 200, 150
row4, col4 = 200, 500

loc1 = round(dem[row1, col1])
loc2 = round(dem[row2, col2])
loc3 = round(dem[row3, col3])
loc4 = round(dem[row4, col4])

#%% Import modflow model
# Create a list of all the .bhd files in the folder
cbc_files = glob.glob(modelpath + "*.cbc")

# Loop over each .bhd file in the folder
#for i, cbc_file in enumerate(cbc_files):
    # Extract the file name without extension
    #modname = os.path.splitext(os.path.basename(cbc_file))[0]
    
# Extract the heads -- if just one file!
cbc = flopy.utils.CellBudgetFile(modelpath + cbcname + '.cbc')   
# Get the list of records in the model.cbc file
records = cbc.list_records()
# Read the recharge data from the model.cbc file
recharge_data = cbc.get_data(text='RECHARGE')

#%% create a time array
# Define start date
start_date = datetime.datetime(2013, 12, 22) # start of period - 1 day for the seady state start

# Calculate end date
num_timesteps = len(recharge_data)
time_step_days = 30
end_date = start_date + datetime.timedelta(days=num_timesteps * time_step_days)

# Create an array of datetime objects for each time step
time_array = [start_date + datetime.timedelta(days=i*time_step_days) for i in range(num_timesteps)]

# Extract only the date part of the datetime objects
date_array = [dt.date() for dt in time_array]



#%% Create a new figure with 2x2 subplots
#id = [244, 486, 609, 852]
id = [ 47, 53, 59, 65]
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8, 6))
fig.suptitle(f"{cbcname}")

# Loop through the index values and plot recharge on each subplot
for i, idx in enumerate(id):
    # Get the date and recharge data for the current index
    date = date_array[idx]
    rch = recharge_data[idx]
    #rch_md = rch*400*1000
    # Plot the recharge on the corresponding subplot
    row = i // 2
    col = i % 2
    im = axs[row, col].imshow(rch*1000, extent=grid_extent)#, vmin=0, vmax=0.25)
    basinoutline.plot(ax=axs[row, col], facecolor='none', edgecolor='black')
    glacier.plot(ax=axs[row, col], facecolor='none', edgecolor='black')
    location.plot(ax=axs[row, col], markersize=1, facecolor='black', edgecolor='black')
    cbar = plt.colorbar(im, ax=axs[row, col], shrink=0.5)
    cbar.set_label('Recharge (mm/d)')

    # Set subplot title with the corresponding date
    axs[row, col].set_title(f"Recharge ({date.strftime('%Y-%m-%d')})")

    # Remove x and y tick labels
    axs[row, col].set_xticklabels([])
    axs[row, col].set_yticklabels([])

        # figure na,e
plt.tight_layout()
plt.savefig(fig_dir + cbcname + 'Recharge_Map.png', dpi=300, bbox_inches='tight')
plt.show()
#%% Time series

    # get the head time series
step_size = 30
    # create an empty DataFrame with columns for each well and each head
columns = ['hd1_well1', 'hd1_well2', 'hd1_well3', 'hd1_well4']
rch_well = pd.DataFrame(columns=columns)
    
for i, rch in enumerate(recharge_data):
    rch_df = pd.DataFrame(rch)
    rch_well.loc[i, 'hd1_well1'] = rch_df.iloc[row1, col1]*1000
    rch_well.loc[i, 'hd1_well2'] = rch_df.iloc[row2, col2] *1000
    rch_well.loc[i, 'hd1_well3'] = rch_df.iloc[row3, col3]*1000
    rch_well.loc[i, 'hd1_well4'] = rch_df.iloc[row4, col4]*1000
    
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(13, 7), 
                            gridspec_kw={'wspace': 0.5, 'hspace': 0.3})
fig.suptitle(f"{cbcname}, Recharge (m/day)")
    
# set font sizes for tick labels and titles
tick_font_size = 8
title_font_size = 10

# subplot 1
axs[0, 0].plot(date_array, rch_well['hd1_well1'])
axs[0, 0].set_title('Outlet, lyr 1, ' + str(loc1) + 'm', fontsize=title_font_size)
axs[0, 0].tick_params(labelsize=tick_font_size)
axs[0, 0].tick_params(axis='x', rotation=30)
axs[0, 0].grid(True) # Add gridlines

# subplot 2
axs[0, 1].plot(date_array, rch_well['hd1_well2'])
axs[0, 1].set_title('Well1, lyr 1, ' + str(loc2) + 'm', fontsize=title_font_size)
axs[0, 1].tick_params(labelsize=tick_font_size)
axs[0, 1].tick_params(axis='x', rotation=30)
axs[0, 1].grid(True) # Add gridlines

# subplot 3
axs[1, 0].plot(date_array, rch_well['hd1_well3'])
axs[1, 0].set_title('Gl. Toe, lyr 1, ' + str(loc3) + 'm', fontsize=title_font_size)
axs[1, 0].tick_params(labelsize=tick_font_size)
axs[1, 0].tick_params(axis='x', rotation=30)
axs[1, 0].grid(True) # Add gridlines

# subplot 4
axs[1, 1].plot(date_array, rch_well['hd1_well4'])
axs[1, 1].set_title('Gl. Head, lyr 1, ' + str(loc4) + 'm', fontsize=title_font_size)
axs[1, 1].tick_params(labelsize=tick_font_size)
axs[1, 1].tick_params(axis='x', rotation=30)
axs[1, 1].grid(True) # Add gridlines

        # figure na,e
plt.tight_layout()
plt.savefig(fig_dir + cbcname + 'Recharge_timeseries.png', dpi=300, bbox_inches='tight')
plt.show()