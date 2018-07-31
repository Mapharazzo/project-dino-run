import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import pyqtgraph as pg
import cv2
from PIL import ImageGrab

from mss import mss

with mss() as sct:
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

    fps = 0.2

    while True:
        # Grab the data
        sct_img = np.array(sct.grab(monitor))


        # printscreen =  np.array(ImageGrab.grab(bbox=bbox))


        # print(sct_img)

        cv2.imshow('window', cv2.cvtColor(sct_img, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break