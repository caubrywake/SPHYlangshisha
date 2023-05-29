# -*- coding: utf-8 -*-
"""
Loop throught folder to import modelled streamflow
"""

import os
os.chdir ('C:/SPHY3/script/SPHY/ModelEval')
# Plotting streamflow component
#import hydrostats as hs
import importSPHYtss as imp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import hydroeval as he

figdir = ("C:/SPHY3/analysis/model_output/fig/FlowComponents/") # directory to save figure
ratio_list = pd.DataFrame(columns=['folder', 'glacier_ratio', 'rain_ratio', 'snow_ratio', 'base_ratio'])
perf_list = pd.DataFrame(columns=['folder', 'NSE', 'KGE', 'RMSE', 'MARE', 'PBIAS'])
#%% List of folder names

# Get list of folders in the directory
directory = "C:/SPHY3/sphy_20230218/"

# Get list of folders in the directory
folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f)) and f.startswith("output_")]

#%% Import measured streaflow (2017-2018)
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
    
#%% Loop through folders
for folder in folders:
   
    #folder = 'output_sphy_config_base16_2' % dfor just one specific folder
    path = os.path.join(directory, folder)

    dd = '01'
    mm = '01'
    yy = '2014'

    min_val = 0
    max_val = 1500
  
    try:
        # Import modelled streamflow
        mod = imp.importtss(yy, mm, dd, path + "/QAllDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
        mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
        qall = mod[['Outlet']]
    except FileNotFoundError:
        print("File not found for folder: {}. Skipping...".format(folder))
        continue
   
    # Import modelled streamflow
    mod  = imp.importtss(yy, mm, dd, path + "/QAllDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
    mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
    qall = mod[['Outlet']]

    # Import modelled Glacier flow
    mod  = imp.importtss(yy, mm, dd, path + "/GTotDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
    mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
    glac = mod[['Outlet']]

    # Import modelled Rain flow
    mod  = imp.importtss(yy, mm, dd, path + "/RTotDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
    mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
    rain = mod[['Outlet']]

    # Import modelled Snow flow
    mod  = imp.importtss(yy, mm, dd, path + "/STotDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
    mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
    snow = mod[['Outlet']]

    # Import modelled Baseflow
    mod  = imp.importtss(yy, mm, dd, path + "/BTotDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
    mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
    base = mod[['Outlet']]
    
    # Import modelled Baseflow
    mod  = imp.importtss(yy, mm, dd, path + "/GwreDTS.tss",  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS', 'soil'])
    mod = mod.where((mod > min_val) & (mod < max_val), np.nan)
    rainf = mod[['AWS']]
    
    # Label and variable names
    modname = 'Outlet'  # name of modelled variable column
    measname = 'Q'
    label1 = 'Modelled'  # label on figure
    label2 = 'Glacier'
    label3 = 'Rain'  # label on figure
    label4 = 'Snow'
    label5 = 'Baseflow'
    figtitle = 'Streamflow Component @ LS'
    savetitle = 'ModelledFlowComponent'  # name of saved file

    # Specify start and end dates for plotting
    start_date = '2017-05-01'
    end_date = '2017-12-31'
    
    # Create subplots
    # Create subplots
    fig, ax = plt.subplots(figsize=(4,4))

    # Plot modelled streamflow components within the specified date range
    ax.plot(mod.loc[start_date:end_date].index, qall[modname].loc[start_date:end_date], label=label1, color='red')
    ax.plot(meas.loc[start_date:end_date].index, meas[measname].loc[start_date:end_date], label='Measured', color='black')
    ax.plot(mod.loc[start_date:end_date].index, glac[modname].loc[start_date:end_date], label=label2, color='blue')
    ax.plot(mod.loc[start_date:end_date].index, rain[modname].loc[start_date:end_date], label=label3, color='magenta')
    ax.plot(mod.loc[start_date:end_date].index, snow[modname].loc[start_date:end_date], label=label4, color='cyan')
    ax.plot(mod.loc[start_date:end_date].index, base[modname].loc[start_date:end_date], label=label5, color='orange')
    #ax.plot(mod.loc[start_date:end_date].index, rainf['AWS'].loc[start_date:end_date], label='subp', color='black')
 
    ax.legend()
    fig.suptitle(str(folder))
    # Set y-axis label
    ax.set_ylabel('Discharge (m3/s)')
    
    # Set x-axis tick labels rotation
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
    # Save figure as .pdf
    plt.savefig(figdir + folder + 'FlowComp.pdf', format='pdf', dpi=300, bbox_inches='tight')
    # Save figure as .png
    plt.savefig(figdir + folder + 'FlowComp.png', dpi=300, bbox_inches='tight')

    plt.show()
    
    # Calculate the sum of plotted part fo the time series
    glac_filtered = glac.loc[start_date:end_date]
    rain_filtered = rain.loc[start_date:end_date]
    snow_filtered = snow.loc[start_date:end_date]
    base_filtered = base.loc[start_date:end_date]

    glac_sum = glac_filtered.sum()
    rain_sum = rain_filtered.sum()
    snow_sum = snow_filtered.sum()
    base_sum = base_filtered.sum()
    
    # Calculate the paer of the time series
    total_sum = glac_sum + rain_sum + snow_sum + base_sum
    
    # Calculate the ratios for each variable
    glac_ratio = glac_sum / total_sum
    rain_ratio = rain_sum / total_sum
    snow_ratio = snow_sum / total_sum
    base_ratio = base_sum / total_sum
    
    glac_ratio_value = glac_ratio.item()
    rain_ratio_value = rain_ratio.item()
    snow_ratio_value = snow_ratio.item()
    base_ratio_value = base_ratio.item()
    
    # Append all ratio values to ratio_list DataFrame
    ratio_list = ratio_list.append(pd.DataFrame({'folder': [folder],
                                             'glacier_ratio': [glac_ratio_value],
                                             'rain_ratio': [rain_ratio_value],
                                             'snow_ratio': [snow_ratio_value],
                                             'base_ratio': [base_ratio_value]}),
                                                ignore_index=True)


    # flow evaluatuion metric
    mask = (mod.index >= start_date) & (mod.index <= end_date)
    mod_cut= qall.loc[mask]
    mod_cut = mod_cut [['Outlet']]
    mod_cut = mod_cut.iloc[1:]
    mask = (meas.index >= start_date) & (meas.index <= end_date)
    meas_cut= meas.loc[mask]
    meas_cut = meas_cut[['Q']]
    meas_cut=meas_cut.iloc[1:]
    
  
    # Compute the cumulative sum
    meas_cumsum = np.cumsum(meas_cut)
    mod_cumsum = np.cumsum(mod_cut)
    # Create a plot
    '''
    plt.plot(meas_cumsum, label = 'meas')
    plt.plot(mod_cumsum, label = 'mod')
    # Add labels and title
    plt.xlabel('Data Points')
    plt.ylabel('Cumulative Sum')
    plt.title(folder)
    plt.legend()
    
    # Show the plot
    plt.show()
'''
    # convert columns to numpy arrays
    mod_array = np.array(mod_cut['Outlet'], dtype=float)
    meas_array = np.array(meas_cut['Q'], dtype=float)
    
    nse2 = he.evaluator(he.nse, mod_array, meas_array)
    kge2, r2, alpha2, beta2 = he.evaluator(he.kge, mod_array, meas_array)
    rmse2 = he.rmse(mod_array, meas_array)
    mare2=he.mare(mod_array, meas_array)
    pbias2=he.pbias(mod_array, meas_array)

     # Get the values for each performance metric
    nse_value = nse2.item()
    kge_value = kge2.item()
    rmse_value = rmse2.item()
    mare_value = mare2.item()
    pbias_value = pbias2.item()
    

    
    perf_dict = {'folder': folder, 'NSE': nse_value, 'KGE': kge_value, 'RMSE': rmse_value, 'MARE': mare_value, 'PBIAS': pbias_value}

    # Append the values to the perf_list DataFrame
    perf_list = perf_list.append(pd.Series(perf_dict), ignore_index=True)

# xporrt the lists
# save the DataFrame to a CSV file
perf_list.to_csv(figdir + 'StreamflowMetric_' + start_date + '_' + end_date+'.csv', index=False)
    # Export the DataFrame as a .csv file
ratio_list.to_csv(figdir + 'FlowRatios_'+ start_date + '_' + end_date+'.csv', index=False)

