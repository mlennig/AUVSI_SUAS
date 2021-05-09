from RPi_image_processing import RPi_ImageProcessing
import clicpic
import glob
import os
import math
from PIL import Image
from clicpic import Clicpic

image_processor: RPi_ImageProcessing = RPi_ImageProcessing('Images')

# Test Area
width, height = image_processor.calculate_image_scale(100)
print("X: %f\nY: %f\nA: %f\n" % (width, height, width * height))

# Test GPS calculation
new_lat, new_long = image_processor.calculate_gps_position(41.30414, -81.75271, 10, 5)
print("Lat: %f\nLong: %f\n" % (new_lat, new_long))

pathname = "/Users/miriamlennig/src/USC2018/click_pic/Images/"
# Navigate to Image directory
os.chdir(pathname)
myClicpic = Clicpic()

# Can change extension of images here
for filename in glob.glob("*"):
    print("\n", pathname + filename)
    x, y = myClicpic.clic2picXY(pathname + filename)
    print ("Pixel coordinates of click are x = :", x, "    y = ", y)