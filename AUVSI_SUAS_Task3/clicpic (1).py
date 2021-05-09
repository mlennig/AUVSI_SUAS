import tkinter as tk
from PIL import Image, ImageTk
import glob
import os
from tkinter import messagebox
from RPi_image_processing import RPi_ImageProcessing
from get_lat_lon_exif_pil import ImageMetaData
from rotateCoordinates import Rotgrid

image_processor = RPi_ImageProcessing('Images')

# TODO: get heading of drone 
# TODO: Make sure heading of camera matches heading drone 
# TODO: Rotate images so that up is North: rotate heading * (-1)
# TODO: Get lat, lon, alt 

class Clicpic:
    def __init__(self, unprocessedPath, processedPath):
        self.x = None       # The x position of the click in pixels
        self.y = None       # The y position of the click in pixels
        self.frame = None   # The graphical frame that the picture appears in 
        self.canvas = None  # The graphical canvas that the picture appears in 
        self.root = tk.Tk() # This is the root of the graphical view tree 
        self.imageWidthPixels = None
        self.imageHeightPixels = None
        self.clickLat = None
        self.clickLon = None
        self.unprocessedPathname = unprocessedPath
        self.processedPathname = processedPath
        self.imageName = None
        self.imageSkipped = False

    # Function to be called when mouse is clicked
    def clickLeftAction(self, event):
        self.canvas = event.widget                # Get the canvas object that was clicked on
        self.imageSkipped = False
        
        if messagebox.askyesno("DON'T FUCK THIS UP!!!", "Commit that click?", default = "no"):
            self.x = self.canvas.canvasx(event.x)     # Convert window x-coordinate to canvas (pixel) x-coordinate
            self.y = self.canvas.canvasy(event.y)     # Convert window y-coordinate to canvas (pixel) y-coordinate 
            # Move processed image to processed image folder
            os.rename(self.unprocessedPathname + self.imageName, self.processedPathname + self.imageName)
            # Now that we know the pixel coordinates (x,y) of the mouse click, we should do something with it
            # and then close the image. We are only collecting one (x,y) per image.
            self.canvas.delete(tk.ALL)
            self.root.quit()
            
    def scrollAction(self, event):
        self.canvas = event.widget                # Get the canvas object that was clicked on
        if messagebox.askyesno("Skip", "Skip this image?", default = "no"):
            # Move processed image to processed image folder
            os.rename(self.unprocessedPathname + self.imageName, self.processedPathname + self.imageName)
            self.imageSkipped = True
            self.canvas.delete(tk.ALL)
            self.root.quit()
        else:
            self.imageSkipped = False
    
    # Open an image file, put it in a frame on a canvas and make it click-sensitive. 
    def clic2picXY(self, imageFile2open : str):
        self.imageName = imageFile2open
        
        # Setting up a tkinter canvas with scrollbars
        if not self.frame:
            # No frame has been created yet
            self.frame = tk.Frame(self.root, bd = 2, relief = tk.SUNKEN)
            self.frame.grid_rowconfigure(0, weight = 1)
            self.frame.grid_columnconfigure(0, weight = 1)
            
        xscroll = tk.Scrollbar(self.frame, orient = tk.HORIZONTAL)
        xscroll.grid(row = 1, column = 0, sticky = tk.E + tk.W)
        yscroll = tk.Scrollbar(self.frame)
        yscroll.grid(row = 0, column = 1, sticky = tk.N + tk.S)
        
        # Set dimensions of canvas here 
        # TODO: If time, look into displaying a down-sampled image 
        canvas = tk.Canvas(self.frame, bd = 0, width = 600, height = 900, xscrollcommand = xscroll.set, yscrollcommand = yscroll.set)
        canvas.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.E + tk.W)
        xscroll.config(command = canvas.xview)
        yscroll.config(command = canvas.yview)
        self.frame.pack(fill = tk.BOTH, expand = 1)       
        
        # Add the image to the canvas 
        myImage = Image.open(self.unprocessedPathname + imageFile2open)
        
        '''
        (newWidth, newHeight) = myImage.size
        newWidth = int(newWidth / 4)
        newHeight = int(newHeight / 4)
        
        myImage = myImage.resize((newWidth, newHeight))
        '''
        
        img = ImageTk.PhotoImage(myImage)                       # Modify string to be an image file name
        canvas.create_image(0, 0, image = img, anchor = "nw")   # Set upper lefthand corner as (0,0)
        canvas.config(scrollregion = canvas.bbox(tk.ALL))
        
        # Bind mouseclick event to the clickAction callback
        # Button 1 is the left button on the mouse
        canvas.bind("<Button-1>", self.clickLeftAction)
        # Button 3 is right button on the mouse
        canvas.bind("<MouseWheel>", self.scrollAction)
        
        # Print picture dimensions to console
        print('Image dimenisons -- width:', img.width(), "   height:", img.height())
        
        self.root.mainloop()
        
        if not self.imageSkipped:
            # Save image dimensions in pixels
            self.imageWidthPixels = img.width()
            self.imageHeightPixels = img.height()
            
            # Calculate image scale
            exifData = ImageMetaData(self.processedPathname + imageFile2open)
            #altitude = exifData.getAltitude()
            altitude = 260 * 0.3048 
            imageWidthMeters, imageHeightMeters = image_processor.calculate_image_scale(altitude)
            
            # Calculates the displacement in meters from center based on (x,y) pixel placement
            dx, dy = image_processor.calculate_displacement(self.x, self.y, self.imageWidthPixels, self.imageHeightPixels, imageWidthMeters, imageHeightMeters)
            
            # Calculate gps position of clicked object
            imageLat, imageLon = exifData.get_lat_lng()
            print("Image latitude = ", imageLat, "Image longitude = ", imageLon)
            self.clickLat, self.clickLon = image_processor.calculate_gps_position(imageLat, imageLon, dx, dy)
            
            # TODO: Rotate images so that up is North: rotate heading * (-1)
            '''
            heading = 135        
            
            rotateCoordinates = Rotgrid(imageLat, imageLon, polerotate = 0, nPoleGridLon= -heading, lonMin = -180.)
            (lonrot, latrot) = rotateCoordinates.transform(self.clickLat, self.clickLon)
            #(lon2, lat2) = rotateCoordinates.transform(lonrot, latrot, inverse = True)
            '''
            
            return self.clickLat, self.clickLon
        
        else:
            return None, None

