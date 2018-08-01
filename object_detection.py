import numpy as np
import time
import cv2
import glob

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

colors = [
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (255, 255, 0),  # idk
    (255, 0, 255),  # idk 2
    (0, 255, 255),  # idk 3
]

template = cv2.imread('templates/cacti-1.png', 0)

templates_files = glob.glob('templates\\*.png')
print(templates_files)
templates = []

for image in templates_files:
    image = cv2.imread(image, 0)
    templates.append(image)

while True:
    sct_img = np.array(sct.grab(monitor))
    sct_grey = cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY)

    for idx, template in enumerate(templates):
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(sct_grey, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95

        loc = np.where( res >= threshold )
        print(*loc)
        coordinates = zip(*loc[::-1])
        # print(*coordinates)

        for pt in coordinates:
            cv2.rectangle(sct_img, pt, (pt[0] + w, pt[1] + h), colors[idx], 2)

    # cv2.imshow('window', cv2.cvtColor(sct_img, cv2.COLOR_BGR2RGB))
    cv2.imshow('window', sct_img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
