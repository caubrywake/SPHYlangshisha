# -*- coding: utf-8 -*-
"""
RECHARGE .CSV FILELIST

This scripts create an .csv file with the names and time steps for the recharge shapefiles
The values in the .csv file can be used when importing the recharge shapefile in modelmuse

For each file in the rechrage values formatted to for modelmuse, the names are read, formatted, and printed in a .csv file
Created on Mon Apr  3 11:34:50 2023

@author: carol
"""
import os
import glob
import csv
import pandas as pd

# Define the paths to the rasters and shapefile
raster_path = r"C:\\SPHY3\\sphy_20230218\\output_sphy_config_base16_2\\"
shapefile_path = r"D:\\UU\\modflow\\recharge\\recharge_fishnet_20230420_1.shp"
save_fig = 'D:/UU/figure/recharge_fig/'

# Create a list of file names to loop through
file_list = [f for f in glob.glob(raster_path + "GwreM*") if not f.endswith(".aux.xml")]
time_list = []
name_list=[]

# Loop throught files and create name
for file_path in file_list:
        # Add the mean value to the fishnet GeoDataFrame
        file_name = os.path.basename(file_path)
        fig_name = 'GW' + file_name[-5:].replace('.', '')  
        last_num = file_name[-5:].replace('.', '') 
        name_list.append(fig_name)
        time_list.append(last_num)
        
new_number_list = [str(int(number)) for number in time_list]
last_number_list = [str(0)] + new_number_list[0:-1]
df = pd.DataFrame({'Time 1': last_number_list, 'Time 2': new_number_list, 'Attribute': name_list})

# create a new row with the values to add for the steady state time step
new_row = ['-1', '0', 'GW0212']
new_df = pd.DataFrame([new_row], columns=['Time 1', 'Time 2', 'Attribute'])
# append the new row to the DataFrame
df = new_df.append(df, ignore_index=True)

# write name file
with open('D:\\UU\\modflow\\input\\name_fileGWrecharge.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in df:
        combined_row = [''.join(row)] # join the characters and create a list with one item
        writer.writerow(combined_row)

df.to_csv('D:\\UU\\modflow\\input\\name_fileGWrecharge_20230420.csv', index=False)
     