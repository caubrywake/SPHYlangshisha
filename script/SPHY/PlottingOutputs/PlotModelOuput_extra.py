# -*- coding: utf-8 -*-
"""
lotting recharge time series vs seepages
Created on Wed Apr  5 16:35:07 2023

@author: carol
"""


import os
os.chdir ('C:\\SPHY3\\script\SPHY\\ModelEval')
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

path = "C:\\SPHY3\\sphy_20230218\\output_20230405"
dd = '01'
mm = '01'
yy = '2014'
# Import modelled streamflow
mod  = imp.importtss(yy, mm, dd, path+ "\\SubpDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
# Keep only the outlet streamflow
qall = mod[['Outlet']]

## Import modelled Glacier flow
mod  = imp.importtss(yy, mm, dd, path+"\\GwreDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
# Keep only the outlet streamflow
gwre = mod[['Outlet']]

# glacier percolation
fn = path+"\GlacPerc.csv"
# Read in th data
GlacP= pd.read_csv(fn)
# Combine the date and time columns into a single datetime column
GlacP['datetime'] = pd.to_datetime(GlacP['Unnamed: 0'])

# Set the index of the DataFrame to the datetime column
GlacP.set_index('datetime', inplace=True)

# Full period
min_val = 0
max_val =200
qall = qall.where((qall > min_val) & (qall < max_val), np.nan)
gwre = gwre.where((gwre > min_val) & (gwre < max_val), np.nan)
gwre = gwre.resample('M').mean()
qall = gwre.resample('M').mean()



# subplot 1#
#plt.plot(date_array, rch_well['hd1_well1']*400)
plt.plot(qall.index, qall['Outlet'], label = 'subperc', color  ='red')
plt.plot(gwre.index, gwre['Outlet'], label = 'gw rech', color  ='blue')
plt.plot(GlacP.index, GlacP['2'], label = 'glacperc', color  ='magenta')


# Convert start and end dates to datetime objects
startdate = '2017-04-01'
enddate='2019-02-01'
start_date = dt.datetime.strptime(startdate, '%Y-%m-%d')
end_date = dt.datetime.strptime(enddate,  '%Y-%m-%d')
plt.xlim (start_date, end_date)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()

# Graph settings
plt.xlabel('Year')
plt.ylabel(measname)
plt.title(figtitle)



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
startdate = '2017-04-01'
enddate='2018-02-01'
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
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
plt.savefig(f"{figdir}{savetitle}{timestamp}.png", dpi = 300)

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

# Create a pandas DataFrame to hold the ratios

# Create a dictionary with the ratios
data = {"glacier_ratio": glac_ratio, "rain_ratio": rain_ratio, "snow_ratio": snow_ratio, "base_ratio": base_ratio}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)
print(df)
# Export the DataFrame as a .csv file
df.to_csv(figdir + 'StreamflowComponentRatios_'+ startdate + '_' + enddate+'.csv', index=False)
