# 3D printed circuit boards

3D printed circuit boards is a system to turn Gerber files into 3D printed circuit boards as easily as possible. It is supposed to allow many people of many skill levels to develop and play with their own circuit boards. 

This requires a 3D printer, preferably a dual nozzle one (as this will allow you to print without swapping filaments constantly.) with both conductive and non-conductive filaments.

## Installation

Download and install python onto your computer from https://www.python.org/downloads/ .

Download the 3D printed circuit board files onto a known location on your computer. 

Run the command to install numpy-stl, a required library for this system:
```bash
pip install numpy-stl
```

## Usage

Open Command prompt or Terminal depending on which operating system you use.

Navigate to the location of these files on your computer

You can then run the code using:
```bash
python index.py
```

From there select your preferences for how the 3D models will be generated, as well as selecting which gerber file you are turning into a 3D model.

Finally click convert and the stl 3D model will be generated in /Output 3D models/.

From there load the model into a 3D slicer of your choice and print or if you want an inlaid 3D model put the file in blender and make a mold, export the mold and import both the original and the mold to your slicer. In future the generation of a negative image will be automated by this system.

Done!