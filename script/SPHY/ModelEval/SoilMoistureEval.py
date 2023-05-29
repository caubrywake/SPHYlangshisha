# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 10:05:25 2023

@author: carol
"""
## Soil moisture comparison

import os
os.chdir ('C:\\SPHY3\\script\SPHY\\ModelEval')
#import hydrostats as hs
import importSPHYtss as imp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import hydroeval as he

figdir = ("C:/SPHY3/analysis/model_output/fig/modeleval/") # directory to save figure

# Load modelled soil moisture C:\SPHY3\sphy_20230218\
mod  = imp.importtss("2014", "01", "01", "C:\\SPHY3\\sphy_20230218\\output_sphy_config_base16_5\RootwDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'GW1 soil'])

# Keep only the outlet streamflow
mod = mod[['GW 3', 'AWS']]
mod = mod.iloc[2:]
# scaled from 0-1 for seelcted column
col = 'AWS'
#mod['AWS'] = mod['AWS'].clip(lower=55)
mod['scaled AWS']= (mod[col]-min(mod[col])) / (max(mod[col]) - min(mod[col]))
mod['scaled AWS']= (mod[col]-min(mod[col])) / (max(mod[col]) - min(mod[col]))

plt.plot(mod['AWS'])

# scaled from 0-1 for seelcted column
col = 'GW 3'
mod['scaled GW 3']= (mod[col]-min(mod[col])) / (max(mod[col]) - min(mod[col]))



#%%  Import measured soil moisture Langshihsa pluvio  2017-2018
fn = "D:\\UU\\field_data\\03_data\\data\\SoilMoisture\\201804_LangshishaPluvio_soilmoisture.csv"

# Read in the data
meas= pd.read_csv(fn)
# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['Date'] + ' ' + meas['Time'])

# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)

# Resample the data to daily frequency and calculate the mean
meas = meas.resample('D').mean()

# remove values above/below threshold
min_val = -0.1
max_val = 0.28
meas = meas.where((meas > min_val) & (meas < max_val), np.nan)

# calculate the average of the 3
meas['avg'] = meas[['SM1', 'SM2', 'SM3']].mean(axis=1)

# Normalize values
#meas['scaled']= (meas['avg']- min(meas['avg'])) / (max(meas['avg']) - min(meas['avg']))
meas['scaled']= (meas['avg']- min(meas['avg'])) / (0.18 - min(meas['avg']))

#%% Plot measured soil moisture

# Label and variable names
figtitle = 'SoilMoisture Probes @ LS AWS'
savetitle = 'SoilMoistureMeasurements_LS_AWS'
fig, axs = plt.subplots(figsize=(4,3))
# Sil moistur sensors
plt.plot(meas.index, meas['SM1'], label = 'SM1', color  ='black')
plt.plot(meas.index, meas['SM2'], label = 'SM2', color  ='red')
plt.plot(meas.index, meas['SM3'], label = 'SM3', color  ='blue')


# Graph settings
plt.xlabel('Year')
plt.ylabel('Soil Moisture')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

plt.show()


#%%  Plot 

# Label and variable names
modname = 'scaled AWS'
measname = 'scaled'
label1 = 'Modelled, AWS'
label2 = 'Measured, average'
yaxislab = 'soil moisture'
figtitle = 'SoilMoisture @ LS AWS'
savetitle = 'SoilMoisture_LS_AWS'

# Full period
plt.plot(mod.index, mod[modname], label = label1, color  ='red')
plt.plot(meas.index, meas[measname], label = label2, color  ='black')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Normalized Soil Moisture')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

plt.show()

#%% Subset period plot
fig, axs = plt.subplots(figsize=(3, 2))

start_date = '2017-08-01'
end_date = '2021-01-01'
savetitle = 'SoilMoisture_AWS_short_2017_2021'
figtitle = 'Streamflow @ LS, 2017-2021'
meas1_period = meas.loc[start_date:end_date]
mod_period = mod.loc[start_date:end_date]
plt.plot(mod_period.index, mod_period[modname], label = label1, color  ='red')
plt.plot(meas1_period.index, meas1_period[measname], label = label2, color  ='black')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Normalized Soil Moisture')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)
plt.savefig(figdir + savetitle + '.pdf', dpi = 300)
#%% #%%% Modemeval
start_date = '2020-01-01'
end_date = '2020-12-31'

mask = (mod.index >= start_date) & (mod.index <= end_date)
mod_cut= mod.loc[mask]
mod_cut = mod_cut [['scaled AWS']]

mask = (meas.index >= start_date) & (meas.index <= end_date)
meas_cut= meas.loc[mask]
meas_cut = meas_cut[['scaled']]
# convert columns to numpy arrays
mod_array = np.array(mod_cut['scaled AWS'], dtype=float)
meas_array = np.array(meas_cut['scaled'], dtype=float)


nse = he.evaluator(he.nse, mod_array, meas_array)
kge, r, alpha1, beta1 = he.evaluator(he.kge, mod_array, meas_array)
rmse = he.rmse(mod_array, meas_array)
mare=he.mare(mod_array, meas_array)
pbias=he.pbias(mod_array, meas_array)
print(nse)
print (kge)
print (rmse)
print (mare)
print(pbias)
#%% Export values
results = pd.DataFrame({'Metric': ['start date', 'end date', 'NSE', 'KGE', 'RMSE', 'MARE', 'PBIAS'], 'Value': [start_date, end_date, nse, kge, rmse, mare, pbias]})

# save the DataFrame to a CSV file
results.to_csv(figdir + 'SoilMoistureMetrics_'+ start_date + '_' + end_date+'.csv', index=False)

# print the DataFrame
print(results)