# this file will be the main loop of the program, it will have the GUI and the functions linkback.
import os
from file_to_stl import *
from tkinter import *

file_path = "C:/Users/lars/Desktop/Design_Tech_2024/Design_Tech_2024/Fritzing/Temp testing/ProcessingRGB_copperBottom.gbl"
scale = 500
trace_resolution = 1 # this is the number of points in the end cap circles of the traces
circle_resolution = 4 # this is the number of points in a cirlce cannot be below 3 and must be even.
height = 10
testing = stl_creator(file_path, "ProcessingRGB_copperBottom.gbl", scale, trace_resolution, circle_resolution, height)     


# now gerber_layers is a dict with split layers that can be used to turn the layers into independant images.

print(gerber_layers)