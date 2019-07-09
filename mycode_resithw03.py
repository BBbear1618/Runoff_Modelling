#-- mycode_resithw03.py
#-- Retake assignment 03 GEO1015 (2018-2019)
#-- [YOUR NAME] Yifang Zhao / Jinglan Li
#-- [YOUR STUDENT NUMBER] 4798899 / 4781937

import math
import rasterio
import numpy as np

def flow_direction(elevation):
    """
    !!! TO BE COMPLETED !!!
     
    Function that computes the flow direction
     
    Input:
        elevation: grid with height values
    Output:
        returns grid with flow directions (encoded in whichever way you decide)
 
    """
    row, column = elevation.shape
    direction = np.zeros(elevation.shape)

    for i in range(row):
        for j in range(column):
            slope = 0
            code = 0
            slopes = []
            codes = []
            if i != 0:
                slopes.append(elevation[i, j] - elevation[i - 1, j])
                codes.append(70)
            if i != 0 and j != column - 1:
                slopes.append((elevation[i, j] - elevation[i - 1, j + 1]) / 2**0.5)
                codes.append(80)
            if j != column - 1:
                slopes.append(elevation[i, j] - elevation[i, j + 1])
                codes.append(10)
            if i != row - 1 and j != column - 1:
                slopes.append((elevation[i, j] - elevation[i + 1, j + 1]) / 2**0.5)
                codes.append(20)
            if i != row - 1:
                slopes.append(elevation[i, j] - elevation[i + 1, j])
                codes.append(30)
            if i != row - 1 and j != 0:
                slopes.append((elevation[i, j] - elevation[i + 1, j - 1]) / 2**0.5)
                codes.append(40)
            if j != 0:
                slopes.append(elevation[i, j] - elevation[i, j - 1])
                codes.append(50)
            if i != 0 and j != 0:
                slopes.append((elevation[i, j] - elevation[i - 1, j - 1]) / 2**0.5)
                codes.append(60)
            
            for n in range(len(slopes)):
                if slopes[n] > slope:
                    slope = slopes[n]
                    code = codes[n]
            direction[i, j] = code
            
    return direction
        

        
def flow_accumulation(directions):
    """
    !!! TO BE COMPLETED !!!
     
    Function that computes the flow accumulation
     
    Input:
        directions: grid with flow directions (encoded in whichever way you decide)
    Output:
        returns grid with accumulated flow (in number of upstream cells)
 
    """
    row, column = directions.shape
    temp = np.ones(directions.shape)
    accumulation = np.ones(directions.shape)
    n = 0 # Iteration times
    
    while True:
        n += 1
        for i in range(row):
            for j in range(column):
                if directions[i, j] == 10:
                    accumulation[i, j + 1] += temp[i, j]
                elif directions[i, j] == 20:
                    accumulation[i + 1, j + 1] += temp[i, j]
                elif directions[i, j] == 30:
                    accumulation[i + 1, j] += temp[i, j]
                elif directions[i, j] == 40:
                    accumulation[i + 1, j - 1] += temp[i, j]
                elif directions[i, j] == 50:
                    accumulation[i, j - 1] += temp[i, j]
                elif directions[i, j] == 60:
                    accumulation[i - 1, j - 1] += temp[i, j]
                elif directions[i, j] == 70:
                    accumulation[i - 1, j] += temp[i, j]
                elif directions[i, j] == 80:
                    accumulation[i - 1, j + 1] += temp[i, j]
        temp = accumulation
        accumulation = np.ones(directions.shape)
        if n > 140: # customized threshold
            if verify(directions, temp):
##                print("Iteration times: ", n)
                break
            else:
                n -= 20

    return temp
    

def write_directions_raster(raster, input_profile):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with nearest neighbour interpolation
     
    Input:
        raster: grid with flow directions (encoded in whichever way you decide)
        input_profile: profile of elevation grid (which you can copy and modify)
 
    """
    output_file = 'output-directions.tif'
    with rasterio.open(output_file, 'w', 
                   driver=input_profile['driver'], 
                   height=input_profile['height'],
                   width=input_profile['width'], 
                   count=1, 
                   dtype=rasterio.uint8,
                   crs=input_profile['crs'], 
                   transform=input_profile['transform']) as dst:
        dst.write(raster.astype(rasterio.uint8), 1)
    print("File written to '%s'" % output_file)

def write_accumulation_raster(raster, input_profile):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with nearest neighbour interpolation
     
    Input:
        raster: grid with accumulated flow (in number of upstream cells)
        input_profile: profile of elevation grid (which you can copy and modify)
 
    """
    output_file = 'output-accumulation.tif'
    with rasterio.open(output_file, 'w', 
                   driver=input_profile['driver'], 
                   height=input_profile['height'],
                   width=input_profile['width'], 
                   count=1, 
                   dtype=rasterio.uint32,
                   crs=input_profile['crs'], 
                   transform=input_profile['transform']) as dst:
        dst.write(raster.astype(rasterio.uint32), 1)
    print("File written to '%s'" % output_file)

def verify(directions, accumulation):
    """
    Indicate whether the accumulation process is done.
    """
    row, column = directions.shape
    # find the number of pixels which do have a flow direction
    nonzero = 0
    allthebiggest = 0
    for i in range(row):
        for j in range(column):
            if directions[i, j] != 0:
                nonzero += 1
            elif directions[i, j] == 0 and accumulation[i, j] > 1:
                nonzero += 1
                allthebiggest += accumulation[i, j]
                
##    print("The number of non-zero pixels: {}".format(nonzero))
##    print("The sum of locally biggest values: {}".format(allthebiggest))
    return nonzero == allthebiggest
