from math import *
import csv
import numpy as np
import sys
from lxml import etree
from GenerateWaypointFile import makeWaypointFile
from pykml import parser
from pykml.parser import Schema
import os
import shutil
from pykml.factory import KML_ElementMaker as KML

# These are "constants" used for indexing into waypointList
LAT = 0
LON = 1

class ComputeGreedyRoute:
    def __init__(self, listOfCoordinates):
        self.coordList = listOfCoordinates          # List of points of interest, current position of drone at index 0
        self.visitedIndices = []                    # List of visited points
        self.waypointList = []                      # List of points to visit in order, initial current position of drone excluded
        self.waypointLabels = []                    # List of the labels for each evidence object in the waypointList
        self.numPoints = len(self.coordList)        # Number of lat lon points in list
        self.distances = np.zeros([self.numPoints, self.numPoints])


    # Given the index of a point, return the index of 
    # the closest point that hasn't already been visited
    def indexClosestPoint(self, indexOfPoint):
        tempMinDist = sys.float_info.max
        self.visitedIndices.append(indexOfPoint)
        tempMinIndex = -1
        
        for iRow in range(self.numPoints):
            if iRow in self.visitedIndices:
                continue
            elif self.distances[iRow][indexOfPoint] < tempMinDist:
                tempMinDist = self.distances[iRow][indexOfPoint]
                tempMinIndex = iRow
        return tempMinIndex
    
    # Returns distance between point1 and point2 in km
    # where point1 and point2 is a [lat,lon] pair 
    def getDistance(self, point1, point2):
        earthRadius = 6371                          # Radius of the earth in km   
        dLat = self.deg2rad(point1[LAT] - point2[LAT])   # Difference of latitudes in radians
        dLon = self.deg2rad(point1[LON] - point2[LON])   # Difference of longitudes in radians
        a = sin(dLat/2) * sin(dLat/2) + cos(self.deg2rad(point1[LAT])) * cos(self.deg2rad(point2[LAT])) * sin(dLon/2) * sin(dLon/2)                                                             
        c = atan2(sqrt(a), sqrt(1 - a)) * 2
        d = earthRadius * c                     # Distance in km
        return d;
    
    # Convert degrees to radians
    def deg2rad(self, deg):
        return deg * (pi/180.)
    
    def makeWaypointFile(self):
        for iRow in range(self.numPoints):
            for iCol in range(self.numPoints):
                self.distances[iRow][iCol] = self.getDistance(self.coordList[iRow], self.coordList[iCol])
        
        for k in range(self.numPoints):
            print(k, self.coordList[k])
                
        # Assume that point0 is the current position of the UAV
        # at the end of initial mapping
        # FIRST ENTRY IS NOT CURRENT POINT, IT IS START POINT
        # SHOULD BE MODIFIED
        currentPoint = 0
        while len(self.visitedIndices) < self.numPoints - 1:
            closestPoint = self.indexClosestPoint(currentPoint)
            self.waypointList.append(self.coordList[closestPoint])
            print(currentPoint, closestPoint)
            currentPoint = closestPoint
            
        # For debugging
        for k in range(len(self.waypointList)):
            print(k, self.waypointList[k])
       
        # Generate waypoint file for Mission Planner
        # TODO: Verify home & waypoint file format
        makeWaypointFile(self.waypointList, self.coordList)
        

############################################################################################################################

#myReader = csv.reader(open('LatLon.csv', newline=''), delimiter=',')
                                      

'''
for row in myReader:
    coordList.append([float(row[0]), float(row[1])])
'''

'''Now we're going to generate a KMZ'''
# Remove existing UAVConcordiaTask3 directory, if it exists
try:
    shutil.rmtree("UAVConcordiaTask3")
except:
    pass

# Create a new UAVConcordiaTask3 directory with
# a files subfolder 
os.makedirs("UAVConcordiaTask3/files")

# These are "constants" used for indexing into waypointList
LAT = 0
LON = 1

# Fill folder with placemarks corresponding to evidence objects from waypointList
placemarkList = []
k = 0
while k < len(waypointList): 
    waypointLabel = input("Evidence " + str(k) + " at " + str(waypointList[k]) + " = ")
    if waypointLabel == "edit":
        if k > 0:
            k -= 1   
            placemarkList = placemarkList[:-1]
            continue
        elif k == 0:
            print("ERROR: You can't do that")
            continue
    pml = KML.Placemark(KML.name("Evidence ", k), KML.description(waypointLabel), KML.Point(KML.coordinates(str(waypointList[k][LAT]), "," ,str(waypointList[k][LON]))))
    placemarkList.append(pml)
    k += 1

# Make a folder for the placemarks
fld = KML.Folder()
for k in range(len(placemarkList)):
    fld.append(placemarkList[k])
    
# Generate KML document
doc = KML.kml(fld)

# tostring outputs a byte sequence
docBytes = etree.tostring(doc, pretty_print=True)

# Convert bytes to string and print 
print(docBytes.decode("utf-8"))

# Read KML schema for validation
schema_ogc = Schema("ogckml22.xsd")
schema_gx = Schema("kml22gx.xsd")

# Print validation results
print(schema_ogc.validate(doc))
print(schema_gx.validate(doc))

# Create folder for basis of KMZ file
kmlOutput = "UAVConcordiaTask3/UAVConcordia_Task3.kml"
f = open(kmlOutput, 'w')

# Write KML document to file
f.write(docBytes.decode("utf-8"))

# Close file
f.close()

# Zip the folder to create a KMZ
shutil.make_archive('UAVConcordiaTask3', 'zip', 'UAVConcordiaTask3')

# Change extension from .zip to .kmz
os.rename('UAVConcordiaTask3.zip', 'UAVConcordiaTask3.kmz')


      



      
