# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 17:59:56 2023

@author: carol

"""
import os
os.chdir ('C:/SPHY3/script/SPHY/ModelEval')
# Plotting streamflow component
#import hydrostats as hs
import importSPHYtss as imp
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
from datetime import datetime
import hydroeval as he

figdir = ("C:/SPHY3/analysis/model_output/fig/") # directory to save figure
plt.close('all')

path = "C:/SPHY3/sphy_20230218/output_sphy_config_base16_5/"
dd = '01'
mm = '01'
yy = '2014'

min_val = 0
max_val =1500

#%%
# Import modelled streamflow
mod  = imp.importtss(yy, mm, dd, path+ "QAllDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
#mod = mod.resample('M').mean()
# Keep only the outlet streamflow
qall = mod[['Outlet']]

## Import modelled Glacier flow
mod  = imp.importtss(yy, mm, dd, path+"/GTotDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
#mod = mod.resample('M').mean()
# Keep only the outlet streamflow
glac = mod[['Outlet']]

## Import modelled Glacier flow
mod  = imp.importtss(yy, mm, dd, path+"/RTotDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
#mod = mod.resample('M').mean()
# Keep only the outlet streamflow
rain = mod[['Outlet']]

## Import modelled Glacier flow
mod  = imp.importtss(yy, mm, dd, path+"/STotDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
#mod = mod.resample('M').mean()
# Keep only the outlet streamflow
snow = mod[['Outlet']]

## Import modelled Glacier flow
mod  = imp.importtss(yy, mm, dd, path+"/BTotDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
#mod = mod.resample('M').mean()
# Keep only the outlet streamflow
base = mod[['Outlet']]

#%% Measured streamflow
fn = "D:\\UU\\field_data\\03_data\\data\\Discharge\\Langshisha\\Langshisha_Q_20172018.csv"

# Read in the data
meas= pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['DATE'] + ' ' + meas['TIME'])

# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)

# Rename column 
meas = meas.rename(columns={'Q [m3/s]': 'Q'})

# Resample the data to daily frequency and calculate the mean - give another name
meas = meas.resample('D').mean()


# remove values above/below threshold
min_val = 0
max_val =15
meas = meas.where((meas > min_val) & (meas < max_val), np.nan)

#%% Plot all tohtehr

# Label and variable names
modname = 'Outlet' # name of modelled variable column
measname = 'Q'
label1 = 'Total Streamflow'  # lable on figure
label2 = 'Glacier'
label3 = 'Rain'  # lable on figure
label4 = 'Snow'
label5 = 'Baseflow'
figtitle = 'Streamflow Component @ LS'
savetitle = 'ModelledFlowComponent' # name of saved file

fig, axes = plt.subplots(1, 1, figsize=(6,3))
# Full period
plt.plot(mod.index, qall[modname], label = label1, color  ='black')
plt.plot(mod.index, glac[modname], label = label2, color  =(51/255, 151/255, 255/255))
plt.plot(mod.index, rain[modname], label = label3, color=( 0/255,0/255, 102/255))
plt.plot(mod.index, snow[modname], label = label4, color  =(130/255, 130/255, 130/255))
plt.plot(mod.index, base[modname], label = label5, color  ='red')
#plt.plot(mod.index, base[modname]+glac[modname]+rain[modname]+snow[modname], label = 'sum' , color  ='red')

# Convert start and end dates to datetime objects
startdate = '2014-04-01'
enddate='2020-12-31'
start_date = dt.datetime.strptime(startdate, '%Y-%m-%d')
end_date = dt.datetime.strptime(enddate,  '%Y-%m-%d')
plt.xlim (start_date, end_date)

# Graph settings
plt.xlabel('Year')
plt.ylabel(measname)
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
# Get the current date and time

plt.savefig(f"{figdir}{savetitle}.png", dpi = 300)
plt.savefig(f"{figdir}{savetitle}.pdf", dpi = 300)
plt.show()

# Calculate the ratios of each time series to the tota
# Calculate the sum of the entire time series for each variable
glac_sum = np.sum(glac)
rain_sum = np.sum(rain)
snow_sum = np.sum(snow)
base_sum = np.sum(base)

# Calculate the total sum of all time series
total_sum = glac_sum + rain_sum + snow_sum + base_sum

# Calculate the ratios for each variable
glac_ratio = glac_sum / total_sum
rain_ratio = rain_sum / total_sum
snow_ratio = snow_sum / total_sum
base_ratio = base_sum / total_sum

print(f"Glacier ratio: {glac_ratio.iloc[0]:.2f}")
print(f"Rain ratio: {rain_ratio.iloc[0]:.2f}")
print(f"Snow ratio: {snow_ratio.iloc[0]:.2f}")
print(f"Base ratio: {base_ratio.iloc[0]:.2f}")

## Plor for just one year

# Label and variable names
modname = 'Outlet' # name of modelled variable column
measname = 'Q'
label1 = 'Total Streamflow'  # lable on figure
label2 = 'Glacier'
label3 = 'Rain'  # lable on figure
label4 = 'Snow'
label5 = 'Baseflow'
figtitle = 'Streamflow Component @ LS'
savetitle = 'ModelledFlowComponent_2017' # name of saved file

fig, axes = plt.subplots(1, 1, figsize=(3,3))
# Full period
plt.plot(mod.index, qall[modname], label = label1, color  ='black')
plt.plot(mod.index, glac[modname], label = label2, color  =(51/255, 151/255, 255/255))
plt.plot(mod.index, rain[modname], label = label3, color=( 0/255,0/255, 102/255))
plt.plot(mod.index, snow[modname], label = label4, color  =(130/255, 130/255, 130/255))
plt.plot(mod.index, base[modname], label = label5, color  ='red')
#plt.plot(mod.index, base[modname]+glac[modname]+rain[modname]+snow[modname], label = 'sum' , color  ='red')

# Convert start and end dates to datetime objects
startdate = '2017-05-01'
enddate='2017-11-30'
start_date = dt.datetime.strptime(startdate, '%Y-%m-%d')
end_date = dt.datetime.strptime(enddate,  '%Y-%m-%d')
plt.xlim (start_date, end_date)
plt.ylim(0, 10)

# Graph settings
plt.xlabel('Year')
plt.ylabel(measname)
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
# Get the current date and time

plt.savefig(f"{figdir}{savetitle}.png", dpi = 300)
plt.savefig(f"{figdir}{savetitle}.pdf", dpi = 300)
plt.show()
# Create a pandas DataFrame to hold the ratios

# Create a dictionary with the ratios
data = {"glacier_ratio": glac_ratio, "rain_ratio": rain_ratio, "snow_ratio": snow_ratio, "base_ratio": base_ratio}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)
print(df)
# Export the DataFrame as a .csv file
df.to_csv(figdir + 'StreamflowComponentRatios_'+ startdate + '_' + enddate+'.csv', index=False)
