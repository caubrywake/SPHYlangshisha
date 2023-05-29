# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 17:44:51 2023

@author: carol
"""

# -*- coding: utf-8 -*-
"""
# output form walter
"""

# Plotting streamflow component
#import hydrostats as hs
import importSPHYtss as imp
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

figdir = ("C:/SPHY3/analysis/model_output/fig/walter/") # directory to save figure
plt.close('all')

path = 'C:\\SPHY3\\output\\20230314'
var = ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS']

# Import modelled streamflow
mod  = imp.importtss("2017", "01", "01", path + "\\QAllDTS.tss",  var)
# Keep only the outlet streamflow
qall = mod[['Outlet']]

## Import modelled Glacier flow
mod  = imp.importtss("2017", "01", "01", path + "\\GTotDTS.tss",  var)
# Keep only the outlet streamflow
glac = mod[['Outlet']]

## Import modelled Glacier flow
mod  = imp.importtss("2017", "01", "01", path + "\\RTotDTS.tss",  var)
# Keep only the outlet streamflow
rain = mod[['Outlet']]

## Import modelled Glacier flow
mod  = imp.importtss("2017", "01", "01", path + "\\STotDTS.tss",  var)
# Keep only the outlet streamflow
snow = mod[['Outlet']]

## Import modelled Glacier flow
mod  = imp.importtss("2017", "01", "01", path + "\\BTotDTS.tss",  var)
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
label1 = 'Qall'  # lable on figure
label2 = 'Glacier'
label3 = 'Rain'  # lable on figure
label4 = 'Snow'
label5 = 'Baseflow'
figtitle = 'Streamflow Component @ LS'
savetitle = 'ModelledFlowComponent' # name of saved file


# Full period
plt.plot(mod.index, qall[modname], label = label1, color  ='red')
plt.plot(mod.index, glac[modname], label = label2, color  ='blue')
plt.plot(mod.index, rain[modname], label = label3, color  ='magenta')
plt.plot(mod.index, snow[modname], label = label4, color  ='cyan')
plt.plot(mod.index, base[modname], label = label5, color  ='orange')
plt.plot(meas.index, meas[measname], label = 'Measured', color  ='black')

# Convert start and end dates to datetime objects
start_date = dt.datetime.strptime('2017-04-01', '%Y-%m-%d')
end_date = dt.datetime.strptime('2018-02-01', '%Y-%m-%d')
plt.xlim (start_date, end_date)

# Graph settings
plt.xlabel('Year')
plt.ylabel(measname)
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)

plt.show()
