
# importing pycairo 
import cairo 
import random
  
# creating a SVG surface 
# here geek is file name & 700, 700 is dimension 
with cairo.SVGSurface("./Vectors/geek.svg", 700, 700) as surface: 
  
    # creating a cairo context object 
    context = cairo.Context(surface) 

    i = 0
    while i < 10:
        i = i + 1
        context.stroke() 
        context.set_line_width(0.01+i*0.1)
        context.move_to(random.uniform(0, 700), random.uniform(0, 700))
        context.line_to(0, 0)
        # setting color of the context 
        context.set_source_rgba(0.4, 1, 0.4, 1) 
        # stroke out the color and width property 
    context.scale(700, 700) 
  

  
  
# printing message when file is saved 
print("File Saved") 