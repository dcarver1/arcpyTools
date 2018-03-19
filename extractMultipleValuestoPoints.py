# -*- coding: utf-8 -*-
"""
Code for setting up the extract multiple values to points in arcpy 
The text input is kinda pain in the but so this script uses 
glob and some for loops to streamline the process. 
Dan Carver 9/28/17
"""

import arcpy
import glob 
import os
import time 
from arcpy import env
from arcpy.sa import *
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
print("spatial analysis has been checked out")

start = time.time()

# Set to the folder location that contains all the raster information 
workspace = arcpy.env.workspace = r"G:\DEVELOP_Fall2017_CRBII\DEVELOP-CRB\Indicies\LS5\p035r034"

#select all the files that end in .tif within the defined workspace
rasterList = (glob.glob(workspace + "\\*.tif"))

# define the point feature for extract value process
inPointFeatures = r"C:\Users\research\Documents\ArcGIS\Default.gdb\RO_present_06_field_inVbet"

print "this is the feature bring worked with ", inPointFeatures, '.'
#create an empty list
inRasterList =[]
#itorate through the list of raster names
for i in rasterList:
    txtname = os.path.basename(i)#select the final segemnt of the path
    file_name = [i,(str(txtname)[12:-4])]# create a list of file directory and file name
    inRasterList.append(file_name)# append the list to a second list of 

print('the raster list has been created')

# Execute ExtractValuesToPoints
print "The extract multiple values to points tool is running, be patient."
ExtractMultiValuesToPoints(inPointFeatures, inRasterList)
end = time.time()

print "This process ran in ",(end-start)/60 ,"minutes." 

