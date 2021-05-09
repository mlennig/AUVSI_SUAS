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
import math

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
    
    # pointA is the center lat lon, pointB is the click point lat lon
    def calculate_initial_compass_bearing(self, pointA, pointB):
        """
        Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),
                      cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
        :Parameters:
          - `pointA: The tuple representing the latitude/longitude for the
            first point. Latitude and longitude must be in decimal degrees
          - `pointB: The tuple representing the latitude/longitude for the
            second point. Latitude and longitude must be in decimal degrees
        :Returns:
          The bearing in degrees
        :Returns Type:
          float
        """
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")
    
        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])
    
        diffLong = math.radians(pointB[1] - pointA[1])
    
        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))
    
        initial_bearing = math.atan2(x, y)
    
        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
    
        return compass_bearing
    
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


      
