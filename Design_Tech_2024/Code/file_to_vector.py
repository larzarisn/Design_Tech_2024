import os
import cairo
import re
import math

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
    # this is scuffed but should work, using trig tomfoolery:
    x_offset = (0.5*delta_y*current_width)/segment_length
    y_offset = (0.5*delta_x*current_width)/segment_length
    # this works by making a triangle out of the main line segment and equating it to the sin/cos of the offset triangle.
    # now these offsets can be used to draw two lines instead of one.

    positive_x_starting_position = start_x_coord + x_offset 
    positive_y_starting_position = start_y_coord - y_offset
    
    positive_x_ending_position = x_coord + x_offset
    positive_y_ending_position = y_coord - y_offset

    negative_x_starting_position = start_x_coord - x_offset 
    negative_y_starting_position = start_y_coord + y_offset
    
    negative_x_ending_position = x_coord - x_offset
    negative_y_ending_position = y_coord + y_offset

    # returning points in touple form to make it easier to identify x,y.
    return [[positive_x_starting_position, positive_y_starting_position], [positive_x_ending_position, positive_y_ending_position], [negative_x_starting_position, negative_y_starting_position], [negative_x_ending_position, negative_y_ending_position]] 

# draws the trace from start to finish, capping off the end.
def draw_trace(point_dict, cairo_context):

    if len(point_dict["positive"]) == 0: # Checking if there's actually anything in the list
        return

    cairo_context.set_line_width(1) 
    cairo_context.set_source_rgba(0, 1, 1, 1)
    # Turning the edge coordinates into a list of commands to run through.
    point_list = []
    print(point_dict["negative"])
    print(list(reversed(point_dict["negative"])))
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
        trace_edge_dict = {"positive":[], "negative":[]} # Stores the line start and end locations for each part of the line post offset.
        last_points = []

        for aperture in aperture_list:
            aperture_instruction_dict[aperture[0]] = aperture[1].split(",") # makes an aperture with the shape information and the size information
        for instruction in instruction_array:
            if re.match(".*D([1-9][0-9]).*", instruction):
                #print("stroke!")
                current_aperture = re.findall(".*D([1-9][0-9]).*", instruction)[0] # This gives the number of the current aperture: that can be fed into the known dict to get the width and the shape
                cairo_context.stroke() # outputting each line/shape here onto the canvas
 
            if instruction.startswith("X"):

                # setting up the svg
                cairo_context.set_line_width(float(aperture_instruction_dict[current_aperture][1].replace("*", ""))*vector_scale_factor) 
                cairo_context.set_source_rgba(0, 0, 1, 1)
                cairo_context.set_line_cap(1)
                to_x_coord = float(re.findall("X(.*)Y", instruction)[0])*pow(10, -1*scale)*vector_scale_factor
                to_y_coord = float(re.findall("Y(.*)D", instruction)[0])*pow(10, -1*scale)*vector_scale_factor

                # Last points is used to try and match lines together.
                if len(last_points) <= 3:
                    last_points.append([to_x_coord, to_y_coord])
                else: 
                    last_points.pop(0)
                    last_points.append([to_x_coord, to_y_coord])

                if re.match(".*D01.*", instruction): # This is the draw instruction
                    # Instead of actually drawing in this step, the coordinates of the edges of the line are saved so that the line can be made in one batch later.
                    
                    # This checks if the line that is being drawn meets the last (or one of the last lines) to be drawn
                    lines_meet_boolean = False
                    for point in last_points[0:3]:
                        if to_x_coord == point[0] and to_y_coord == point[1]:
                            lines_meet_boolean = True
                    # If it is false it traces out the line
                    if not lines_meet_boolean:
                        draw_trace(trace_edge_dict, cairo_context)
                        trace_edge_dict = {"positive":[], "negative":[]} # resets the edge coordinates for new trace
                        line_edge_array = return_line_coordinates(last_points[-2][0], last_points[-2][1], to_x_coord, to_y_coord, float(aperture_instruction_dict[current_aperture][1].replace("*", ""))*vector_scale_factor)
                        # line_edge_array = return_line_coordinates(to_x_coord, to_y_coord, last_points[-2][0], last_points[-2][1], float(aperture_instruction_dict[current_aperture][1].replace("*", ""))*vector_scale_factor)
                        for positive_edge_coordinates in line_edge_array[0: 2]:
                            trace_edge_dict["positive"].append(positive_edge_coordinates)
                        for negative_edge_coordinates in line_edge_array[2: 4]:
                            trace_edge_dict["negative"].append(negative_edge_coordinates)
                    else:
                        line_edge_array = return_line_coordinates(last_points[-2][0], last_points[-2][1], to_x_coord, to_y_coord, float(aperture_instruction_dict[current_aperture][1].replace("*", ""))*vector_scale_factor)
                        for positive_edge_coordinates in line_edge_array[0: 2]:
                            trace_edge_dict["positive"].append(positive_edge_coordinates)
                        for negative_edge_coordinates in line_edge_array[2: 4]:
                            trace_edge_dict["negative"].append(negative_edge_coordinates)
                    #cairo_context.set_source_rgba(0, 1, 0, 1)
                    #cairo_context.line_to(to_x_coord, to_y_coord)
                if re.match(".*D02.*", instruction):
                    # draw_trace(trace_edge_dict, cairo_context)
                    # trace_edge_dict = {"positive":[], "negative":[]} # resets the edge coordinates for new trace
                    cairo_context.move_to(to_x_coord, to_y_coord)

                if re.match(".*D03.*", instruction): # This needs to move to a point, create a single aperture point and stop. (ie it makes a circle with the apertures width)
                    # draw_trace(trace_edge_dict, cairo_context)
                    # trace_edge_dict = {"positive":[], "negative":[]} # resets the edge coordinates for new trace
                    cairo_context.move_to(to_x_coord, to_y_coord) 
                    cairo_context.line_to(to_x_coord, to_y_coord)
                    # LOOK INTO pycairos PATTERNS FOR THIS
        draw_trace(trace_edge_dict, cairo_context)
        cairo_context.stroke()
    return "testing123"

