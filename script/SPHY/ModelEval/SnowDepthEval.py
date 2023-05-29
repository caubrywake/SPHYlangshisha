# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 13:46:37 2023

@author: carol
"""

## Snow cover cmomparison
import os
os.chdir ('C:\\SPHY3\\script\SPHY\\ModelEval')
import importSPHYtss as imp
import matplotlib.pyplot as plt
import pandas as pd



figdir = ("C:/SPHY3/analysis/model_output/fig/modeleval/") # directory to save figure
plt.close('all')

#%% Model output
# Load modelled snowpack 
mod  = imp.importtss("2014", "01", "01", "C:\\SPHY3\\sphy_20230218\\output_20230529\\SnowSDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])

# Keep only the outlet streamflow
mod = mod[['AWS']]
#%%  Import measured snow depth -  Langshihsa pluvio  2017-2018
fn = "D:\\UU\\field_data\\03_data\\data\\Pluvio\\20211206_Pluvio_Langshisha.csv"

# Read in the data
meas = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['Date'] + ' ' + meas['Time'])

# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)

# Resample the data to daily frequency and calculate the mean
meas = meas.resample('D').mean()

# select the snowdepth column
meas = meas[['SnowD']]

# Correct for sensor height
# assuming a density of 150 kg/m - fresh snow

meas = (-meas+2.65) # snow depth in m
meas = meas * 1000 * 0.50  # in mm w.e.


#%%  Plot 

# Label and variable names
modname = 'AWS'
measname = 'SnowD'
label1 = 'Modelled'
label2 = 'Measured'
figtitle = 'SnowDepth @ LS'
savetitle = 'SnowD_LS'

# Full period
plt.plot(mod.index, mod[modname], label = label1, color  ='black')
plt.plot(meas.index, meas[measname], label = label2, color  ='red')

# Graph settings
plt.xlabel('Year')
plt.ylabel(measname)
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

plt.show()

#%% Subset period plot
start_date = '2019-01-01'
end_date = '2020-11-01'
savetitle = 'SnowD_LS_short'

fig, axs = plt.subplots(figsize=(3, 2))
meas_period = meas.loc[start_date:end_date]
mod_period = mod.loc[start_date:end_date]
plt.plot(meas_period.index, meas_period[measname], label = 'Measured', color  ='black')
plt.plot(mod_period.index, mod_period[modname], label = 'Modelled', color  ='red')

# Graph settings

plt.xlabel('Year')
plt.ylabel(measname)
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)
plt.savefig(figdir + savetitle + '.pdf', dpi = 300)
#%%
