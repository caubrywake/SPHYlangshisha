# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 19:50:38 2023

@author: carol
"""

# emp forcing with spin up period
import pandas as pd
#%% Ta mean
###################################################################################
# Load the CSV file
df = pd.read_csv('C:/SPHY3/analysis/data_processed/LSaws_Ta_filledwithERA_20132021.csv')

# Convert the date column to a datetime object
df['date'] = pd.to_datetime(df['datetime'])

# Filter the rows based on date range
df_filtered = df[(df['date'] >= '2014-01-01') & (df['date'] <= '2020-12-31')]

# Copy the filtered dataframe to create a second copy
df_copy = df_filtered.copy()

# Update the date column in the copied dataframe by subtracting 7 years
df_copy['date'] = df_copy['date'] - pd.DateOffset(years=7)

# Concatenate the original filtered dataframe and the copied dataframe vertically
df_result = pd.concat([df_filtered, df_copy], ignore_index=True)

# Sort the resulting dataframe by date
df_result = df_result.sort_values('date')

# Reset the index
df_result = df_result.reset_index(drop=True)

# remove the ofll date 
df_result = df_result.drop(columns=['datetime'])


# Reformat the date column to have only year-month-day
df_result['date'] = df_result['date'].dt.strftime('%Y-%m-%d')


# Reorder columns
df_result = df_result[['date', 'LS_filled']]

# Set the 'date' column as the index
df_result = df_result.set_index('date')  # <-- Update this line to set the index

# Write the resulting dataframe to a CSV file
df_result.to_csv('C:/SPHY3/analysis/data_processed/LSaws_Ta_filledwithERA_20132021_withspinup.csv', index=True)

###################################################################################
#%% Tmin
###################################################################################
# Load the CSV file
df = pd.read_csv('C:/SPHY3/analysis/data_processed/LSaws_Ta_filledwithERA_20132021min.csv')

# Convert the date column to a datetime object
df['date'] = pd.to_datetime(df['datetime'])

# Filter the rows based on date range
df_filtered = df[(df['date'] >= '2014-01-01') & (df['date'] <= '2020-12-31')]

# Copy the filtered dataframe to create a second copy
df_copy = df_filtered.copy()

# Update the date column in the copied dataframe by subtracting 7 years
df_copy['date'] = df_copy['date'] - pd.DateOffset(years=7)

# Concatenate the original filtered dataframe and the copied dataframe vertically
df_result = pd.concat([df_filtered, df_copy], ignore_index=True)

# Sort the resulting dataframe by date
df_result = df_result.sort_values('date')

# Reset the index
df_result = df_result.reset_index(drop=True)

# remove the ofll date 
df_result = df_result.drop(columns=['datetime'])


# Reformat the date column to have only year-month-day
df_result['date'] = df_result['date'].dt.strftime('%Y-%m-%d')


# Reorder columns
df_result = df_result[['date', 'LS_filled']]

# Set the 'date' column as the index
df_result = df_result.set_index('date')  # <-- Update this line to set the index

# Write the resulting dataframe to a CSV file
df_result.to_csv('C:/SPHY3/analysis/data_processed/LSaws_Ta_filledwithERA_20132021min_withspinup.csv', index=True)

###################################################################################
#%% Tmax
###################################################################################
# Load the CSV file
df = pd.read_csv('C:/SPHY3/analysis/data_processed/LSaws_Ta_filledwithERA_20132021max.csv')

# Convert the date column to a datetime object
df['date'] = pd.to_datetime(df['datetime'])

# Filter the rows based on date range
df_filtered = df[(df['date'] >= '2014-01-01') & (df['date'] <= '2020-12-31')]

# Copy the filtered dataframe to create a second copy
df_copy = df_filtered.copy()

# Update the date column in the copied dataframe by subtracting 7 years
df_copy['date'] = df_copy['date'] - pd.DateOffset(years=7)

# Concatenate the original filtered dataframe and the copied dataframe vertically
df_result = pd.concat([df_filtered, df_copy], ignore_index=True)

# Sort the resulting dataframe by date
df_result = df_result.sort_values('date')

# Reset the index
df_result = df_result.reset_index(drop=True)

# remove the ofll date 
df_result = df_result.drop(columns=['datetime'])

# Reformat the date column to have only year-month-day
df_result['date'] = df_result['date'].dt.strftime('%Y-%m-%d')

# Reorder columns
df_result = df_result[['date', 'LS_filled']]

# Set the 'date' column as the index
df_result = df_result.set_index('date')  # <-- Update this line to set the index

# Write the resulting dataframe to a CSV file
df_result.to_csv('C:/SPHY3/analysis/data_processed/LSaws_Ta_filledwithERA_20132021max_withspinup.csv', index=True)
###################################################################################
#%% Precip
###################################################################################
# Load the CSV file
df = pd.read_csv('D:\\UU\\field_data\\processed\\Pdaily_Ls_infilledw_CEcorr_20120503_20210701.csv')

# Convert the date column to a datetime object
df['date'] = pd.to_datetime(df['t'])

# Filter the rows based on date range
df_filtered = df[(df['date'] >= '2014-01-01') & (df['date'] <= '2020-12-31')]

# Copy the filtered dataframe to create a second copy
df_copy = df_filtered.copy()

# Update the date column in the copied dataframe by subtracting 7 years
df_copy['date'] = df_copy['date'] - pd.DateOffset(years=7)

# Concatenate the original filtered dataframe and the copied dataframe vertically
df_result = pd.concat([df_filtered, df_copy], ignore_index=True)

# Sort the resulting dataframe by date
df_result = df_result.sort_values('date')

# Reset the index
df_result = df_result.reset_index(drop=True)

# remove the ofll date 
df_result = df_result.drop(columns=['t'])

# Reformat the date column to have only year-month-day
df_result['date'] = df_result['date'].dt.strftime('%Y-%m-%d')

# Reorder columns
df_result = df_result[['date', 'Pcorr']]

# Set the 'date' column as the index
df_result = df_result.set_index('date')  

# Write the resulting dataframe to a CSV file
df_result.to_csv('C:/SPHY3/analysis/data_processed/PdailyCorr_Ls_infilledw_20120503_20210701_withspinup.csv', index=True)

# redo with the min, max, and precip
# then rerun the forcing raster
