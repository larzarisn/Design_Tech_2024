import numpy as np
import re
import math
import stl
from file_to_stl import return_flash_coordinates
from file_to_stl import return_line_coordinates
from file_to_stl import mesh_list_combiner
from file_to_stl import triangle_solver

def shape_intersection_finder(shape1, shape2):
    for vertice1 in shape1:
        for vertice3 in shape2:
            balls

def shape_combiner(shape1, shape2):
    print("hi")

# This function sorts through the shapes, removes and fixes lines that intersect and generates 4 numpy arrays for:
# The trace index connections array which is
# The trace vertex array
# The negative index connections array
# The negative vertex array

# NOTES:
# Check the first one, if it finds an intersection combine the shapes then go back and check the new combined shape until there are no intersections left

def shape_sorter(shape_list):
    combined_list = []
    temp_shape_list = shape_list
    while True:
        no_intersects = False
        while not no_intersects:
            combined_shape = temp_shape_list[0]
            temp_shape_list.pop(0)
            for i, shape in enumerate(temp_shape_list):
                if shape_intersection_finder(shape, shape_list[0]) == False:
                    combined_shape = shape_combiner(shape_list[0], shape)
                    temp_shape_list.pop(i)
                    break
        combined_list.append(combined_shape)            

# this is the main loop with everything in it, it calls all the other functions in this.
def stl_creator(gerber_file_path, gerber_file_name, scale_factor, num_circle_points, num_flash_points, layer_height):
    # getting variables ready
    print(gerber_file_path)
    gerber_file_extensionless = gerber_file_name.partition(".")[0]
    gerber_file = open(gerber_file_path, "r")   
    instruction_array = gerber_file.readlines()
    aperture_instruction_dict = {}
    instruction_string = "".join(instruction_array)
    aperture_list = re.findall("ADD([0-9][0-9])(.*)?/*%", instruction_string) 
    scale = int(re.findall("FSLAX[1-6]([1-9])Y", instruction_string)[0])
    current_aperture = "NaN" 
    last_x_coord = 0 # setting this for later because of weird for loop behavior.
    last_y_coord = 0
    mesh_list = []
    shape_list = []
    # Finds and puts into a dictionary all of the apertures (or tools/shapes) that will be used
    for aperture in aperture_list:
        aperture_instruction_dict[aperture[0]] = aperture[1].split(",") # makes an aperture with the shape information and the size information
    
    # This is the main loop for interpreting the gerber files into a format that can be turned into a mesh
    # It gets the instructions and outputs into a list of shapes that need to be rendered
    # The output is in the form [[shape1], [shape2]....] where [shape1] is a list of points with an index specifying which point they connect to next
    for instruction in instruction_array:
        if re.match(".*D([1-9][0-9]).*", instruction):
            current_aperture = re.findall(".*D([1-9][0-9]).*", instruction)[0] # This gives the number of the current aperture: that can be fed into the known dict to get the width and the shape

        if instruction.startswith("X"):
            to_x_coord = float(re.findall("X(.*)Y", instruction)[0])*pow(10, -1*scale)*scale_factor
            to_y_coord = float(re.findall("Y(.*)D", instruction)[0])*pow(10, -1*scale)*scale_factor
            current_width = float(aperture_instruction_dict[current_aperture][1].replace("*", ""))*scale_factor

            if re.match(".*D01.*", instruction):
                line_edge_array = return_line_coordinates(to_x_coord, to_y_coord, last_x_coord, last_y_coord, current_width, num_circle_points)
                for i, vertex in enumerate(line_edge_array):
                    next_vertex_index = i+1
                    if next_vertex_index >= len(line_edge_array):
                        next_vertex_index = 0
                    verticies_with_pointer.append([next_vertex_index, vertex])
                shape_list.append(verticies_with_pointer)
                # mesh_list.append(triangle_solver(line_edge_array, layer_height))

            if re.match(".*D03.*", instruction): # This needs to move to a point, create a single aperture point and stop. (ie it makes a circle with the apertures width)
                line_edge_array = return_flash_coordinates(to_x_coord, to_y_coord, current_width, num_flash_points)
                verticies_with_pointer = []
                for i, vertex in enumerate(line_edge_array):
                    next_vertex_index = i+1
                    if next_vertex_index >= len(line_edge_array):
                        next_vertex_index = 0
                    verticies_with_pointer.append([next_vertex_index, vertex])
                shape_list.append(verticies_with_pointer)
                # mesh_list.append(triangle_solver(line_edge_array, layer_height))

            # This tells the drawline function where the last known coordinates were
            last_x_coord = to_x_coord 
            last_y_coord = to_y_coord 
    # vertices, faces = mesh_list_combiner(mesh_list)
    





    # Goes through shapes and checks if they intersect, if they do then it combines their verticies into one larger list
    # for i, shape in enumerate(shape_list):
    #     print(i)
    #     for ii, check_shape in enumerate(shape_list):
    #         if shape_intersection_checker(shape, check_shape):
    #             return
    #         else:

        
    print(shape_list)

    # gerber_3d_model = stl.mesh.Mesh(np.zeros(faces.shape[0], dtype=stl.mesh.Mesh.dtype))
    # for i, f in enumerate(faces):
    #     for j in range(3):
    #         gerber_3d_model.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file
    print(f'./{gerber_file_extensionless}.stl')
    # gerber_3d_model.save(f'./Output 3D models/{gerber_file_extensionless}.stl')
    return "testing123"
file_path = "./Example gerber files/ProcessingRGB_copperBottom.gbl"
scale = 500
trace_resolution = 1 # this is the number of points in the end cap circles of the traces
circle_resolution = 4 # this is the number of points in a cirlce cannot be below 3 and must be even.
height = 10
stl_creator(file_path, file_path.split("/")[-1], scale, trace_resolution, circle_resolution, height)
