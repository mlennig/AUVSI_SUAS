''' This is the main module for FlyHigh '''
import glob
import os
from clicpic import Clicpic
from USC_ComputeRoute import ComputeGreedyRoute
from GenerateKMZ import MakeKMZ

# Point to directory of Images
unprocessed_path = "/Users/miriamlennig/src/USC2018/Task3FlyHigh/Images/"
processed_path = "/Users/miriamlennig/src/USC2018/Task3FlyHigh/ProcessedImages/"
os.chdir(unprocessed_path)

answer = "NO"

myClicpic = Clicpic(unprocessed_path, processed_path)

objectCoordinates = []

while answer != "YES":
    imageFilenameList = glob.glob("*")
    
    if len(imageFilenameList) > 0:
        for filename in imageFilenameList:
            print("\n", unprocessed_path + filename)
            lat, lon = myClicpic.clic2picXY(filename)
            if lat != None and lon != None:
                objectCoordinates.append([lat,lon])
                print("Object Latitude = ", lat, "Object Longitude = ", lon)
                print(objectCoordinates)
    else:
        answer = input("Ready to make KMZ (YES)? ")
        
greedyRoute = ComputeGreedyRoute(objectCoordinates)
writeKMZFile = MakeKMZ(objectCoordinates)

greedyRoute.makeWaypointFile()
writeKMZFile.writeFile()


            
    