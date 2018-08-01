import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import pyqtgraph as pg
import cv2
from PIL import ImageGrab

from mss import mss

sct = mss()
# The screen part to capture

# 1440p monitor parameteres
top = 300
left = 943
width = 675
height = 200

monitor = {'top': top, 'left': left, 'width': width, 'height': height}


left = 945
right = 1620
up = 300
down = 470

bbox = (left, up, right, down)

# trigger for window switching
# time.sleep(5)

template = cv2.imread('templates/cacti-1v2.png', 0)

w, h = template.shape[::-1]

while True:
    sct_img = np.array(sct.grab(monitor))
    # Grab the data

    sct_grey = cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(sct_grey, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7

    loc = np.where( res >= threshold )

    print(loc)

    coordinates = zip(*loc[::-1])


    for pt in zip(*loc[::-1]):
        cv2.rectangle(sct_img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    cv2.imshow('window', cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY))

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
