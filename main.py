import time
import mss
import cv2
import uuid
import numpy as np
import ctypes
import win32api

# Open source screenshot tool made by Gannon: https://www.youtube.com/@Gannon./videos

# Keybind
keybind = "0xBE" #Default is Period .  See: https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

delay_between_screenshots = 1 # Default is 1 second

screensize = {'X': ctypes.windll.user32.GetSystemMetrics(0), 'Y': ctypes.windll.user32.GetSystemMetrics(1)}

screen_res_X = screensize['X']  # Horizontal
screen_res_Y = screensize['Y']  # Vertical
screen_x = int(screen_res_X / 2)
screen_y = int(screen_res_Y / 2)

image_size = 640 # Size of the screen shots

def is_holding_keydind():
    return win32api.GetKeyState(int(keybind, 16)) in (-127, -128)

camera = mss.mss()
pause = 0
number_of_images_taken = 0
box = {
        'left': int(screen_x - image_size//2),
        'top': int(screen_y - image_size//2),
        'width': int(image_size),
        'height': int(image_size)
    }

while True:
    frame = np.array(camera.grab(box))
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if frame is not None:
        if is_holding_keydind() and time.perf_counter() - pause > 1:
            frame_copy = np.copy(frame)
            cv2.imwrite(f"images/{str(uuid.uuid4())}.jpg", frame_copy)
            pause = time.perf_counter()
            number_of_images_taken += 1
            print(f"Screenshots taken: {number_of_images_taken}")