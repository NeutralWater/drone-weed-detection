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

    # Connect nearby green pixels and fill small gaps
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Calculate how much of the camera frame is green
    green_pixels = cv2.countNonZero(mask)
    total_pixels = frame.shape[0] * frame.shape[1]
    green_percent = (green_pixels / total_pixels) * 100

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.putText(
                frame,
                f"Green Target: {int(area)}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.putText(
    frame,
    f"Green Coverage: {green_percent:.1f}%",
    (10, 65),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (255, 255, 255),
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