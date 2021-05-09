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

'''Now we're going to generate a KMZ'''
# These are "constants" used for indexing into waypointList
LAT = 0
LON = 1

class MakeKMZ:
    def __init__(self, coordindateList):
        self.waypointList = coordindateList
        self.placemarkList = []
        self.waypointLabel = None
    def writeFile(self):
        # Remove existing UAVConcordiaTask3 directory, if it exists
        try:
            shutil.rmtree("UAVConcordiaTask3")
        except:
            pass
        
        # Create a new UAVConcordiaTask3 directory with
        # a files subfolder 
        os.makedirs("UAVConcordiaTask3/files")
        
        # Fill folder with placemarks corresponding to evidence objects from waypointList
        self.placemarkList = []
        k = 0
        while k < len(self.waypointList): 
            pml = KML.Placemark(KML.name("Evidence ", k), KML.Point(KML.coordinates(str(self.waypointList[k][LAT]), "," , str(self.waypointList[k][LON]))))
            self.placemarkList.append(pml)
            k += 1
        
        # Make a folder for the placemarks
        fld = KML.Folder()
        for k in range(len(self.placemarkList)):
            fld.append(self.placemarkList[k])
            
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


      
