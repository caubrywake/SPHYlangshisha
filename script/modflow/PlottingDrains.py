# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:03:34 2023

@author: carol
"""

# modeflow output for drains
# -*- coding: utf-8 -*-
"""
# Plotting river Leakage

Created on Mon Apr 10 20:24:28 2023

@author: carol
"""
import matplotlib.pyplot as plt

import flopy

import pandas as pd
import rasterio
import geopandas as gpd
import rasterio.features
import numpy as np
import glob
import datetime

#%% Set paths
modelname = "mod6_02.nam"
cbcname = 'mod6_02'
modelpath  = "D:\\UU\\modflow\\20230420\\"
fig_dir  ='D:\\UU\\figure\\modflow_recharge\\20230420\\'

cbc_files = glob.glob(modelpath + "*.cbc")

# Loop over each .bhd file in the folder
#for i, cbc_file in enumerate(cbc_files):
    # Extract the file name without extension
    #modname = os.path.splitext(os.path.basename(cbc_file))[0]
    
# Extract the heads -- if just one file!
cbc = flopy.utils.CellBudgetFile(modelpath + cbcname + '.cbc')   
# Get the list of records in the model.cbc file
records = cbc.list_records()

#%% Import shapefiles
path = "D:\\UU\\processed_files\\shapefile\\langshihsa_basin_outline\\LangshisaBasinandSide_outline_2mDEM.shp"
basinoutline = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\RGI_withingbasin.shp"
glacier = gpd.read_file(path)

path = "D:\\UU\\SPHY\\scratch\\location_utm.shp"
location = gpd.read_file(path)
     
path = "D:/UU\processed_files/shapefile/langshihsa_surfacestream/surfacestream_20230420_2.shp"
rivshp = gpd.read_file(path)  

# grid raster is an empty grid to have the coordinate of the modelled results.
with rasterio.open('D:\\UU\\modflow\\result\\grid_raster.tif') as src:
     # Read the metadata and data of the input raster
     metadata_dem = src.meta
     grid = src.read(1)
     grid_extent = [src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
     transform = src.transform


#%%
# Load the model
model_ws = 'D:\\UU\\modflow\\20230420\\'
model_name = 'mod6_02.nam'
model = flopy.modflow.Modflow.load(model_name, model_ws=model_ws)

    
# Read the recharge data from the model.cbc file
drains_data = cbc.get_data(text='DRAINS')

# Get the model grid
dis = model.get_package('DIS')
times = dis.get_totim()

import datetime

# Set the starting date
start_date = datetime.datetime(2013, 12, 31)

date_times = []
for time in times:
    delta_days = int(time)
    delta_seconds = int((time - delta_days) * 86400)
    delta = datetime.timedelta(days=delta_days, seconds=delta_seconds)
    date_time = start_date + delta
    rounded_date_time = date_time.replace(hour=0, minute=0, second=0, microsecond=0)
    date_times.append(rounded_date_time.strftime('%Y-%m-%d'))

print(date_times)
tgoal = '2017-08-05'
tstep = tt[tt['datetime'] == tgoal].index[0]


# Set the plot figure size
figsize = (10, 10)
drain_sums = []


# Loop through each stress period and plot the data for the first time step of each period
for i in range(dis.nper):
    i = tstep
    drain_values = drains_data[i]['q']
    drain_values = drain_values[93:]
    # Reshape the data into a grid
    rows = dis.nrow
    cols = dis.ncol
    
    drain_values_grid = drain_values.reshape(cols, -1).T
    # Calculate the sum of drain values and append to the list
    drain_sums.append(np.sum(drain_values_grid))
    

    # Create the plot
    fig, ax = plt.subplots(figsize=(8,6))
    im = ax.imshow(drain_values_grid*1000/400, extent=grid_extent, cmap='Blues_r', vmin = -10, vmax =0)
    basinoutline.plot(ax=ax, facecolor='none', edgecolor='black')
    glacier.plot(ax=ax, facecolor='none', edgecolor='black')
    rivshp.plot(ax=ax, linewidth=0.5, facecolor='none', edgecolor='black') 
    location.plot(ax=ax, markersize=1, facecolor='black', edgecolor='black')
    cbar1 = plt.colorbar(im, ax=ax, shrink=0.5)
    cbar1.set_label('Drains (mm/day)')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(f"Drains ({tgoal})")

    plt.tight_layout()
    plt.savefig(fig_dir + modelname + '_Drains2_time_step_{}.png'.format(round(times[tstep])), dpi=300, bbox_inches='tight')
    plt.savefig(fig_dir + modelname + '_Drains2_time_step_{}.pdf'.format(round(times[tstep])), dpi=300, bbox_inches='tight')
    plt.show()  
  
df = pd.DataFrame({'timestep': date_array, 'Total_Value': total_values})
df.to_csv(fig_dir+'/MODFLOW_riverleakage_Basin.csv')



#%% Import coordinate grid 





         
# Read the recharge data from the model.cbc file
drains_data = cbc.get_data(text='DRAINS')

# Loop over the periods in drains_data
for period in range(len(drains_data)):
    
    # Get the drain values for the current period
    drain_values = drains_data[period]['q']

    # Append NaN rows to the drain values
    drains_vals = np.array(drain_values)
    nan_rows = np.empty((300, 1))
    nan_rows[:] = np.nan
    drain_values2 = np.concatenate([nan_rows.flatten(), drains_vals])

    # Reshape the drain values into a grid
    drain_values_grid = drain_values2.reshape(cols, -1).T

    # Create a new figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the grid using imshow
    im = ax.imshow(drain_values_grid,extent=grid_extent, cmap='Blues', vmin=-10, vmax=0)
    basinoutline.plot(ax=ax, facecolor='none', edgecolor='black')
    glacier.plot(ax=ax, facecolor='none', edgecolor='black')
    rivshp.plot(ax=ax, linewidth=0.5, facecolor='none', edgecolor='black')
    location.plot(ax=ax, markersize=1, facecolor='black', edgecolor='black')

    # Add a colorbar
    cbar1 = plt.colorbar(im, ax=ax, shrink=0.5)
    cbar1.set_label('Drains (m)')

    # Set the title and axis labels
    ax.set_title('Period: {}'.format(period))
    ax.set_xlabel('X coordinate (m)')
    ax.set_ylabel('Y coordinate (m)')

    # Show the plot
    plt.show()
    
drain_values = drains_data[4]['q']

drains_vals = np.array(drain_values)
# Create an array of NaN values with the same shape as drain_values
nan_rows = np.empty((300, 1))
nan_rows[:] = np.nan

# Append the NaN rows to the end of the drain_values array
drain_values2 = np.concatenate([ nan_rows.flatten(), drains_vals])


            # sixze: 247683
rows = 393
cols = 631

drain_values_grid =drain_values2.reshape(cols, -1).T

# Plot the grid using imshow
fig, ax = plt.subplots(figsize=(10, 10))

# plot drains_data as image
im = ax.imshow(drain_values_grid,extent = grid_extent, cmap='Blues', vmin = -10, vmax = 0)
basinoutline.plot(ax=ax, facecolor='none', edgecolor='black')
glacier.plot(ax=ax, facecolor='none', edgecolor='black')
rivshp.plot(ax=ax,  linewidth=0.5, facecolor='none', edgecolor='black') 
location.plot(ax=ax, markersize=1, facecolor='black', edgecolor='black')

cbar1 = plt.colorbar(im, ax=ax, shrink=0.5)
cbar1.set_label('Drains (m)')
#ax.set_title('Time: {}'.format(round(times[tstep])))
ax.set_xticklabels([])
ax.set_yticklabels([])

    # subplot 2
    
    
    
# plot basinoutline, glacier, location, and rivshp as lines on the same axis
basinoutline.plot(ax=ax, facecolor='none', edgecolor='black')
glacier.plot(ax=ax, facecolor='none', edgecolor='black')
location.plot(ax=ax, markersize=2, facecolor='black', edgecolor='black')
rivshp.plot(ax=ax, linewidth=0.5, facecolor='none', edgecolor='black')

# add a colorbar
cbar = fig.colorbar(im, ax=ax, shrink=0.5)

# set axis labels and title
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_title('Drain Values')

# show the plot
plt.show()



    # Loop through all the time steps and stress periods in the drains data
    for ts in range(drains_data.shape[0]):
        for sp in range(drains_data.shape[1]):
            # Access the drain values at the current time step and stress period
            drain_values = drains_data[0]['q']
            plt.plot(drain_values)
            
            drain_values = drains_data[10]['q']
            plt.plot(drain_values)
                        

            
            # how do i get row and colum of each drain value location?
            
            # Process the drain values as needed
            # You can access the data using numpy indexing and slicing
            # For example, you can calculate statistics, plot the data, etc.

            # Example: Print the drain values at the current time step and stress period
            print("Time step:", ts)
            print("Stress period:", sp)
            print("Drain values:", drain_values)

