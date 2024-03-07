import time
import mss
import cv2
import uuid
import numpy as np
import ctypes
import win32api
import os

# Open source screenshot tool made by Gannon: https://www.youtube.com/@Gannon./videos

# Configuration
keybind = '0xBE' #Default is Period .  See: https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
image_size = 640 # Size of the screen shots
delay_between_screenshots = 1 # Default is 1 second
images_folder_path = 'images'


half_screen_x = int(ctypes.windll.user32.GetSystemMetrics(0) / 2)
half_screen_y = int(ctypes.windll.user32.GetSystemMetrics(1) / 2)
camera = mss.mss()
pause = number_of_images_taken = 0

box = {
        'left': int(half_screen_x - image_size//2),
        'top': int(half_screen_y - image_size//2),
        'width': int(image_size),
        'height': int(image_size)
    }

if not os.path.exists(images_folder_path):
    print('Creating images folder..')
    os.mkdir('images')

def is_holding_keydind():
    return win32api.GetKeyState(int(keybind, 16)) in (-127, -128)

while True:
    frame = np.array(camera.grab(box))
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if frame is not None:
        if is_holding_keydind() and time.perf_counter() - pause > 1:
            frame_copy = np.copy(frame)
            cv2.imwrite(f'images/{str(uuid.uuid4())}.jpg', frame_copy)
            pause = time.perf_counter()
            number_of_images_taken += 1
            print(f'Screenshots taken: {number_of_images_taken}')