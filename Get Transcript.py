import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_text(img, debug = False):
    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define blue color range
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([145, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # Extract blue text from image
    blue_text_img = cv2.bitwise_and(img, img, mask=mask)
    if debug:
        plt.imshow(cv2.cvtColor(blue_text_img, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.show()
    print(cv2.countNonZero(mask))
    return cv2.countNonZero(mask), blue_text_img

folder = 'Input Video'
video_name = "Short.mp4"
video_path = video_name #folder + '/' + video_name
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_index = 0

prev_state = None
prev = None
text = []
change_timestamps = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    present_pixel, filtered = find_text(frame)
    if present_pixel > 5000:
        if prev_state is None:
            prev_state = filtered
            prev = present_pixel
            text.append(frame)
        elif present_pixel - prev > 1000: #filtered != prev_state and 
            # Color state changed at this frame
            timestamp_sec = frame_index / fps
            change_timestamps.append(timestamp_sec)
            prev_state = filtered
            text.append(frame)
            print(timestamp_sec)

    frame_index += 1

cap.release()

print("Color-change timestamps (seconds):")
for t in change_timestamps:
    print(t)

for frame in text:
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()

print("Color-change timestamps (seconds):")
for t in change_timestamps:
    print(t)
