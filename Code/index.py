# this file will be the main loop of the program, it will have the GUI and the functions linkback.
import os
import file_to_vector

folder_path = "C:/Users/larsn/Desktop/Design tech/Fritzing/Temp testing" # replace this with a dynamic link, will happen with GUI

gerber_files = os.listdir(folder_path)

gerber_layers = {}
 
for gerber_file in gerber_files: # loop over all gerber files and sort them into layers, this will get messy, needs fixing once operational.
    gerber_file_path = folder_path + "/" + gerber_file
    print(gerber_file_path)
    if "bottom" in gerber_file.lower():
        try:
            gerber_layers["bottom"].append(gerber_file)
        except Exception as exception:
            print(exception)
            gerber_layers["bottom"] = [gerber_file]
    elif "top" in gerber_file.lower():
        try:
            testing = file_to_vector.vector_creator(gerber_file_path, 0)
            gerber_layers["top"].append(gerber_file)
        except Exception as exception:
            print(exception)
            gerber_layers["top"] = [gerber_file]
    else:
        try:
            gerber_layers["other"].append(gerber_file)
        except:
            gerber_layers["other"] = [gerber_file]

# now gerber_layers is a dict with split layers that can be used to turn the layers into independant images.
print(gerber_layers)