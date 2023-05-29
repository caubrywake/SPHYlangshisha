# -*- coding: utf-8 -*-
"""
Plortting well data
Created on Mon Apr 17 08:37:43 2023

@author: carol
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import well data
gwpath = 'D:/UU/field_data/03_data/data/Groundwater/'
# Load Langshisha Bottom Groundwater data
meas = pd.read_csv(gwpath +'202111_LangshishaBottom_Groundwater.csv')
# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['DATE'] + ' ' + meas['TIME'])
meas.set_index('datetime', inplace=True)
lsbot = meas;
lsbot['waterlevel']= lsbot['diff_pres']*1000./(999.965*9.81)-2.07
column_name = 'waterlevel'  # Replace with the actual column name
lsbot[column_name] = np.where(lsbot[column_name] < -1.7, np.nan, lsbot[column_name])

# Load Langshisha Mid Groundwater data
meas = pd.read_csv(gwpath +'202111_LangshishaMid_Groundwater.csv')
# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['DATE'] + ' ' + meas['TIME'])
meas.set_index('datetime', inplace=True)
lsmid = meas;
lsmid['waterlevel']= lsmid['diff_pres']*1000./(999.965*9.81)-1.62
lsmid[column_name] = np.where(lsmid[column_name] < -1.62, np.nan, lsmid[column_name])

# Load Langshisha Top Groundwater data
meas = pd.read_csv(gwpath +'202111_LangshishaTop_Groundwater.csv')
# Combine the date and time columns into a single datetime column
meas['datetime'] = pd.to_datetime(meas['DATE'] + ' ' + meas['TIME'])
meas.set_index('datetime', inplace=True)
lstop = meas;
lstop['waterlevel']= lstop['diff_pres']*1000./(999.965*9.81)-1.38
lstop[column_name] = np.where(lstop[column_name] < -1.38, np.nan, lstop[column_name])
#%% Plot output
figdir = 'D:/UU/figure/00_dataexploration/well/'
savetitle = 'Well_LS'
# Plot Langshisha Bottom data
plt.plot(lstop['waterlevel'], label='Langhisha Top', color= 'red')
plt.plot(lsmid['waterlevel'], label='Langhisha Mid', color= (160/255, 160/255,160/255))
plt.plot(lsbot['waterlevel'], label='Langhisha Bottom', color= 'k')

# Graph settings
plt.xlabel('Year')
plt.ylabel('Water level (m)')
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(figdir + savetitle + '.png', dpi = 300)
plt.savefig(figdir + savetitle + '.pdf', dpi = 300)
plt.show()