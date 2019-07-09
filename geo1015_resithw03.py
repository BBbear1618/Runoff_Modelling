#-- geo1015_resithw03.py
#-- hw03 resit GEO1015/2018
#-- 2019-02-27

#------------------------------------------------------------------------------
# DO NOT MODIFY THIS FILE!!!
#------------------------------------------------------------------------------

import json, sys
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns

import mycode_resithw03

def main():
        # Open file
        with rasterio.open('tasmania.tif') as src:
                elevation = np.array(src.read()[0])
                profile = src.profile


        # Plot input
        plt.figure(1)
        im = plt.imshow(elevation)
        plt.colorbar(im)
        plt.show()

        # Compute flow directions
        directions = mycode_resithw03.flow_direction(elevation)

        # Plot directions and write them to a file
        plt.figure(2)
        im = plt.imshow(directions)
        plt.colorbar(im)
        plt.show()
        mycode_resithw03.write_directions_raster(directions, profile)

        # Compute flow accumulation
        accumulation = mycode_resithw03.flow_accumulation(directions)

        # Plot accumulation and write them to a file
        plt.figure(3)
        im = plt.imshow(accumulation, norm=LogNorm())
        plt.colorbar(im)
        plt.show()
        mycode_resithw03.write_accumulation_raster(accumulation, profile)

if __name__ == '__main__':
  main()

