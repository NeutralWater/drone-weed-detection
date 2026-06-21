# Drone Weed Detection 

A Python and OpenCV computer-vision prototype that detects green vegetation-like regions from a live webcam feed.

## Features

- Live webcam feed
- HSV-based green color detection
- Contour detection with bounding boxes
- Green coverage percentage
- Detected-region pixel area labels
- FPS counter
- Full-screen screenshot capture with left mouse click
- Press `Q` to quit safely

## How It Works

The program converts each webcam frame from BGR to HSV color space. It creates a mask for green pixels, fills small gaps between nearby green pixels, and detects connected green regions using contours.

Each detected region receives:

- A bounding box
- A pixel-area measurement
- A `Green Target` label

## Current Limitation

The prototype detects **green regions**, not weeds specifically. Crops, weeds, green objects, and green packaging can all trigger detection.

A future version could use a machine-learning model trained on labeled crop and weed images to classify each detected plant correctly.

## Technologies

- Python
- OpenCV
- NumPy
- Pillow

## Controls

| Control | Action |
|---|---|
| Left Mouse Button | Save a full-screen screenshot |
| `Q` | Quit the program |

## Run It

Install dependencies:

```bash
python -m pip install opencv-python numpy pillow