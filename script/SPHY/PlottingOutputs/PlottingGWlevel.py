# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 16:16:18 2023

@author: carol

plotting GW level
"""



# plotmodelled gw recharge vs percolation?
# First, look into the location i already have time series for
# make a time series at 4 locations:
    
# gwrecharge (Gwre) vs subzone percolation vs glacier pecolation (Subp + GlacP)
# (C:\SPHY3\sphy_20230218\output_sphy_config_base14\GwreM001 ) vs (C:\SPHY3\sphy_20230218\output_sphy_config_base14\SubpM003) + (C:\SPHY3\sphy_20230218\output_sphy_config_base14\GlacpM000)

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

figdir = ("C:/SPHY3/analysis/model_output/fig/recharge/v3/") # directory to save figure
plt.close('all')

path = 'C:/SPHY3/sphy_20230218/output_sphy_config_base14/'
dd = '01'
mm = '01'
yy = '2014'



#%%
# Import gw recharge
mod  = imp.importtss(yy, mm, dd, path+ "/GwlDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
min_val = -6
max_val =-4.99
gwl = mod.where((mod > min_val) & (mod < max_val), np.nan)

## Import subzone percolation
mod  = imp.importtss(yy, mm, dd, path+"/SubpDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
min_val = -6
max_val =-4.99
gwl = mod.where((mod > min_val) & (mod < max_val), np.nan)
subp = mod.where((mod > min_val) & (mod < max_val), np.nan)

## Import modelled baseflow
mod  = imp.importtss(yy, mm, dd, path+"/BaserDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
baser = mod.where((mod > min_val) & (mod < max_val), np.nan)

## Import rootzone percolation
mod  = imp.importtss(yy, mm, dd, path+"/RootpDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
rootp = mod.where((mod > min_val) & (mod < max_val), np.nan)

## Import infiltration
mod  = imp.importtss(yy, mm, dd, path+"/InfilDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
infil = mod.where((mod > min_val) & (mod < max_val), np.nan)

# import ET and Preci[
mod  = imp.importtss(yy, mm, dd, path+ "/ETaFDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
etac = mod.where((mod > min_val) & (mod < max_val), np.nan)

mod  = imp.importtss(yy, mm, dd, path+ "/PrecFDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
precip = mod.where((mod > min_val) & (mod < max_val), np.nan)

# GlacP glacier id 2  (Langshihsa glacier)
## Import Glac percolation .csv
path = "C:/SPHY3/sphy_20230218/output_sphy_config_base14/"
fn = path+"GlacPerc.csv"

# Read in th data
GlacP= pd.read_csv(fn)
# Combine the date and time columns into a single datetime column
GlacP['datetime'] = pd.to_datetime(GlacP['Unnamed: 0'])

# Set the index of the DataFrame to the datetime column
GlacP.set_index('datetime', inplace=True)
glacp = GlacP.resample('D').mean()

#%% Plot timeseries

# Create a figure with two subplots, for AWS and gw1
savetitle = "RechargeSPHY_TS_2017_2018"
fig, axes = plt.subplots(2, 1, figsize=(8,8))


startdate = '2017-05-15'
enddate = '2017-11-01'
start_date = dt.datetime.strptime(startdate, '%Y-%m-%d')
end_date = dt.datetime.strptime(enddate, '%Y-%m-%d')
# Plot for the first subplot: all
axes[0].plot(gwl.index, gwl['AWS'], label='GW level', color = (0/255, 102/255, 0), linewidth=2)
axes[0].plot(gwl.index, gwl['GW 3'], label='Rootzone Percolation',color = (124/255, 87/255,0) , linewidth=2) 
axes[0].plot(gwl.index, gwl['GW 1'], label='Rootzone Percolation',color = (124/255, 87/255,0) , linewidth=2) 

axes[0].plot(subp.index, subp['AWS'], label='Subzone Percolation', color='black', linewidth=2)
axes[0].plot(gwre.index, gwre['AWS'], label='GW recharge', color='red', linewidth=2)
axes[0].plot(glacp.index, glacp['2'], label='Glacier Percolation', color=(130/255, 130/255, 130/255), linewidth=2)

#axes[0].plot(precip.index, precip['AWS'], label='Precipitation', color='black', linewidth=2)

axes[0].set_xlim(start_date, end_date)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('SPHY Fluxes (mm/day)')
#axes[0].set_title('Groundwater fluxes, AWS')
axes[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
axes[0].tick_params(rotation=30)
#axes[0].grid(which='major')
axes[0].set_ylim(ymin=0, ymax=25)

# Plot for the second subplot: infil, percolation
# Plot for the third subplot: percolation, baseflow
startdate = '2017-06-01'
enddate = '2019-12-31'
start_date = dt.datetime.strptime(startdate, '%Y-%m-%d')
end_date = dt.datetime.strptime(enddate, '%Y-%m-%d')
#axes[1].plot(infil.index, infil['AWS'], label='Infiltration', color = (0/255, 102/255, 0), linewidth=2)
#axes[1].bar(precip.index, precip['AWS'],label='Precipitation', color=( 102/255,178/255, 255/255), linewidth=2) 
#axes[1].plot(rootp.index, rootp['AWS'], label='Rootzone Percolation',color = (124/255, 87/255,0) , linewidth=2) 
axes[1].plot(subp.index, subp['AWS'], label='Subzone Percolation', color='black', linewidth=2)
axes[1].plot(gwre.index, gwre['AWS'], label='GW recharge', color='red', linewidth=2)
#axes[1].plot(glacp.index, glacp['2'], label='Glacier Percolation', color=(160/255, 160/255, 160/255), linewidth=2)

axes[1].set_xlim(start_date, end_date)
axes[1].set_xlabel('Year')
axes[1].set_ylabel('SPHY Fluxes (mm/day)')
#axes[1].set_title('Groundwater fluxes, GW 1')
axes[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
axes[1].tick_params(rotation=30)
#axes[1].grid(which='major')
axes[1].set_ylim(ymin=0, ymax=2)

# Adjust layout and show the plot
plt.tight_layout()
plt.savefig(f"{figdir}{savetitle}.png", dpi = 300)
plt.savefig(f"{figdir}{savetitle}.pdf", dpi = 300)
plt.show()