# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:20:52 2023

@author: carol
"""

# print the DataFrame
# Model evaluation

import os
os.chdir ('C:\\SPHY3\\script\SPHY\\ModelEval')
#import hydrostats as hs
import importSPHYtss as imp
import matplotlib.pyplot as plt
import pandas as pd
import hydroeval as he
import numpy as np

figdir = ("C:/SPHY3/analysis/model_output/fig/modeleval/") # directory to save figure
plt.close('all')

# Import modelled streamflow
mod  = imp.importtss("2014", "01", "01", "C:\\SPHY3\\sphy_20230218\\output_20230529\\QAllDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'GW1 soil'])

# Keep only the outlet streamflow
mod = mod[['Outlet']]
plt.plot(mod.index, mod)
#%% Import measured streamflow, - 2017-2018
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
meas1 = meas.resample('D').mean()

#%% Import measured streamflow, - 2013-2016
fn = "D:\\UU\\field_data\\03_data\\data\\Discharge\\Langshisha\\Langshisha_Q_20132016.csv"

# Read in the data
meas= pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['DATE'] + ' ' + meas['TIME'])

# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)

# Rename column 
meas = meas.rename(columns={'Q [m3/s]': 'Q'})

# Resample the data to daily frequency and calculate the mean - give another name
meas2 = meas.resample('W').mean()

#%% Plot all period

# Label and variable names
start_date = '2014-04-29'
end_date = '2018-07-05'
meas1_period = meas1.loc[start_date:end_date]
mod_period = mod.loc[start_date:end_date]
meas2_period = meas2.loc[start_date:end_date]

modname = 'Outlet' # name of modelled variable column
measname = 'Q' # name of measured variable column
label1 = 'Modelled'  # lable on figure
label2 = 'Measured'
figtitle = 'Streamflow @ LS'
savetitle = 'Q_LS_all' # name of saved file

fig, axs = plt.subplots(figsize=(5,3))

# Full period
plt.plot(mod_period.index, mod_period[modname], label = label1, color  ='black')
plt.plot(meas1_period.index, meas1_period[measname], label = 'Measured, outlet', color  ='red')
plt.plot(meas2_period.index, meas2_period[measname], label = 'Measured, upstream', color  ='blue')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Q (m3/s)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.ylim(0, 12) # set the y-axis limit to 12
plt.savefig(figdir + savetitle + '.png', dpi = 300)
plt.savefig(figdir + savetitle + '.pdf', dpi = 300)

plt.show()

#%% Subset period plot
start_date = '2017-04-29'
end_date = '2018-07-05'
savetitle = 'Q_LS_short_2017_2018'
figtitle = 'Streamflow @ LS, 2017-2018'
meas1_period = meas1.loc[start_date:end_date]
mod_period = mod.loc[start_date:end_date]
plt.plot(mod_period.index, mod_period[modname], label = label1, color  ='black')
plt.plot(meas1_period.index, meas1_period[measname], label = label2, color  ='red')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Q (m3/s)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.ylim(0, 12) # set the y-axis limit to 12
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

#%% Subset period plot
start_date = '2014-01-01'
end_date = '2016-07-06'
savetitle = 'Q_LS_short_2014_2016'
figtitle = 'Streamflow @ LS, 2014-2016'
meas1_period = meas2.loc[start_date:end_date]
mod_period = mod.loc[start_date:end_date]
plt.plot(mod_period.index, mod_period[modname], label = label1, color  ='black')
plt.plot(meas1_period.index, meas1_period[measname], label = label2, color  ='blue')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Q (m3/s)')
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)
#%% #%%% Modemeval
start_date = '2017-04-29'
end_date = '2017-12-31'

mask = (mod.index >= start_date) & (mod.index <= end_date)
mod_cut= mod.loc[mask]
mod_cut = mod_cut [['Outlet']]

mask = (meas1.index >= start_date) & (meas1.index <= end_date)
meas_cut= meas1.loc[mask]
meas_cut = meas_cut[['Q']]
# convert columns to numpy arrays
mod_array = np.array(mod_cut['Outlet'], dtype=float)
meas_array = np.array(meas_cut['Q'], dtype=float)

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
results.to_csv(figdir + 'StreamflowMetrics_'+ start_date + '_' + end_date+'.csv', index=False)

# print the DataFrame
print(results)

#%% #%%% Modemeval
mod_wk = mod.resample('W').mean()

start_date = '2014-01-01'
end_date = '2016-07-06'

mask = (mod_wk.index >= start_date) & (mod_wk.index <= end_date)
mod_cut= mod_wk.loc[mask]
mod_cut = mod_cut [['Outlet']]
mod_cut = mod_cut.iloc[1:]
mask = (meas2.index >= start_date) & (meas2.index <= end_date)
meas_cut= meas2.loc[mask]
meas_cut = meas_cut[['Q']]
meas_cut=meas_cut.iloc[1:]
# convert columns to numpy arrays
mod_array = np.array(mod_cut['Outlet'], dtype=float)
meas_array = np.array(meas_cut['Q'], dtype=float)

nse2 = he.evaluator(he.nse, mod_array, meas_array)
kge2, r2, alpha2, beta2 = he.evaluator(he.kge, mod_array, meas_array)
rmse2 = he.rmse(mod_array, meas_array)
mare2=he.mare(mod_array, meas_array)
pbias2=he.pbias(mod_array, meas_array)
print(nse2)
print (kge2)
print (rmse2)
print (mare2)
print(pbias2)

#%% Export values
results = pd.DataFrame({'Metric': ['start date', 'end date', 'NSE', 'KGE', 'RMSE', 'MARE', 'PBIAS'], 'Value': [start_date, end_date, nse2, kge2, rmse2, mare2, pbias2]})

# save the DataFrame to a CSV file
results.to_csv(figdir + 'StreamflowMetric_' + start_date + '_' + end_date+'.csv', index=False)

print(results)

df = pd.read_csv(figdir + 'StreamflowMetrics_'+ start_date + '_' + end_date+'.csv')
with open(figdir + 'StreamflowMetrics_' + start_date + '_' + end_date +'.md', 'w') as md:
  df.to_markdown(buf=md, tablefmt="grid")
  

df = pd.read_csv("C:/SPHY3/analysis/model_output/fig/modeleval/StreamflowMetrics_2017-04-29_2018-07-05.csv")
# Select the second and third columns
selected_cols = df.loc[:, ['Metric', 'Value']]

from IPython.display import Markdown
from tabulate import tabulate

# Convert dataframe to list of lists
table = selected_cols.values.tolist()
Markdown(tabulate(
  table, 
  headers=["Planet","R (km)", "mass (x 10^29 kg)"]
))