import os
import index
import cairo
import re

def vector_creator(gerber_file_path, gerber_file_name, settings):
    gerber_file_extensionless = gerber_file_name.partition(".")[0]
    print(f"./Vectors/{gerber_file_extensionless}.svg")
    with cairo.SVGSurface(f"./Vectors/{gerber_file_extensionless}.svg", 700, 700) as svg_layer: 
        vector_scale_factor = 10
        cairo_context = cairo.Context(svg_layer)
        gerber_file = open(gerber_file_path, "r")   
        instruction_array = gerber_file.readlines()
        # have to loop over twice: once to get the vectors of the shapes and what tool to use, then to actually make the shapes in the svg
        # pg.26-> on gerber layer format pdf to specify which each thing is
        # have to make a list of tools with different sizes and etc....
        # then use that list to loop over the rest of the commands
        # possibly using {shape:[vectors]} as the structure (which will make this ugly)
        # then a for loop over each shape, and adding to svg
        # might want to make a line break process to watch it happen to an svg to understand it.
        aperture_instruction_dict = {}
        instruction_string = "".join(instruction_array)
        aperture_list = re.findall("ADD([0-9][0-9])(.*)?\*%", instruction_string) 
        scale = int(re.findall("FSLAX[1-6]([1-9])Y", instruction_string)[0])
        print(scale)
        current_aperture = "NaN"
        for aperture in aperture_list:
            aperture_instruction_dict[aperture[0]] = aperture[1].split(",") # makes an aperture with the shape information and the size information
        for instruction in instruction_array:
            if re.match(".*D([1-9][0-9]).*", instruction):
                print("stroke!")
                current_aperture = re.findall(".*D([1-9][0-9]).*", instruction)[0] # This gives the number of the current aperture: that can be fed into the known dict to get the width and the shape
                #cairo_context.scale(700, 700)
                cairo_context.stroke()

            if instruction.startswith("X"):
                cairo_context.set_line_width(float(aperture_instruction_dict[current_aperture][1])*vector_scale_factor) 
                cairo_context.set_line_cap(1)
                cairo_context.set_source_rgba(0, 0, 1, 1)
                to_x_coord = float(re.findall("X(.*)Y", instruction)[0])*pow(10, -1*scale)*vector_scale_factor
                to_y_coord = float(re.findall("Y(.*)D", instruction)[0])*pow(10, -1*scale)*vector_scale_factor
                print(f"current coordinates: y: {to_y_coord} x: {to_x_coord}  using aperture {current_aperture} with width of {cairo_context.get_line_width()}")

                if re.match(".*D01.*", instruction):
                    cairo_context.line_to(to_x_coord, to_y_coord)
                    #cairo_context.stroke()

                if re.match(".*D02.*", instruction):
                    cairo_context.move_to(to_x_coord, to_y_coord)
                    #cairo_context.stroke()

                if re.match(".*D03.*", instruction): # This needs to move to a point, create a single aperture point and stop.
                    cairo_context.move_to(to_x_coord, to_y_coord)
                    cairo_context.line_to(to_x_coord, to_y_coord)
                    #cairo_context.stroke()
        # cairo_context.scale(700, 700)
        cairo_context.stroke()
    return "balls"