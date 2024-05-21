import os
import cairo
import re
import math

# this function finds the x and y coordinates for a circle around the the end points.
def return_circle_coordinates(delta_x, delta_y, width, segment_length, x, y, t):
    
    circle_x_coordinate = (width*(delta_y*math.cos(t)-delta_x*math.sin(t)))/(2*segment_length)+x
    
    circle_y_coordinate = (width*(delta_y*math.sin(t)+delta_x*math.cos(t)))/(2*segment_length)+y

    return [circle_x_coordinate, circle_y_coordinate]


# return_line_coordinates takes the current trace and returns the coordinates of its edges.
# This is useful to make the traces continuous because otherwise there would be gaps in traces for each time a new coordinate is given.
def return_line_coordinates(x_coord, y_coord, start_x_coord, start_y_coord, current_width): 
    # making function to calculate the outline of the main traces to work with freeCAD.
    # to make this I will make an x/y offset and move the aperture by that much
    # this offset requires a calculation of the hypotonuse/length of the line as well as the distance that the aperture moves in both x and y.
    delta_x = x_coord - start_x_coord
    delta_y = y_coord - start_y_coord
    # using pythag for the length:
    segment_length = math.hypot(delta_x, delta_y)

    positive_starting_position = return_circle_coordinates(delta_x, -delta_y, current_width, segment_length, start_x_coord, start_y_coord, math.pi)

    negative_starting_position = return_circle_coordinates(delta_x, -delta_y, current_width, segment_length, start_x_coord, start_y_coord, 0)

    positive_ending_position = return_circle_coordinates(-delta_x, delta_y, current_width, segment_length, x_coord, y_coord, 0)
    
    negative_ending_position = return_circle_coordinates(-delta_x, delta_y, current_width, segment_length, x_coord, y_coord, math.pi)

    # returning points in touple form to make it easier to identify x,y.
    return [positive_starting_position, positive_ending_position, negative_starting_position, negative_ending_position] 

# draws the trace from start to finish, capping off the end.
def draw_trace(point_dict, cairo_context):

    if len(point_dict["positive"]) == 0: # Checking if there's actually anything in the list
        return

    cairo_context.set_line_width(1) 
    cairo_context.set_source_rgba(0, 1, 1, 1)
    # Turning the edge coordinates into a list of commands to run through.
    point_list = []
    for point in point_dict["positive"]:
        point_list.append(point)
    for point in list(reversed(point_dict["negative"])):
        point_list.append(point)    
    # Running through the commands
    cairo_context.move_to(point_list[0][0], point_list[0][1])
    for point in point_list: 
        cairo_context.line_to(point[0], point[1])
    cairo_context.line_to(point_list[0][0], point_list[0][1])
    cairo_context.stroke()

def vector_creator(gerber_file_path, gerber_file_name, settings):
    gerber_file_extensionless = gerber_file_name.partition(".")[0]
    # print(f"./Design_Tech_2024/Vectors/{gerber_file_extensionless}.svg")
    with cairo.SVGSurface(f"./Design_Tech_2024/Vectors/{gerber_file_extensionless}.svg", 1500, 1500) as svg_layer: 
        # user variables to be set
        vector_scale_factor = 500
        # getting variables ready
        cairo_context = cairo.Context(svg_layer)
        gerber_file = open(gerber_file_path, "r")   
        instruction_array = gerber_file.readlines()
        aperture_instruction_dict = {}
        instruction_string = "".join(instruction_array)
        aperture_list = re.findall("ADD([0-9][0-9])(.*)?/*%", instruction_string) 
        scale = int(re.findall("FSLAX[1-6]([1-9])Y", instruction_string)[0])
        current_aperture = "NaN" 
        last_x_coord = 0 # setting this for later because of weird for loop behavior.
        last_y_coord = 0
        trace_edge_dict = {"positive":[], "negative":[]} # Stores the line start and end locations for each part of the line post offset.

        for aperture in aperture_list:
            aperture_instruction_dict[aperture[0]] = aperture[1].split(",") # makes an aperture with the shape information and the size information
        for instruction in instruction_array:
            if re.match(".*D([1-9][0-9]).*", instruction):
                #print("stroke!")
                current_aperture = re.findall(".*D([1-9][0-9]).*", instruction)[0] # This gives the number of the current aperture: that can be fed into the known dict to get the width and the shape
                cairo_context.stroke() # outputting each line/shape here onto the canvas
 
            if instruction.startswith("X"):
                cairo_context.set_line_width(float(aperture_instruction_dict[current_aperture][1].replace("*", ""))*vector_scale_factor) 
                cairo_context.set_source_rgba(0, 0, 1, 1)
                cairo_context.set_line_cap(1)
                to_x_coord = float(re.findall("X(.*)Y", instruction)[0])*pow(10, -1*scale)*vector_scale_factor
                to_y_coord = float(re.findall("Y(.*)D", instruction)[0])*pow(10, -1*scale)*vector_scale_factor
                #print(f"current coordinates: y: {to_y_coord} x: {to_x_coord}  using aperture {current_aperture} with width of {cairo_context.get_line_width()}")

                if re.match(".*D01.*", instruction):
                    line_edge_array = return_line_coordinates(to_x_coord, to_y_coord, last_x_coord, last_y_coord, cairo_context.get_line_width())
                    for positive_edge_coordinates in line_edge_array[0: 2]:
                        trace_edge_dict["positive"].append(positive_edge_coordinates)
                    for negative_edge_coordinates in line_edge_array[2: 4]:
                        trace_edge_dict["negative"].append(negative_edge_coordinates)
                    cairo_context.set_source_rgba(0, 1, 0, 1)
                    # cairo_context.line_to(to_x_coord, to_y_coord)
                    
                if re.match(".*D02.*", instruction):
                    draw_trace(trace_edge_dict, cairo_context)
                    trace_edge_dict = {"positive":[], "negative":[]} # resets the edge coordinates for new trace
                    cairo_context.move_to(to_x_coord, to_y_coord)

                if re.match(".*D03.*", instruction): # This needs to move to a point, create a single aperture point and stop. (ie it makes a circle with the apertures width)
                    draw_trace(trace_edge_dict, cairo_context)
                    trace_edge_dict = {"positive":[], "negative":[]} # resets the edge coordinates for new trace
                    cairo_context.move_to(to_x_coord, to_y_coord) 
                    cairo_context.line_to(to_x_coord, to_y_coord)
                    # LOOK INTO pycairos PATTERNS FOR THIS
                # This tells the drawline function where the last known coord was and is useful to make the D03 work properly later.
                last_x_coord = to_x_coord 
                last_y_coord = to_y_coord 
        draw_trace(trace_edge_dict, cairo_context)
        cairo_context.stroke()
    return "testing123"
