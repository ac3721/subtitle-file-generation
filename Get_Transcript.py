import cv2
import numpy as np

folder = 'Input Video'
video_name = "captions.mp4"
video_path = folder + '/' + video_name
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_index = 0

lower_color = np.array([204,50, 65])    # HSV lower bound
upper_color = np.array([210, 100, 100])  # HSV upper bound

prev_state = None
change_timestamps = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask for the selected color
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Optional: keep only that color in the frame
    filtered = cv2.bitwise_and(frame, frame, mask=mask)

    # Decide if color is "present" in this frame
    colored_pixels = cv2.countNonZero(mask)
    present = colored_pixels > 0  # or a threshold like > 500

    # Detect state change
    if prev_state is None:
        prev_state = present
    elif present != prev_state:
        # Color state changed at this frame
        timestamp_sec = frame_index / fps
        change_timestamps.append(timestamp_sec)
        prev_state = present
        print(timestamp_sec)

    frame_index += 1

cap.release()

print("Color-change timestamps (seconds):")
for t in change_timestamps:
    print(t)
