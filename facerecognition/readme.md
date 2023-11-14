# Driver Fatigue Detection with Blink Counter
## Overview
This Python script uses facial landmarks to detect signs of driver fatigue, focusing on blink analysis. It utilizes the MediaPipe library for facial landmark detection and OpenCV for image processing.

## Usage
### Virtual Environment (venv) Setup:
Activate the virtual environment: `python -m venv .`
On Windows: `venv\Scripts\activate`
On macOS/Linux: `source venv/bin/activate`

---
### Install Dependencies:
Install required libraries: `pip install -r requirements.txt`

---
### Run the Script:
Run the Python script: `python facerecognition.py`

### Monitor Facial Landmarks:

- The script uses facial landmarks to track both eyes and the mouth.
- Eye landmarks are used to calculate the Eye Aspect Ratio (EAR), indicating eye openness.
- Mouth landmarks are used to calculate the Mouth Aspect Ratio (MAR), indicating mouth openness.

### Blink Analysis:
- The script analyzes blinks based on the EAR and MAR values.
- It calculates the number of blinks, blink frequency, and total blink time.
- If the blink frequency is low or total blink time exceeds a threshold, a caution message is displayed.

### Caution Message:
- If signs of drowsiness are detected, a caution message is displayed on the screen.
- The script continuously monitors for signs of drowsiness while the camera is active.
---

### Exiting:
Certain finger gestures exit the drawing mode or close the notepad.
Press the `Esc` key to terminate the script.
---

### Deactivate Virtual Environment:
Deactivate the virtual environment: `deactivate`