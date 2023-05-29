# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:26:58 2023

@author: carol
"""

# Create temperature time series
## 
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
import rasterio as rs
import numpy as np
import statistics
import os

## Mean temperature
#%% Import temperature series
figdir = ("C:/SPHY3/analysis/model_output/fig/dataplot/") # directory to save figure

# Import temperature time serie
fn = "D:\\UU\\field_data\\03_data\\data\\Pluvio\\20211206_Pluvio_Langshisha.csv"

# Read in the data
meas = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['Date'] + ' ' + meas['Time'])

# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)

# Keep only Temp old and temp new
meas = meas.iloc[:, [5,6]]
meas = meas.resample('D').mean()


#%% Plot both Old and New temp sensor

# Label and variable names
modname = 'Temp old'
measname = 'Temp new'
label1 = 'Old'
label2 = 'New'
figtitle = 'Temperature, Langshisha Pluvio'
savetitle = 'TempLs'

# Full period
plt.plot(meas.index, meas[modname], label = label1, color  ='black')
plt.plot(meas.index, meas[measname], label = label2, color  ='red')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Ta (C)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

# Keep temp old for analysis
meas = meas[['Temp old']] # as it is more stable and complete

#%% Infill gaps form ERA observations
fn = 'G:\\14_TU\\Data_Langtang_raw\\ERA5_Temp_1981_2020.csv'
# Read in the data
era = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
era['datetime'] = pd.to_datetime(era['datetime'] )

# Set the index of the DataFrame to the datetime column
era.set_index('datetime', inplace=True)
era = era['temp']-273.15;

# Make sure both time series have the same time index
common_index = meas.index.intersection(era.index)
meas_cut = meas.loc[common_index]
era_cut = era.loc[common_index]

# Merge the dataframe
merged_df = pd.merge(meas_cut, era_cut, on='datetime', how='outer')
merged_df = merged_df.rename (columns={'Temp old':'ls'})
merged_df['date'] = merged_df.index
merged_df['numerical_index'] =merged_df.reset_index().index

# make a duplicate of the DataFrame
df_nonan = merged_df.copy()
df_nonan.dropna(inplace=True)

# %% calculate linear regression coefficients and plot
slope, intercept, r_value, p_value, std_err = linregress(df_nonan['temp'],df_nonan['ls'])

# predict missing values using linear regression
meas_cut['ls_pred'] = intercept + slope * era_cut

meas_cut['combined']=meas_cut['Temp old']

# fill missing values with predicted values
df = meas_cut;
df.loc[df['Temp old'].isna(), 'Temp old'] = df.loc[df['combined'].isna(), 'ls_pred']

# make a duplicate of the DataFrame
meas_cut= df.copy()

#%% plot ERA and Lansghisha Old
# Label and variable names
modname = 'ls'
measname = 'temp'
label1 = 'LS'
label2 = 'ERA'
figtitle = 'Daily Mean Temperature @ Ls Pluvio and ERA'
savetitle = 'MeanTemp_Langshisha_ERA'

# Full period

fig, ax = plt.subplots()

ax.plot(merged_df.index, merged_df[modname], label = label1, color  ='black')
ax.plot(merged_df.index, merged_df[measname], label = label2, color  ='red')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Daily Mean Ta (C)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

plt.show()

#%% plot Filled in LS, ERA and LS Old

# Label and variable names
modname = 'ls'
measname = 'temp'
label1 = 'LS'
label2 = 'ERA'
figtitle = 'Daily Mean Temperature @ LS Pluvio, filled with lin. regression ERA'
savetitle = 'MeanTemp_Langshisha_filledwithERA'

# Full period
fig, ax = plt.subplots()

ax.plot(era_cut.index, era_cut, label = 'ERA', color  ='blue')
ax.plot(meas_cut.index, meas_cut['Temp old'], label = 'Filled', color  ='red')
ax.plot(meas_cut.index, meas_cut['combined'], label = 'LS', color  ='black')

eq = f'LSfit = {slope:.2f}ERA + {intercept:.2f}\n r = {r_value:.2f}'
ax.text(0.95, 0.05, eq, ha='right', va='bottom', transform=ax.transAxes)
ax.text(0.95, 0.05, '', ha='right', va='bottom', transform=ax.transAxes)


# Graph settings
plt.xlabel('Year')
plt.ylabel('Daily Mean Ta (C)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

# export the dataframe to a csv file
LS = meas_cut['Temp old']
LS = LS.rename('LS_filled')

LS.to_csv('C:\\SPHY3\\analysis\\data_processed\\LSaws_Ta_filledwithERA_20132021.csv')
####################################################

########################################################
#%% Min temperature
# Import clean temperature time serie
fn = "D:\\UU\\field_data\\03_data\\data\\Pluvio\\20211206_Pluvio_Langshisha.csv"

# Read in the data
meas = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['Date'] + ' ' + meas['Time'])

# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)

# Keep only Temp old and temp new - 
meas = meas.iloc[:, [5,6]]
meas = meas.resample('D').min()

"""
meas = meas.resample('D').agg({'Temp old':['min', 'max', 'mean']})
meas = meas.resample('D').agg({'Temp new':['min', 'max', 'mean']})
"""

#%% plot both Old and New temp sensor

# Label and variable names
modname = 'Temp old'
measname = 'Temp new'
label1 = 'Old'
label2 = 'New'
figtitle = 'Minimum Daily Temperature, Langshisha Pluvio'
savetitle = 'TempLs_dailyMin'

# Full period
plt.plot(meas.index, meas[modname], label = label1, color  ='black')
plt.plot(meas.index, meas[measname], label = label2, color  ='red')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Daily Minum Temperature (C)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)


# Keep temp old for analysis
meas = meas[['Temp old']]

#%% Infill gaps form ERA observations
fn = 'G:\\14_TU\\Data_Langtang_raw\\ERA5_Temp_1981_2020.csv'
# Read in the data
era = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
era['datetime'] = pd.to_datetime(era['datetime'] )

# Set the index of the DataFrame to the datetime column
era.set_index('datetime', inplace=True)
era = era['temp']-273.15;
era = era.resample('D').min()

# Make sure both time series have the same time index
common_index = meas.index.intersection(era.index)
meas_cut = meas.loc[common_index]
era_cut = era.loc[common_index]

# Merge the dataframe
merged_df = pd.merge(meas_cut, era_cut, on='datetime', how='outer')
merged_df = merged_df.rename (columns={'Temp old':'ls'})
merged_df['date'] = merged_df.index
merged_df['numerical_index'] =merged_df.reset_index().index

# make a duplicate of the DataFrame
df_nonan = merged_df.copy()
df_nonan.dropna(inplace=True)

# %% calculate linear regression coefficients and plot
slope, intercept, r_value, p_value, std_err = linregress(df_nonan['temp'],df_nonan['ls'])

# predict missing values using linear regression
meas_cut['ls_pred'] = intercept + slope * era_cut

meas_cut['combined']=meas_cut['Temp old']

# fill missing values with predicted values
df = meas_cut;
df.loc[df['Temp old'].isna(), 'Temp old'] = df.loc[df['combined'].isna(), 'ls_pred']

# make a duplicate of the DataFrame
meas_cut= df.copy()

#%% plot ERA and Lansghisha Old
# Label and variable names
modname = 'ls'
measname = 'temp'
label1 = 'LS'
label2 = 'ERA'
figtitle = 'Daily Minimum Temperature @ Ls Pluvio and ERA'
savetitle = 'MinTemp_Langshisha_ERA'

# Full period

fig, ax = plt.subplots()

ax.plot(merged_df.index, merged_df[modname], label = label1, color  ='black')
ax.plot(merged_df.index, merged_df[measname], label = label2, color  ='red')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Daily Minimum temperature (C)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

plt.show()

#%% plot Filled in LS, ERA and LS Old

# Label and variable names
modname = 'ls'
measname = 'temp'
label1 = 'LS'
label2 = 'ERA'
figtitle = 'Daily Minimum Temperature @ LS Pluvio, filled with lin. regression ERA'
savetitle = 'MinTemp_Langshisha_filledwithERA'

# Full period
fig, ax = plt.subplots()

ax.plot(era_cut.index, era_cut, label = 'ERA', color  ='blue')
ax.plot(meas_cut.index, meas_cut['Temp old'], label = 'Filled', color  ='red')
ax.plot(meas_cut.index, meas_cut['combined'], label = 'LS', color  ='black')

eq = f'LSfit = {slope:.2f}ERA + {intercept:.2f}\n r = {r_value:.2f}'
ax.text(0.95, 0.05, eq, ha='right', va='bottom', transform=ax.transAxes)
ax.text(0.95, 0.05, '', ha='right', va='bottom', transform=ax.transAxes)


# Graph settings
plt.xlabel('Year')
plt.ylabel('Daily Minimum Temperature (C)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

# export the dataframe to a csv file
LS = meas_cut['Temp old']
LS = LS.rename('LS_filled')

LS.to_csv('C:\\SPHY3\\analysis\\data_processed\\LSaws_Ta_filledwithERA_20132021min.csv')

#######################################################################################
#%% MNaximum daily temperature

# Import clean temperature time serie
fn = "D:\\UU\\field_data\\03_data\\data\\Pluvio\\20211206_Pluvio_Langshisha.csv"

# Read in the data
meas = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['Date'] + ' ' + meas['Time'])

# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)

# Keep only Temp old and temp new - 
meas = meas.iloc[:, [5,6]]
meas = meas.resample('D').max()

"""
meas = meas.resample('D').agg({'Temp old':['min', 'max', 'mean']})
meas = meas.resample('D').agg({'Temp new':['min', 'max', 'mean']})
"""

#%% plot both Old and New temp sensor

# Label and variable names
modname = 'Temp old'
measname = 'Temp new'
label1 = 'Old'
label2 = 'New'
figtitle = 'Maximum Daily Temperature, Langshisha Pluvio'
savetitle = 'TempLs_dailyMax'

# Full period
plt.plot(meas.index, meas[modname], label = label1, color  ='black')
plt.plot(meas.index, meas[measname], label = label2, color  ='red')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Daaily Maximum temperature (C)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)


# Keep temp old for analysis
meas = meas[['Temp old']]

#%% Infill gaps form ERA observations
fn = 'G:\\14_TU\\Data_Langtang_raw\\ERA5_Temp_1981_2020.csv'
# Read in the data
era = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
era['datetime'] = pd.to_datetime(era['datetime'] )

# Set the index of the DataFrame to the datetime column
era.set_index('datetime', inplace=True)
era = era['temp']-273.15;
era = era.resample('D').max()

# Make sure both time series have the same time index
common_index = meas.index.intersection(era.index)
meas_cut = meas.loc[common_index]
era_cut = era.loc[common_index]

# Merge the dataframe
merged_df = pd.merge(meas_cut, era_cut, on='datetime', how='outer')
merged_df = merged_df.rename (columns={'Temp old':'ls'})
merged_df['date'] = merged_df.index
merged_df['numerical_index'] =merged_df.reset_index().index

# make a duplicate of the DataFrame
df_nonan = merged_df.copy()
df_nonan.dropna(inplace=True)

# %% calculate linear regression coefficients and plot
slope, intercept, r_value, p_value, std_err = linregress(df_nonan['temp'],df_nonan['ls'])

# predict missing values using linear regression
meas_cut['ls_pred'] = intercept + slope * era_cut

meas_cut['combined']=meas_cut['Temp old']

# fill missing values with predicted values
df = meas_cut;
df.loc[df['Temp old'].isna(), 'Temp old'] = df.loc[df['combined'].isna(), 'ls_pred']

# make a duplicate of the DataFrame
meas_cut= df.copy()

#%% plot ERA and Lansghisha Old
# Label and variable names
modname = 'ls'
measname = 'temp'
label1 = 'LS'
label2 = 'ERA'
figtitle = 'Daily Maximum Temperature @ Ls Pluvio and ERA'
savetitle = 'MaxTemp_Langshisha_ERA'

# Full period

fig, ax = plt.subplots()

ax.plot(merged_df.index, merged_df[modname], label = label1, color  ='black')
ax.plot(merged_df.index, merged_df[measname], label = label2, color  ='red')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Daily maximum temperature (C)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

plt.show()

#%% plot Filled in LS, ERA and LS Old

# Label and variable names
modname = 'ls'
measname = 'temp'
label1 = 'LS'
label2 = 'ERA'
figtitle = 'Daily Maximum Temperature @ LS Pluvio, filled with lin. regression ERA'
savetitle = 'MaxTemp_Langshisha_filledwithERA'

# Full period
fig, ax = plt.subplots()

ax.plot(era_cut.index, era_cut, label = 'ERA', color  ='blue')
ax.plot(meas_cut.index, meas_cut['Temp old'], label = 'Filled', color  ='red')
ax.plot(meas_cut.index, meas_cut['combined'], label = 'LS', color  ='black')

eq = f'LSfit = {slope:.2f}ERA + {intercept:.2f}\n r = {r_value:.2f}'
ax.text(0.95, 0.05, eq, ha='right', va='bottom', transform=ax.transAxes)
ax.text(0.95, 0.05, '', ha='right', va='bottom', transform=ax.transAxes)


# Graph settings
plt.xlabel('Year')
plt.ylabel('Daily maximum temperature (C)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

# export the dataframe to a csv file
LS = meas_cut['Temp old']
LS = LS.rename('LS_filled')

LS.to_csv('C:\\SPHY3\\analysis\\data_processed\\LSaws_Ta_filledwithERA_20132021max.csv')