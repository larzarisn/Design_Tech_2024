import re
import math
import numpy as np
import stl

# this function takes the list of all of the traces and shapes
# and returns a touple with two combined numpy arrays
# which should return the mesh coordinates and faces for the entire Gerber file
def mesh_list_combiner(mesh_list):
    return_coordinates_array = mesh_list[0][1]
    return_faces_array = mesh_list[0][0]
    current_index_offset = return_coordinates_array.shape[0]

    for mesh in mesh_list[0:]:
        return_coordinates_array = np.append(return_coordinates_array, mesh[1], axis=0)
        # this adds the current index of everything to all of the triangle connection values as all coordinates have been moved by that much
        return_faces_array = np.append(return_faces_array, np.add(mesh[0], current_index_offset), axis=0) 
        # print(np.add(mesh[0], current_index_offset))
        current_index_offset = return_coordinates_array.shape[0] 
    # print(return_coordinates_array)
    return return_coordinates_array, return_faces_array

# this function makes the whole thing 3D by getting each edge position and adding a 3D component to it
# it then calculates what the triangle verticies are that make up the faces and returns two arrays
# one array with the actual position of the verticies, and one that says how they connect to each other.
def triangle_solver(point_list, height):
    vertices = np.array([[point_list[0][0], point_list[0][1], height], [point_list[0][0], point_list[0][1], 0]])

    # print(len(point_list))
    faces = np.array([[len(point_list)*2-2, len(point_list)*2-1, 1],[len(point_list)*2-2, 0, 1]])

    # this calculates the triangles for the top/bottom.
    # it loops over the amount of triangles it has to make, and fills them in.
    for i in range(int((len(point_list)+1)/2-1)):
        new_faces = np.array([
            [0+2*i, len(point_list)*2-2-2*i, len(point_list)*2-4-2*i], # bottom triangles
            [0+2*i, 2+2*i, len(point_list)*2-4-2*i], 
            [1+2*i, len(point_list)*2-1-2*i, len(point_list)*2-3-2*i], # top triangles
            [1+2*i, 3+2*i, len(point_list)*2-3-2*i]
            ])
        faces = np.append(faces, new_faces, axis=0) # and then adds them to the existing face array

    for i, point in enumerate(point_list[1:]):
        triangle_connection = np.array([[i*2, i*2+1, i*2+3],[i*2, i*2+2, i*2+3]])
        faces = np.append(faces, triangle_connection, axis=0)

        vertice = np.array([[point[0], point[1], height], [point[0], point[1], 0]])
        vertices = np.append(vertices, vertice, axis=0)

    # return the two arrays for useage later
    return [faces, vertices]

# this function finds the x and y coordinates for a circle around the the end points.
def return_circle_coordinates(delta_x, delta_y, width, segment_length, x, y, t):
    
    circle_x_coordinate = (width*(delta_y*math.cos(t)-delta_x*math.sin(t)))/(2*segment_length)+x
    
    circle_y_coordinate = (width*(delta_y*math.sin(t)+delta_x*math.cos(t)))/(2*segment_length)+y

    return [circle_x_coordinate, circle_y_coordinate]

# return_line_coordinates takes the current trace and returns the coordinates of its edges.
# This is useful to make the traces continuous because otherwise there would be gaps in traces for each time a new coordinate is given.
def return_line_coordinates(x_coord, y_coord, start_x_coord, start_y_coord, current_width, num_circle_points): 
    # making function to calculate the outline of the main traces to work with freeCAD.
    # to make this I will make an x/y offset and move the aperture by that much
    # this offset requires a calculation of the hypotonuse/length of the line as well as the distance that the aperture moves in both x and y.
    return_point_list = []

    delta_x = x_coord - start_x_coord
    delta_y = y_coord - start_y_coord
    # using pythag for the length:
    segment_length = math.hypot(delta_x, delta_y)

    # using for loops to generate points that go around a circle at the end
    for i in range(num_circle_points + 2):
        t = i*(math.pi/(num_circle_points + 1))
        point_gen = return_circle_coordinates(-delta_x, delta_y, current_width, segment_length, x_coord, y_coord, t)
        return_point_list.append(point_gen)
    # and doing the same thing for the circle at the start
    for i in range(num_circle_points + 2):
        t = i*(math.pi/(num_circle_points + 1))
        point_gen = return_circle_coordinates(delta_x, -delta_y, current_width, segment_length, start_x_coord, start_y_coord, t)
        return_point_list.append(point_gen)

    # returning points in touple form to make it easier to identify x,y.
    return return_point_list

# this generates a simple circle around x_coord and y_coord with a radius of current width and a definition of num_flash_points
def return_flash_coordinates(x_coord, y_coord, current_width, num_flash_points):
    return_point_list = []

    for i in range(num_flash_points):
        t = i*(2*math.pi/(num_flash_points))
        x_point_gen = 0.5*current_width*math.cos(t) + x_coord
        y_point_gen = 0.5*current_width*math.sin(t) + y_coord
        return_point_list.append([x_point_gen,y_point_gen])

    return return_point_list

# this is the main loop with everything in it, it calls all the other functions in this.
def stl_creator(gerber_file_path, gerber_file_name, vector_scale_factor, ):
    gerber_file_extensionless = gerber_file_name.partition(".")[0]
    # user variables to be set
    vector_scale_factor = 500
    num_circle_points = 10 # this is the number of points in the end cap circles of the traces
    num_flash_points = 20 # this is the number of points in a cirlce cannot be below 3 and must be even.
    layer_height = 10
    # getting variables ready
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

    for aperture in aperture_list:
        aperture_instruction_dict[aperture[0]] = aperture[1].split(",") # makes an aperture with the shape information and the size information
    for instruction in instruction_array:
        if re.match(".*D([1-9][0-9]).*", instruction):
            current_aperture = re.findall(".*D([1-9][0-9]).*", instruction)[0] # This gives the number of the current aperture: that can be fed into the known dict to get the width and the shape

        if instruction.startswith("X"):
            to_x_coord = float(re.findall("X(.*)Y", instruction)[0])*pow(10, -1*scale)*vector_scale_factor
            to_y_coord = float(re.findall("Y(.*)D", instruction)[0])*pow(10, -1*scale)*vector_scale_factor
            current_width = float(aperture_instruction_dict[current_aperture][1].replace("*", ""))*vector_scale_factor

            if re.match(".*D01.*", instruction):
                line_edge_array = return_line_coordinates(to_x_coord, to_y_coord, last_x_coord, last_y_coord, current_width, num_circle_points)
                mesh_list.append(triangle_solver(line_edge_array, layer_height))

            if re.match(".*D03.*", instruction): # This needs to move to a point, create a single aperture point and stop. (ie it makes a circle with the apertures width)
                line_edge_array = return_flash_coordinates(to_x_coord, to_y_coord, current_width, num_flash_points)
                mesh_list.append(triangle_solver(line_edge_array, layer_height))

            # This tells the drawline function where the last known coordinates were
            last_x_coord = to_x_coord 
            last_y_coord = to_y_coord 
    vertices, faces = mesh_list_combiner(mesh_list)

    gerber_3d_model = stl.mesh.Mesh(np.zeros(faces.shape[0], dtype=stl.mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            gerber_3d_model.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    gerber_3d_model.save(f'{gerber_file_extensionless}.stl')
    return "testing123"
