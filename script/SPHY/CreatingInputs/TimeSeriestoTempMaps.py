# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 20:19:25 2023
This script takes the input timeseries of temperature (mean, max, min) 
and using the elevation DEM and montlhy temperature gradients, 
extrapolates it to the study area (as dictated by the dem). 
for each timestep. a .tiff file is created with the distributed values
@author: carol
"""

import os
os.chdir("C:\\SPHY3\\script\\SPHY\\") # directory to save maps
import TimeseriestoRaster_v2 as ts

dempath = 'D:\\UU\\SPHY\\scratch\\v2\\dem_filled.tif' # dem location
start_date = '2014-01-01'
end_date = '2020-12-31'
figdir = ("C:/SPHY3/analysis/model_output/fig/dataplot/") # directory to save figure

#%% Minimum temp
fn ='C:\\SPHY3\\analysis\\data_processed\\LSaws_Ta_filledwithERA_20132021min_withspinup.csv' # time series
csv_out = 'C:\\SPHY3\\analysis\\data_processed\\temp_min_output_2017.csv'
label = "tmin"

dir_name = 'D:\\UU\processed_files\\temp_maps\\20230419_2tmin\\'

# create a directory to export the temperature maps
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
os.chdir(dir_name) # directory to save maps
ts.temperature_tiff(figdir, fn, dempath, start_date, end_date, csv_out, label)

#%% Maximum temp
figdir = ("C:/SPHY3/analysis/model_output/fig/dataplot/") # directory to save figure
fn ='C:\\SPHY3\\analysis\\data_processed\\LSaws_Ta_filledwithERA_20132021max_withspinup.csv' # time series
csv_out = 'C:\\SPHY3\\analysis\\data_processed\\temp_max_output_2017.csv'
label = 'tmax'

dir_name = 'D:\\UU\processed_files\\temp_maps\\20230419_2tmax\\'

# create a directory to export the temperature maps
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
os.chdir(dir_name) # directory to save maps
ts.temperature_tiff(figdir, fn, dempath, start_date, end_date, csv_out, label)

#%% Mean temp
figdir = ("C:/SPHY3/analysis/model_output/fig/dataplot/") # directory to save figure
fn ='C:\\SPHY3\\analysis\\data_processed\\LSaws_Ta_filledwithERA_20132021_withspinup.csv' # time series
csv_out = 'C:\\SPHY3\\analysis\\data_processed\\temp_mean_output_2017.csv'
label = 'temp'

dir_name = 'D:\\UU\processed_files\\temp_maps\\20230419_2temp\\'

# create a directory to export the temperature maps
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
os.chdir(dir_name) # directory to save maps
ts.temperature_tiff(figdir, fn, dempath, start_date, end_date, csv_out, label)

