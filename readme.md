# 3D printed circuit boards

3D printed circuit boards is a system to turn Gerber files into 3D printed circuit boards as easily as possible. It is supposed to allow many people of many skill levels to develop and play with their own circuit boards. 

This requires a 3D printer, preferably a dual nozzle one (as this will allow you to print without swapping filaments constantly.) with both conductive and non-conductive filaments.

## Installation (Windows)
1. Download the 3D printed circuit board files onto a known location on your computer. Click "Code" on github and Download zip to download it. Then extract it from the zip file it is in.

2. Download and install python, on the first screen on opening the .exe file make sure to tick the "Add python.exe to PATH" selection box and then continue the installation onto your computer from [https://www.python.org/downloads/](https://www.python.org/downloads/).

4. Open command prompt in the windows search and run the following command to install numpy-stl, a required library for this system:
```bash
pip install numpy-stl
```

## Usage

Open Command prompt or Terminal depending on which operating system you use.

Navigate to the location of these files on your computer:

(On windows to navigate in the command prompt, use "cd {folder name}" to move between folders, "cd .." to go back a folder and "dir" to list folders you can navigate to.)

You can then run the code using:
```bash
python index.py
```

From there select your preferences for how the 3D models will be generated, as well as selecting which gerber file you are turning into a 3D model.

Finally click convert and the stl 3D model will be generated in ./Output 3D models/. (which is inside the project folder)

From there load the model into a 3D slicer of your choice and follow your printers instructions. 

## Making negatives with blender (Advanced only)
If you want an inlaid 3D model, the easiest method I have found follows this video: [https://www.youtube.com/watch?v=57CmROIJP6w](https://www.youtube.com/watch?v=57CmROIJP6w):
1. Load the model into blender by importing the STL you have just generated
2. Use the create box tool in blender to create a box that entirely encompasses the STL
3. Select the box and in the bottom right of the screen select modify and boolean and select the STL you loaded as the boolean object.