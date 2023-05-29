# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 10:18:34 2023

@author: carol
"""

import os
# go to function directpry
os.chdir("C:\\SPHY3\\script\\SPHY\\") # directory to save maps
import tifftopcraster as topcr

# common poutput dir
output_dir='C:\\SPHY3\\sphy_20230218\\input_20230322\\forcing_20230523_1\\' 
# create a directry to export the temperature maps
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
os.chdir(output_dir) # directory to save maps

# temperature mean
input_dir = 'D:\\UU\\processed_files\\temp_maps\\20230419_2temp\\' #input dir
topcr.tifftopcraster(input_dir, output_dir)

# Temp min
input_dir = 'D:\\UU\\processed_files\\temp_maps\\20230419_2tmin\\' #input dir
topcr.tifftopcraster(input_dir, output_dir)

# temp max
input_dir = 'D:\\UU\\processed_files\\temp_maps\\20230419_2tmax\\' #input dir
topcr.tifftopcraster(input_dir, output_dir)

# precip
input_dir = 'D:\\UU\\processed_files\\temp_maps\\20230419_3prec\\' #input dir
topcr.tifftopcraster(input_dir, output_dir)
