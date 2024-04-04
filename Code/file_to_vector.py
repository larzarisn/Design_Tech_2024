import os
import index
import cairo
import re

def vector_creator(gerber_file_path, gerber_file_name, settings):
    gerber_file_extensionless = gerber_file_name.partition(".")[0]
    print(f"./Vectors/{gerber_file_extensionless}.svg")
    with cairo.SVGSurface(f"./Vectors/{gerber_file_extensionless},svg", 700, 700) as svg_layer: 
        cario_context = cairo.Context(svg_layer)
        
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
        aperture_list = re.findall("ADD([0-9][0-9])(.*)?%", instruction_string) 
        current_aperture = "NaN"
        for aperture in aperture_list:
            aperture_instruction_dict[aperture[0]] = [aperture[1]]
        for instruction in instruction_array:
            if re.match(".*D([1-9][0-9]).*", instruction):
                print(instruction)
                current_aperture = re.findall(".*D([1-9][0-9]).*", instruction)[0]
            
        # tool_instruction_dict = {}
        # for instruction in instruction_array: # REGEX
        #     if instruction.startswith("%ADD"):
        #         tool_instruction_dict[instruction[4:6]] = [instruction[6:-3], []]
        # for instruction in instruction_array: # REGEX
        #     current_aperature = 0
        #     print(instruction)
        #     if "D" in instruction: 
        #         aperature_index = instruction.index("D")
        #         aperature = instruction[aperature_index:]
        #         if is_integer(aperature[1:3]):
        #             if int(aperature[1:3]) >= 3:
        #                 print(aperature)
        #         print(current_aperature)
        print(aperture_instruction_dict)
    return "balls"