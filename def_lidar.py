# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 13:51:43 2016

@author: dcarver

This is a list of fuctions that will be used for creating the lidar basemaps
for the disk maps.

"""
import arcpy
from arcpy import env
import arcpy.sa as sa
env.workspace = workspace =  r"G:\personal\diskgolfmapping"
arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension("Spatial")

def las_to_GandFrreturns(las_files, mask,name):
    '''This function takes a list of las files, creates a las dataset. Then
    it create a lasd for first and ground returns. After which it rasterizes
    the lasd and masks them to a specified area.
    las_files:  a list of the paths for all the las files
    mask:
    '''
    lasd = arcpy.CreateLasDataset_management(las_files,name)
    g_lasd = arcpy.MakeLasDatasetLayer_management(lasd,"ground", 2)
    g_ras = arcpy.LasDatasetToRaster_conversion(g_lasd,"g_rast.img", "ELEVATION",
                                            "BINNING AVERAGE NATURAL_NEIGHBOR",
                                            "FLOAT", "CELLSIZE", 0.5)
    g_mask = arcpy.sa.ExtractByMask(g_ras,mask)
    g_mask.save("g_mask"+name+".img")
    f_lasd = arcpy.MakeLasDatasetLayer_management(lasd,"first", '', 1)
    f_ras = arcpy.LasDatasetToRaster_conversion(f_lasd,"f_rast.img", "ELEVATION",
                                            "BINNING MAXIMUM NATURAL_NEIGHBOR",
                                            "FLOAT", "CELLSIZE", 0.5)
    f_mask = arcpy.sa.ExtractByMask(f_ras, mask, name)
    f_mask.save("f_mask"+ name + ".img")
    return f_mask, g_mask


def las_fhillshade(f_mask, name):
    '''takes the first return mask lasd and creates a hillshade'''
    f_mask = str(f_mask)
    f_hill = arcpy.sa.Hillshade(f_mask)
    f_hill.save("\f_hill" + name + ".img")
    return f_hill

def las_differ_ras(f_mask, g_mask, name):
    '''creates a difference raster between the first return and the second
    highlights the elevated surface(trees) of the area'''
    f_mask = str(f_mask)
    g_mask = str(g_mask)
    dif_ras = arcpy.Raster(f_mask) - arcpy.Raster(g_mask)
    dif_ras.save("dif_ras" + name + ".img")
    return dif_ras


# adding to the script so I can find all las files in a fold and run this
# process over a for p

import glob, os

lasFiles = []
os.chdir(workspace)
for file in glob.glob("*.las"):
    lasFiles.append(file)

for i in lasFiles:
    #for now the name file will just be the last 4 digits
    name = str(lasFile[-8:-4])
    f_mask, g_mask = las_to_GandFrreturns(las_files, mask, name)
    f_hill = las_fhillshade(f_mask, name)
    #this one below is what works... hopefully the reference will work
    #dif_ras = las_differ_ras('f_mask.img', 'g_mask.img')
    dif_ras = las_differ_ras(f_mask, g_mask)



las_files = env.workspace + r"\las\CO_Denver_2008_000128.las"
mask = env.workspace + r"\extent\extent.shp"
name = 'cc_lasd'

f_mask, g_mask = las_to_GandFrreturns(las_files, mask, name)

f_hill = las_fhillshade(f_mask)

dif_ras = las_differ_ras('f_mask.img', 'g_mask.img')
