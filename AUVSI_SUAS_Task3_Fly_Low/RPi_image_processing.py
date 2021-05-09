import math
from PIL import Image
from clicpic import Clicpic
import os
import glob

class RPi_ImageProcessing:
    def __init__(self, images_dir: str):
        # Member variables (object properties)
        self.sensor_length_x: float = 4.5 / 1000    # TODO: change to RPi camera module V2 sensor dimensions 3.68 x 2.76 mm
        self.sensor_length_y: float = 6.2 / 1000
        self.focal_length: float = 28.0 / 1000      # TODO: change to RPi camera module V2 focal length 3.04 mm, focal length of lens is 2.1
        self.images_dir = images_dir
        
        self.current_image: Image = None
        self.current_x_len = None
        self.current_y_len = None

    def process_directory(self):
        # TODO: Access self.images_dir and process_image on every image in the directory
        return None

    def process_image(self, file_path: str):
        # TODO: Process a single image
            # TODO: Read image - Image.open(file_path)
            # TODO: calculate_image_scale
            # TODO: Find custom color pixel identifying object in image
            # TODO: calculate_displacement based on pixels position in image
        return None

    def calculate_image_scale(self, altitude: float) -> (float, float):
        """
        Calculate scale of x and y axis of image based on camera parameters and altitude. Produces a tuple of dimensions

        :param altitude: height in meters
        :return: (width, height)
        """
        # width, height are dimensions of the area in the picture, in meters
        width = altitude / self.focal_length * self.sensor_length_x
        height = altitude / self.focal_length * self.sensor_length_y

        return width, height

    def calculate_gps_position(self, lat: float, long: float, dx: float, dy: float) -> (float, float):
        """
        Calculate new GPS latitude and longitude based on a displacement of dx and dy meters

        :param lat: Initial latitude
        :param long: Initial longitude
        :param dx: displacement in X
        :param dy: displacement in Y
        :return: (new_latitude, new_longitude)
        """
        r_earth: float = 6371.0 * 1000

        new_latitude: float = lat + (dy / r_earth) * (180 / math.pi)
        new_longitude: float = long + (dx / r_earth) * (180 / math.pi) / math.cos(lat * math.pi / 180)

        return new_latitude, new_longitude

    def calculate_displacement(self, x, y) -> (float, float):
        """
        Calculates the displacement in meters from center based on (x,y) pixel placement

        :param x: x pixel position
        :param y: y pixel position
        :return: (dx, dy)
        """
        # Width, height are the pixel dimensions of the image 
        width, height = self.current_image.size
        
        """(x - the midpoint (of width)) * the distance per pixel value"""
        # self.current_x_len, self.current_y_len are the dimensions of the area
        # in the picture, in meters         
        dx = (x - width / 2) * (self.current_x_len / width)
        dy = (y - height / 2) * (self.current_y_len / height)

        return dx, dy


