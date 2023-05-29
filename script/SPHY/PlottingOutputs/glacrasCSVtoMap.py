# -*- coding: utf-8 -*-
"""
Created on Mon May 29 16:05:23 2023

@author: carol
"""

# Create glac Runoff mas from .csv file

import pandas as pd
import rasterio
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
import numpy as np
import rasterio
from rasterio.transform import from_origin
import numpy as np
import matplotlib.pyplot as plt
from rasterio.features import geometry_mask


### Import glac_D shapefile
path = "D:\\UU\\modflow\\input\\Glacier_ID_shapefile.shp"
glacier_gdf = gpd.read_file(path)
glacier_gdf = glacier_gdf.sort_values(by="DN", ascending=True)
glacier_gdf = glacier_gdf.set_index("DN")
glacier_gdf.plot(color='blue', edgecolor='black', linewidth=0.5)

## Import Glac percolation .csv
path = "C:/SPHY3/sphy_20230218/output_20230529/"
fn = path+"Glacr.csv"

# Read in th data
GlacP= pd.read_csv(fn)
# Combine the date and time columns into a single datetime column
GlacP['datetime'] = pd.to_datetime(GlacP['Unnamed: 0'])

# Set the index of the DataFrame to the datetime column
GlacP.set_index('datetime', inplace=True)
glacp_df = GlacP.resample('M').mean()
glacp_df_tr = glacp_df.transpose()
glacp_df_tr['Index'] = glacp_df_tr.index

df1 = glacier_gdf
df2 = glacp_df_tr

# Reset the index of both DataFrames
df1.reset_index(inplace=True)
df2.reset_index(inplace=True)
glacp_df_tr['Index'] = glacp_df_tr['Index'].astype('int64')
glacperc = pd.merge(glacier_gdf, glacp_df_tr, left_on='DN', right_on='Index')
glacperc = glacperc.drop(['Index', 'index'], axis=1)

import rasterio
from rasterio import features
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# Specify the input raster file path
raster_file = 'D:\\UU\\SPHY\\scratch\\v2\\dem_filled.tif'
# Open raster file
raster = rasterio.open(raster_file)


from datetime import datetime

# Convert attribute column names to datetime objects
date_format = '%Y%m%d'
glacperc_dates = [col.strftime(date_format) for col in glacperc.columns if col != 'geometry' and col != 'DN']

# Find the minimum date to calculate number of days since the first date
min_date = datetime.strptime('2013-12-31', '%Y-%m-%d')
##
# Loop through all attribute columns
for attr_col in glacperc.columns:
    if attr_col != 'geometry' and attr_col != 'DN':
        # Convert attr_col to string representation of the date
        attr_col_str = attr_col.strftime(date_format)
        
        # Calculate the number of days between the minimum date and the current attribute column date
        num_days = (datetime.strptime(attr_col_str, date_format) - min_date).days

        # Create tuples of geometry, value pairs, where value is the attribute value you want to burn
        geom_value = ((geom, value) for geom, value in zip(glacperc.geometry, glacperc[attr_col]))

        # Rasterize vector using the shape and transform of the raster
        rasterized = features.rasterize(geom_value,
                                        out_shape=raster.shape,
                                        transform=raster.transform,
                                        all_touched=True,
                                        fill=0,  # background value
                                        merge_alg=features.MergeAlg.replace,
                                        dtype='float32')  # use float32 as the data type

        # Update raster metadata
        meta = raster.meta
        meta.update(dtype='float32', count=1, nodata=-9999)  # update metadata with the new nodata value

        # Generate output file name based on the number of days since the first date
        num_days_str = f'{num_days:06d}'  # Use six digits with leading zeros
        output_file = f'C:/SPHY3/sphy_20230218/output_20230529/glacr/GlacrM{num_days_str[:3]}.{num_days_str[3:]}'  # Add dot between front three and last three digits
        
        
        # Write rasterized array to output file
        with rasterio.open(output_file, 'w', **meta) as dst:
            dst.write_band(1, rasterized)

        print(f'Rasterized raster for attribute column {attr_col_str} saved to: {output_file}')


