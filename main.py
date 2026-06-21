import cv2
import time
import numpy as np
from PIL import ImageGrab

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def take_full_screen_screenshot():
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    filename = f"screen_{int(time.time())}.png"
    cv2.imwrite(filename, screenshot)
    print("Saved full screen:", filename)

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        take_full_screen_screenshot()

cv2.namedWindow("Drone Vision")
cv2.namedWindow("Green Detection")

# MB1 works in either window
cv2.setMouseCallback("Drone Vision", on_mouse)
cv2.setMouseCallback("Green Detection", on_mouse)

prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time else 0
    prev_time = current_time

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.imshow("Drone Vision", frame)
    cv2.imshow("Green Detection", result)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    if cv2.getWindowProperty("Drone Vision", cv2.WND_PROP_VISIBLE) < 1:
        break

    if cv2.getWindowProperty("Green Detection", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()