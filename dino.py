import numpy as np
import time
import cv2
import screen
from pynput.keyboard import Key, Controller

while True:
    sct_img = screen.grab_screen()
    screen.draw_screen(sct_img, detection=True)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
