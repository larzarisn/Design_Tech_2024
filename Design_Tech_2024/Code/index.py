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
    current_file_text_box.configure(text=file_path)

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

root.title("Geber to STL")

# adding the title
title = Label(root, text= "Gerber to STL")
title.config(font=("Arial", 25))

current_file_text_box = Label(
    root,
    padx = 10,
    height = 2,
    width= 100,
    bg="white",
    bd=3,
    font=("Arial", 12),
    text="Input gerber file path"
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
    bg="white",
    bd=3,
    font=("Arial", 12),
    text="scale: ")
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
    bg="white",
    bd=3,
    font=("Arial", 12),
    text="trace resolution:")
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
    bg="white",
    bd=3,
    font=("Arial", 12),
    text="height: ")
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
    bg="white",
    bd=3,
    font=("Arial", 12),
    text="circle_resolution: ")
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


title.grid(column=1, row = 1, pady=20)
current_file_text_box.grid(column=1, row=2, pady=0, padx=20)
browse_button.grid(column=1, row=3, pady=0)
scale_label.grid(column=1, row= 4, pady=20, padx=20)
scale_spinbox.grid(column=2, row= 4, pady=20)
trace_resolution_label.grid(column=1, row= 5, pady=20)
trace_resolution_spinbox.grid(column=2, row= 5, pady=20)
circle_resolution_label.grid(column=1, row= 6, pady=20)
circle_resolution_spinbox.grid(column=2, row= 6, pady=20)
height_label.grid(column=1, row= 7, pady=20)
height_spinbox.grid(column=2, row= 7, pady=20)
convert_button.grid(column=1, row=8, padx=20, pady=20)

root.mainloop()