import os
import index
import cairo
import re
import math

# draw_line function turns one line into two to make it parsable by parametric editing software.
def draw_line(x_coord, y_coord, start_x_coord, start_y_coord, current_width, cairo_context): 
    # making function to calculate the outline of the main traces to work with freeCAD.
    # to make this I will make an x/y offset and move the aperture by that much
    # this offset requires a calculation of the hypotonuse/length of the line as well as the distance that the aperture moves in both x and y.
    delta_x = x_coord - start_x_coord
    delta_y = y_coord - start_y_coord
    # using pythag for the length:
    segment_length = math.hypot(delta_x, delta_y)
    # this is scuffed but should work, using trig tomfoolery:
    x_offset = (0.5*delta_y*current_width)/segment_length
    y_offset = (0.5*delta_x*current_width)/segment_length
    # this works by making a triangle out of the main line segment and equating it to the sin/cos of the offset triangle.
    # now these offsets can be used to draw two lines instead of one.
    for i in [-1, 1]: # this means that i can be either -1, or 1 allowing to create two lines with either a positive or a negative offset.

        x_starting_position = start_x_coord + i*x_offset 
        y_starting_position = start_y_coord + i*y_offset
        
        x_ending_position = x_coord + i*x_offset
        y_ending_position = y_coord + i*y_offset

        cairo_context.move_to(x_starting_position, y_starting_position) # move to starting point
        cairo_context.line_to(x_ending_position, y_ending_position) # and draw
        print(f"going from current coordinates: y: {y_starting_position} x: {x_starting_position} to y: {y_ending_position} x: {x_ending_position}  with width of {cairo_context.get_line_width()}")
        print(delta_x)

def vector_creator(gerber_file_path, gerber_file_name, settings):
    gerber_file_extensionless = gerber_file_name.partition(".")[0]
    print(f"./Vectors/{gerber_file_extensionless}.svg")
    with cairo.SVGSurface(f"./Vectors/{gerber_file_extensionless}.svg", 700, 700) as svg_layer: 
        # user variables to be set
        vector_scale_factor = 10
        # getting variables ready
        cairo_context = cairo.Context(svg_layer)
        gerber_file = open(gerber_file_path, "r")   
        instruction_array = gerber_file.readlines()
        aperture_instruction_dict = {}
        instruction_string = "".join(instruction_array)
        aperture_list = re.findall("ADD([0-9][0-9])(.*)?\*%", instruction_string) 
        scale = int(re.findall("FSLAX[1-6]([1-9])Y", instruction_string)[0])
        current_aperture = "NaN" 
        last_x_coord = 0 # setting this for later because of weird for loop behavior.
        last_y_coord = 0

        for aperture in aperture_list:
            aperture_instruction_dict[aperture[0]] = aperture[1].split(",") # makes an aperture with the shape information and the size information
        for instruction in instruction_array:
            if re.match(".*D([1-9][0-9]).*", instruction):
                print("stroke!")
                current_aperture = re.findall(".*D([1-9][0-9]).*", instruction)[0] # This gives the number of the current aperture: that can be fed into the known dict to get the width and the shape
                cairo_context.stroke() # outputting each line/shape here onto the canvas
 
            if instruction.startswith("X"):
                cairo_context.set_line_width(float(aperture_instruction_dict[current_aperture][1])*vector_scale_factor) 
                cairo_context.set_line_cap(1)
                cairo_context.set_source_rgba(0, 0, 1, 1)
                to_x_coord = float(re.findall("X(.*)Y", instruction)[0])*pow(10, -1*scale)*vector_scale_factor
                to_y_coord = float(re.findall("Y(.*)D", instruction)[0])*pow(10, -1*scale)*vector_scale_factor
                print(f"current coordinates: y: {to_y_coord} x: {to_x_coord}  using aperture {current_aperture} with width of {cairo_context.get_line_width()}")

                if re.match(".*D01.*", instruction):
                    # cairo_context.line_to(to_x_coord, to_y_coord)
                    draw_line(to_x_coord, to_y_coord, last_x_coord, last_y_coord, cairo_context.get_line_width(), cairo_context)
                if re.match(".*D02.*", instruction):
                    cairo_context.move_to(to_x_coord, to_y_coord)

                if re.match(".*D03.*", instruction): # This needs to move to a point, create a single aperture point and stop. (ie it makes a circle with the apertures width)
                    cairo_context.move_to(to_x_coord, to_y_coord) 
                    cairo_context.line_to(to_x_coord, to_y_coord)
                    # LOOK INTO pycairos PATTERNS FOR THIS
                # This tells the drawline function where the last known coord was and is useful to make the D03 work properly later.
                last_x_coord = to_x_coord 
                last_y_coord = to_y_coord 
        cairo_context.stroke()
    return "balls"

