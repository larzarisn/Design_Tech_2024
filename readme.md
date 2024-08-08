# 3D printed circuit boards

3D printed circuit boards is a system to turn Gerber files into 3D printed circuit boards as easily as possible. It is supposed to allow many people of many skill levels to develop and play with their own circuit boards. 

This requires a 3D printer, preferably a dual nozzle one (as this will allow you to print without swapping filaments constantly.) with both conductive and non-conductive filaments.

## Installation (Windows)

1. Download and install python onto your computer from https://www.python.org/downloads/ .

2. Download the 3D printed circuit board files onto a known location on your computer. 

3. Run the following command to install numpy-stl, a required library for this system:
```bash
pip install numpy-stl
```

4. Install Tkinter:
```bash
pip install Tkinter
```

## Usage

Open Command prompt or Terminal depending on which operating system you use.

Navigate to the location of these files on your computer

You can then run the code using:
```bash
python index.py
```

From there select your preferences for how the 3D models will be generated, as well as selecting which gerber file you are turning into a 3D model.

Finally click convert and the stl 3D model will be generated in ./Output 3D models/. (which is inside the project folder)

From there load the model into a 3D slicer of your choice and follow your printers instructions. 

If you want an inlaid 3D model, the easiest method I have found follows this video: [https://www.youtube.com/watch?v=57CmROIJP6w](https://www.youtube.com/watch?v=57CmROIJP6w).