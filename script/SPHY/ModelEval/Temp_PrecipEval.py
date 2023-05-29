# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 17:08:47 2023

@author: carol
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 13:46:37 2023

@author: carol
"""
import os
os.chdir("C:\\SPHY3\\script\\SPHY\\ModelEval") #

## Precipitation
import importSPHYtss as imp
import matplotlib.pyplot as plt
import pandas as pd

figdir = ("C:/SPHY3/analysis/model_output/fig/") # directory to save figure
plt.close('all')

#%% Model output
# Load modelled snowpack 
mod  = imp.importtss("2017", "01", "01", "C:\\SPHY3\\sphy_20230218\\output_20230324\\PrecFDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
plt.plot(mod.index, mod)
# Keep only the outlet streamflow
mod = mod[['AWS']]
#%%  Import rainfall
fn = "D:\\UU\\field_data\\03_data\\data\\TippingBuckets\\20211206_TB_LangshishaBC_10271177_data.csv"

# Read in the data
meas = pd.read_csv(fn)

# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['DATE'] + ' ' + meas['TIME'])

# Set the index of the DataFrame to the datetime column
meas.set_index('datetime', inplace=True)
meas['rain'] = 0.2
meas = meas [['rain']]

meas = meas.resample('D').sum()

#%%  Import rainfall2
# Import precipitation time series
fn = 'D:\\UU\\field_data\\processed\\Pdaily_Ls_infilledw_20120503_20210701.csv'

# Read in the data
meas2 = pd.read_csv(fn)
os.environ["PROJ_LIB"] = "C:\\Users\\carol\\miniconda3\\envs\\spyder-env\\Lib\\site-packages\\pyproj\\proj_dir\\share\\proj\\"

# Combine the date and time columns into a single datetime column
meas2['datetime'] = pd.to_datetime(meas2['Time'] )
# Set the index of the DataFrame to the datetime column
meas2.set_index('datetime', inplace=True)

plt.plot(meas2.index, meas2['Var1'], label = 'Rain', color  ='black') # seems pretty good

#%% Import the ERA5 precip


#%%  Plot 

# Label and variable names
modname = 'AWS'
measname = 'rain'
label1 = 'Modelled'
label2 = 'TB Langshisa'
figtitle = 'RainfallTB @ LS'
savetitle = 'Rainfall_LS'

# Full period
plt.plot(meas2.index, meas2['Var1'], label = 'Input Rain', color  ='blue') # seems pretty good
plt.plot(meas.index, meas[measname], label = label2, color  ='red')
plt.plot(mod.index, mod[modname], label = label1, color  ='black')


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
start_date = '2017-01-01'
end_date = '2018-10-01'
savetitle = 'RainfallTB_LS_short'

meas_period = meas.loc[start_date:end_date]
mod_period = mod.loc[start_date:end_date]
plt.plot(meas_period.index, meas_period[measname], label = label2, color  ='red')
plt.plot(mod_period.index, mod_period[modname], label = label1, color  ='black')

# Graph settings
plt.xlabel('Year')
plt.ylabel(measname)
plt.title(figtitle)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)
#%% Plot cumulative precip
df = mod
df_annual = df.resample('A').sum()
cumsum_df = pd.DataFrame()
for year in df_annual.index.year:
    year_df = df.loc[df.index.year == year]
    cumsum_df = pd.concat([cumsum_df, year_df.cumsum()])

df2 = meas
df2_annual = df2.resample('A').sum()
cumsum_df2 = pd.DataFrame()
for year in df2_annual.index.year:
    year_df2 = df2.loc[df2.index.year == year]
    cumsum_df2 = pd.concat([cumsum_df2, year_df2.cumsum()])

cumsum_df['AWS'].plot()
cumsum_df2['rain'].plot()
plt.legend()
plt.xlabel('Date')
plt.ylabel('Cumulative Sum AWS')
plt.title('Cumulative Sum of AWS for each year from Jan 1 to Dec 31')
plt.show()

#%% Rain vs Snow
# Load modelled snowpack 
rain  = imp.importtss("2017", "01", "01", "C:\\SPHY3\\sphy_20230218\\output_20230322\\RainDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
snow  = imp.importtss("2017", "01", "01", "C:\\SPHY3\\sphy_20230218\\output_20230322\\SnowDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])

plt.plot(rain.index, rain['AWS'], label = 'Rain', color  ='blue') # seems pretty good
plt.plot(snow.index, snow['AWS'], label = 'Snow', color  ='red')


