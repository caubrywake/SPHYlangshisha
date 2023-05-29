# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 11:20:43 2023

@author: carol
"""
import numpy as np
import os
import rasterio
from rasterio import Affine as A
from rasterio.warp import reproject, Resampling

# Load the source and target rasters
src_path = 'C:\\SPHY3\\sphy_20230218\\input_cut\\forcing_cut\\prec0000.001'
target_path = 'C:\\SPHY3\\sphy_20230218\\input_cut\\cut\\clone2.map'
save_path = 'C:\\SPHY3\\sphy_20230218\\input_cut\\forcing_cut\\test\\prec0000.001'


# Input directory with rasters
input_dir = 'C:\\SPHY3\\sphy_20230218\\input_cut\\forcing_cut'
# Output directory to save the resampled rasters
output_dir = 'C:\\SPHY3\\sphy_20230218\\input_cut\\forcing_cut_2\\'


# Open the reference raster
with rasterio.open(target_path) as ref:
    # Read the metadata of the reference raster
    ref_metadata = ref.meta
    ref_metadata['crs'] = rasterio.crs.CRS.from_epsg(9822)

    # Loop over all files in the input directory
    for filename in os.listdir(input_dir):
            src_path = os.path.join(input_dir, filename)
            save_path = os.path.join(output_dir, filename)

            # Open the source raster
            with rasterio.open(src_path) as src:
                # Read the metadata and data of the input raster
                metadata = src.meta
                data = src.read(1)

                # Update the metadata of the input raster to match the reference raster
                metadata.update({
                    'transform': ref_metadata['transform'],
                    'width': ref_metadata['width'],
                    'height': ref_metadata['height'],
                    'crs' : ref_metadata['crs']
                })

                # Create an empty destination array with the correct shape and data type
                dst_shape = (ref_metadata['height'], ref_metadata['width'])
                dst_dtype = data.dtype
                destination = np.zeros(dst_shape, dtype=dst_dtype)

                # Resample the input raster to match the resolution and extent of the reference raster
                rasterio.warp.reproject(
                    source=data,
                    src_crs=metadata['crs'],
                    src_transform=metadata['transform'],
                    src_nodata=metadata['nodata'],
                    destination=destination,
                    dst_transform=ref_metadata['transform'],
                    dst_crs=ref_metadata['crs'],
                    dst_nodata=metadata['nodata'],
                    resampling=rasterio.warp.Resampling.bilinear
                )

                metadata.update({'driver': 'PCRaster', 'PCRASTER_VALUESCALE': 'VS_SCALAR'})

                # Write the resampled raster to the output file with the same name
                with rasterio.open(save_path, 'w', **metadata) as dst:
                    dst.write(destination, 1)

       #%% Plot
      # Get spatial transform and dimensions
      transform = src.transform
      width = src.width
      height = src.height
        
      # Define x and y extent
      xmin, ymin = transform * (0, height)
      xmax, ymax = transform * (width, 0)
      extent = [xmin, xmax, ymin, ymax]

      # Plot DEM with colorbar
      plt.imshow(clone, cmap='terrain', extent=extent)
      plt.colorbar(label='Elevation (m)')
      plt.xlabel('Longitude')
      plt.ylabel('Latitude')
      plt.show()
                  """
      