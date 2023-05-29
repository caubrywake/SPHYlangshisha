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

import glob
import datetime

#%% Set paths
modelname = "mod6_02.nam"
cbcname = 'mod6_02'
modelpath  = "D:\\UU\\modflow\\20230420\\"
fig_dir  ='D:\\UU\\figure\\modflow_recharge\\20230420\\'


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
 
path = "D:\\UU\\modflow\\result\\riv_shp_point.shp"
rivshp = gpd.read_file(path)  
rivshp['id'] = range(1, len(rivshp)+1)  
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
    
# Extract the heads -- if just one file!
cbc = flopy.utils.CellBudgetFile(modelpath + cbcname + '.cbc')   
# Get the list of records in the model.cbc file
records = cbc.list_records()
river_leakage = cbc.get_data(text='RIVER LEAKAGE')
# Read the recharge data from the model.cbc file
leakage_data = cbc.get_data(text='LEAKAGE')

#%% create a time array

times = cbc.get_times()
    
start_date = datetime.datetime(2013, 12, 31)
date_times = []
for time in times:
        delta_days = int(time)
        delta_seconds = int((time - delta_days) * 86400)
        delta = datetime.timedelta(days=delta_days, seconds=delta_seconds)
        date_time = start_date + delta
        rounded_date_time = date_time.replace(hour=0, minute=0, second=0, microsecond=0)
        date_times.append(rounded_date_time.strftime('%Y-%m-%d'))
tt = pd.DataFrame({'datetime': date_times})
    
print(date_times)   

tgoal = '2017-08-05'
tstep = tt[tt['datetime'] == tgoal].index[0]
leakage = cbc.get_data(totim=times[tstep])
rch = leakage_data[tstep]
df = pd.DataFrame.from_records(rch)
df = (df*1000)/400 # in mm per day
 # add id value
df['id'] = range(1, len(df)+1)
df1 = rivshp['id']
 # merge the two
rivshp_merged = rivshp.merge(df, on='id')
 # create a new dataframe with just these two values
newriv= rivshp[['id', 'geometry']].copy()
newriv = newriv.merge(df[['id', 'q']], on='id')
 # Create a new DataFrame with just 2 columns from the previous DataFrame
 # Append the 'q' values from the current iteration as a new column in the rivshp DataFrame
col_name = f'q_{tstep}'  # Create a unique column name for each iteration
rivshp[col_name] = newriv['q']    # Get the row and column index
 
fig, axs = plt.subplots(figsize=(4,3))
savetitle = 'RiverLeakage_mm'
newriv.plot(ax=axs, column='q', cmap='Blues', marker='o', markersize=20, legend=True, vmin = -0.15, vmax = 0.35)
basinoutline.plot(ax=axs, facecolor='none', edgecolor='black')
glacier.plot(ax=axs, facecolor='none', edgecolor='black')
location.plot(ax=axs, markersize=1, facecolor='black', edgecolor='black')


    # Set the x-axis and y-axis limits of the subplot to the extent of 'rivshp_merged'
axs.set_xlim(newriv.total_bounds[0]-500, newriv.total_bounds[2]+500)
axs.set_ylim(newriv.total_bounds[1]-500, newriv.total_bounds[3]+500)
axs.set_xticklabels([])
axs.set_yticklabels([])
    # Set subplot title
axs.set_title(f"Leakage ({tgoal})")
# Add colorbar outside of subplots
#cbar = plt.colorbar(axs.collections[0],shrink=0.5)
cbar.set_label('River Leakage (mm/d)')

        # figure name
plt.tight_layout()
plt.savefig(fig_dir + modelname + '_time_step_{}.png'.format(round(times[tstep])), dpi=300, bbox_inches='tight')
plt.savefig(fig_dir + modelname + '_time_step_{}.pdf'.format(round(times[tstep])), dpi=300, bbox_inches='tight')
plt.show()  



#%% Create a new figure with 2x2 subplots

id = [6,8, 10,12]

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8, 6))
fig.suptitle(f"{cbcname}")
newriv_list =[]
# Loop through the index values and plot recharge on each subplot
for i, idx in enumerate(id):
    # Get the date and recharge data for the current index
    date = date_array[idx]
    rch = leakage_data[idx]
    df = pd.DataFrame.from_records(rch)
    df = df*1000/(400) # in mm per day
    # add id value
    df['id'] = range(1, len(df)+1)
    df1 = rivshp['id']
    # merge the two
    rivshp_merged = rivshp.merge(df, on='id')
    # create a new dataframe with just these two values
    newriv= rivshp[['id', 'geometry']].copy()
    newriv = newriv.merge(df[['id', 'q']], on='id')
    # Create a new DataFrame with just 2 columns from the previous DataFrame
    # Append the 'q' values from the current iteration as a new column in the rivshp DataFrame
    col_name = f'q_{idx}'  # Create a unique column name for each iteration
    rivshp[col_name] = newriv['q']    # Get the row and column index
    
    
    row = i // 2
    col = i % 2

    # Create a new ax object for the current subplot
    ax = axs[row, col]

    # Plot the recharge on the corresponding subplot
    newriv.plot(ax=ax, column='q', cmap='Blues_r', marker='o', markersize=20, legend=True)
    basinoutline.plot(ax=ax, facecolor='none', edgecolor='black')
    glacier.plot(ax=ax, facecolor='none', edgecolor='black')
    location.plot(ax=ax, markersize=1, facecolor='black', edgecolor='black')

    # Set the x-axis and y-axis limits of the subplot to the extent of 'rivshp_merged'
    ax.set_xlim(newriv.total_bounds[0]-500, newriv.total_bounds[2]+500)
    ax.set_ylim(newriv.total_bounds[1]-500, newriv.total_bounds[3]+500)

    # Set subplot title
    axs[row, col].set_title(f"Leakage ({date.strftime('%Y-%m-%d')})")

    # Remove x and y tick labels
    axs[row, col].set_xticklabels([])
    axs[row, col].set_yticklabels([])
    
# Add colorbar outside of subplots
cbar = plt.colorbar(ax.collections[0], ax=axs.ravel().tolist(), shrink=0.5)
cbar.set_label('River Leakage (m3/d)')
    
# Show the plot
plt.savefig(fig_dir + cbcname + '_RiverLeakage.png', dpi=300, bbox_inches='tight')

plt.show()

#%% Plot a time series

rivloc = [100, 18, 253, 254]  # Define the locations of interest

# Create an empty dataframe to store the extracted values
df_extracted = pd.DataFrame(columns=['Time Step', 'Value1', 'Value2', 'Value3', 'Value4'])
raster_file_names = []
total_values = []

# Iterate through each row in the leakage_data dataframe
for idx in range(0, len(leakage_data)):  # Use len(leakage_data) to get the length of the dataframe
    rch = leakage_data[idx] # Filter rows with matching time_step
    df = pd.DataFrame.from_records(rch)
    riv_tosurface = df['q'].sum()
        # Append the raster file name and total value to the lists

    total_values.append(riv_tosurface) # montlhy sum to m3/s
    #df = df/(400) # in mm per day
    # Extract the values from the df dataframe using rivloc
    value1 = df.iloc[rivloc[0]]['q']
    value2 = df.iloc[rivloc[1]]['q']
    value3 = df.iloc[rivloc[2]]['q']
    value4 = df.iloc[rivloc[3]]['q']
    
    # Append the extracted values to the df_extracted dataframe
    df_extracted = df_extracted.append({'Time Step': idx,
                                        'outlet': value1,
                                        'gw1': value2,
                                        'glacier toe': value3,
                                        'waterfall': value4},
                                       ignore_index=True)

# Print the extracted values in the df_extracted dataframe
fig, axs = plt.subplots(figsize=(13, 7), 
                                gridspec_kw={'wspace': 0.5, 'hspace': 0.3})
fig.suptitle("")
        
        # set font sizes for tick labels and titles
tick_font_size = 8
title_font_size = 10
    
    # subplot 1
plt.plot(date_array, total_values)


# Create a dataframe from the lists
df = pd.DataFrame({'timestep': date_array, 'Total_Value': total_values})
df.to_csv(fig_dir+'/MODFLOW_riverleakage_Basin.csv')



#%% plot result
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(13, 7), 
                                gridspec_kw={'wspace': 0.5, 'hspace': 0.3})
fig.suptitle("")
        
        # set font sizes for tick labels and titles
tick_font_size = 8
title_font_size = 10
    
    # subplot 1
axs[0, 0].plot(date_array, df_extracted['outlet'])
axs[0, 0].set_title('outlet', fontsize=title_font_size)
axs[0, 0].tick_params(labelsize=tick_font_size, rotation=30)

    # subplot 5 
axs[1, 0].plot(date_array, df_extracted['gw1'])
axs[1, 0].set_title('gw1', fontsize=title_font_size)
axs[1, 0].tick_params(labelsize=tick_font_size, rotation=30)
    
    # subplot 2
axs[0, 1].plot(date_array, df_extracted['glacier toe'])
axs[0, 1].set_title('glacier toe', fontsize=title_font_size)
axs[0, 1].tick_params(labelsize=tick_font_size, rotation=30)
    
    # subplot 6
axs[1, 1].plot(date_array, df_extracted['waterfall'])
axs[1, 1].set_title('waterfall', fontsize=title_font_size)
axs[1, 1].tick_params(labelsize=tick_font_size, rotation=30)
    
plt.savefig(fig_dir + cbcname + '_RiverLeakage_TS.png', dpi=300, bbox_inches='tight')
   
