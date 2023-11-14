# Gesture-Controlled Notepad and Drawing
## Overview
This Python script enables hands-free interaction with a notepad application and a drawing canvas using gesture recognition. It utilizes computer vision libraries such as OpenCV, MediaPipe, and Pynput.

## Usage
### Virtual Environment (venv) Setup:
Activate the virtual environment:
On Windows: `venv\Scripts\activate`
On macOS/Linux: `source venv/bin/activate`

---
### Install Dependencies:
Install required libraries: `pip install -r requirements.txt`

---
### Run the Script:
Run the Python script: `python handtracker.py`

### Interact with Notepad:
- Use your left hand to control notepad interactions.
- Raise fingers to simulate keyboard key presses.
- Adjust the hand's distance from the camera to trigger key presses.

### Drawing on Canvas:
- If two hands are detected, the script enters drawing mode.
- The right hand controls pen color based on raised fingers.
- The left hand draws on the canvas.
---

### Open files:
- Your right hand alone can open files, for example, pointer finger raised from closed hand it will open notepad.
---

### Exiting:
Certain finger gestures exit the drawing mode or close the notepad.
Metal sign with your right hand `{ .\m/ }` to terminate the script.
---

### Save Output:
The script saves the drawing as `canvas.png` and typed text in `text.txt`.

### Deactivate Virtual Environment:
Deactivate the virtual environment: `deactivate`