'''
The goal of this script is to create a 2d array with alternating values
that will be referenced to a landsat image and used for a framework for
sampling.

Dan carver
github:dcarver1

'''


def rastDesc(inputRaster):
    '''
    the goal of this function is to gather raster properties and return them as a
    dictionary
    Other properties can be gathered, see docs on GetRasterProperties
    '''
    left1 = arcpy.GetRasterProperties_management(raster, "LEFT" )
    left = float(left1.getOutput(0))
    bottom1 = arcpy.GetRasterProperties_management(raster, "BOTTOM" )
    bottom = float(bottom1.getOutput(0))
    numRows1 = arcpy.GetRasterProperties_management(raster, "ROWCOUNT" )
    numRows = int(numRows1.getOutput(0))
    numCols1 = arcpy.GetRasterProperties_management(raster, "COLUMNCOUNT" )
    numCols = int(numCols1.getOutput(0))
    xSize1 = arcpy.GetRasterProperties_management(raster, "CELLSIZEX" )
    xSize = float(xSize1.getOutput(0))
    ySize1 = arcpy.GetRasterProperties_management(raster, "CELLSIZEY" )
    ySize = float(ySize1.getOutput(0))
    #ensure that the number of columns is odd
    if numCols % 2 == 0:
        numCols += 1
    else:
        pass
    #Return the values in a dictionary
    values = {"left" : left, "bottom" : bottom, "numRows" : numRows,
              "numCols" : numCols, "xSize" : xSize, "ySize" : ySize}

    return values




import numpy as np
import arcpy

'''
You need to enter three variable for this to work
1. pathToRast = the location of your raster
2. lowerLeft = coordinates of the lower left corner of your image. (options below)
3. myRaster.save = set the path and name of the output raster. Include file
extension type
'''

#import refernce landsat raster
pathToRast = r"D:\BigBison\Spatial_Data\Sentinel\EarthExplorerSentinel\mosacsentTiff.tif"
raster = arcpy.Raster(pathToRast)


#set environmental varables based on raster
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = raster
#if this coordinate system does not work we will need to reproject in the input raster
#arcpy.SpatialReference("WGS 1984")
arcpy.env.cellSize = raster
arcpy.env.snapRaster = raster

#Store values into a dictionary
values = rastDesc(raster)

#call the left and bottom values to define the lower left point
# this is in meters due to landsats projection. You can find your point in arcmap and enter it
# manually
lowerLeftAproximate = [352674, 3990249]

#set the lowerleft so it aligns with a cell of the raster
adjustLeft = lowerLeftAproximate[0] - ((values['left'] - lowerLeftAproximate[0]) % values['xSize'])
adjustBottom =  lowerLeftAproximate[1] - ((values["bottom"] - lowerLeftAproximate[1])% values['ySize'])

lowerLeft = arcpy.Point(adjustLeft, adjustBottom)

##uncommit this code if you want to keep it defined to the lower left corner of the ls area.
lowerLeft = arcpy.Point(values["left"],values["bottom"])


#calculate the totalCells
# We had to cut this in half due to a memory error. I'm going to test it but for now it an
# appropriate area

if values["numCols"] % 2 == 0:
    numCols = values["numCols"]+ 1
else:
    numCols = values["numCols"]


totalCells = (values["numRows"]) * (numCols)

# this was just hack from stackexchange, I always get a little confused with
# numpy indexing, but it should do the trick for us
a = np.empty((totalCells,))
a[::2] = 0
a[1::2] = 1

print(a[0:15])

#reshape the array to match the dimensions of the landsat scene
lsShape = a.reshape((values["numRows"]),(numCols))


print (lsShape.shape)

# Convert the array to raster and save it
myRaster = arcpy.NumPyArrayToRaster(lsShape, lowerLeft ,values["xSize"],values["ySize"])
print('the array has been made into a raster.' )
myRaster.save(r"D:\BigBison\Spatial_Data\Sentinel\Shoelaces.TIF")

'''
to load onto Earth engine
Log into earth engine
Add Asset
navigate to path and add feature

this will take a bit

You can share the file from your asset folder with whom ever you want.

To display, add to map

'''
