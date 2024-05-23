# this file will be the main loop of the program, it will have the GUI and the functions linkback.
import os
from file_to_stl import *
from tkinter import *
from tkinter import filedialog
file_path = "NaN"
scale = 500
trace_resolution = 1 # this is the number of points in the end cap circles of the traces
circle_resolution = 4 # this is the number of points in a cirlce cannot be below 3 and must be even.
height = 10
# testing = stl_creator(file_path, "ProcessingRGB_copperBottom.gbl", scale, trace_resolution, circle_resolution, height)     

def browse_files():
    global file_path
    file_path = filedialog.askopenfilename(
        initialdir = "./",
        title = "Select a Gerber file",
    )
    current_file_text_box.configure(text=file_path.split("/")[-1])

def call_file_to_stl():
    if file_path == "NaN":
        return
    # print(file_path.split("/")[-1])
    stl_creator(file_path, file_path.split("/")[-1], scale, trace_resolution, circle_resolution, height)

def scale_change():
    global scale
    scale = scale_spinbox.get()

def trace_resolution_change():
    global trace_resolution
    trace_resolution = trace_resolution.get()

def circle_resolution_change():
    global circle_resolution
    circle_resolution = circle_resolution_spinbox.get()

def height_change():
    global height
    height = height_spinbox.get()

root = Tk()

root.geometry("600x350")
root.minsize(600, 350)
root.maxsize(600, 350)
root.title("Geber to STL")

# adding the title
title = Label(root, text= "Gerber to STL")
title.config(font=("Arial", 25))

file_text_frame = Frame()

current_file_text_box = Label(
    root,
    padx = 10,
    width= 50,
    height=2,
    bg="white",
    bd=3,
    font=("Arial", 12),
    text="Input gerber file path",
    borderwidth=1,
    relief="solid"
)


browse_button = Button(
    root,
    text = "browse",
    font=("Arial", 12),
    command = browse_files,
    height = 2,
    cursor="hand2",
    width = 6    
)

scale_var = DoubleVar(value=scale)
scale_label = Label(
    root,
    padx = 10,
    font=("Arial", 12),
    text="Scale: ",
    anchor="w",
    width=12,
    )
scale_spinbox = Spinbox(
    root,
    from_= 0,
    to=1000,
    width=10,
    font=("Arial", 12),
    cursor="hand2",
    command = scale_change,
    textvariable=scale_var
)

trace_resolution_var = DoubleVar(value=trace_resolution)
trace_resolution_label = Label(
    root,
    padx = 10,
    font=("Arial", 12),
    text="Trace resolution:",
    anchor="w",
    width=12,
    )
trace_resolution_spinbox = Spinbox(
    root,
    from_= 0,
    to=1000,
    width=10,
    font=("Arial", 12),
    cursor="hand2",
    command = trace_resolution_change,
    textvariable=trace_resolution_var
)

height_var = DoubleVar(value=height)
height_label = Label(
    root,
    padx = 10,
    font=("Arial", 12),
    text="Height: ",
    anchor="w",
    width=12,
    )
height_spinbox = Spinbox(
    root,
    from_= 0,
    to=1000,
    width=10,
    font=("Arial", 12),
    cursor="hand2",
    command = height_change,
    textvariable=height_var
)

circle_resolution_var = DoubleVar(value=circle_resolution)
circle_resolution_label = Label(
    root,
    padx = 10,
    bd=3,
    font=("Arial", 12),
    text="Circle resolution: ",
    anchor="w",
    width=12
    )
circle_resolution_spinbox = Spinbox(
    root,
    from_= 0,
    to=1000,
    width=10,
    font=("Arial", 12),
    cursor="hand2",
    command = circle_resolution_change,
    textvariable=circle_resolution_var
)

# Creating the convert button
convert_button = Button(
    root, 
    text="Convert", 
    command=call_file_to_stl,
    anchor="center",
    cursor="hand2",
    disabledforeground="gray",
    fg="black",
    font=("Arial", 12),
    height=2,
    highlightthickness=2,
    justify="center",
    overrelief="raised",
    padx=10,
    pady=5,
    width=15,
    wraplength=100
)


title.grid(column=0, row = 0, columnspan=4 ,pady=20)

current_file_text_box.grid(column=0, row=1, pady=10, padx=(35, 0), columnspan=2)

browse_button.grid(column=2, row=1, pady=0)

scale_label.grid(column=0, row= 2, padx=20, sticky="E")
scale_spinbox.grid(column=1, row= 2, sticky="W")

trace_resolution_label.grid(column=0, row= 3, padx=20, sticky="E")
trace_resolution_spinbox.grid(column=1, row= 3, sticky="W")

circle_resolution_label.grid(column=0, row= 4, padx=20, sticky="E")
circle_resolution_spinbox.grid(column=1, row= 4, sticky="W")

height_label.grid(column=0, row= 5, padx=20, sticky="E")
height_spinbox.grid(column=1, row= 5, sticky="W")

convert_button.grid(column=0, row=6, padx=20, pady=20, columnspan=4)

root.mainloop()